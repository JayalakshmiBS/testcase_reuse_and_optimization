# views.py
import json
import io
from django.conf import settings
from django.http import HttpResponse
import zipfile
from pathlib import Path
from django.shortcuts import render, redirect
from celery.result import AsyncResult
from .models import Program, AnalysisReport
from .services import adapt_test_code, discover_required_mappings, run_full_analysis_for_program

def upload_view(request):
    """
    Handles the initial upload.
    Checks if an interface_map.json exists. If so, runs the full analysis.
    If not, runs the discovery task to generate the mapping form.
    """
    if request.method == 'POST':
        program_name = request.POST.get('name')
        source_zip = request.FILES.get('source_zip')
        if program_name and source_zip:
            program, created = Program.objects.update_or_create(
                name=program_name,
                defaults={'source_zip': source_zip, 'required_mappings': {}}
            )
            AnalysisReport.objects.filter(target_program=program).delete()

            # --- NEW LOGIC: Check for interface_map.json ---
            try:
                with zipfile.ZipFile(source_zip, 'r') as zip_ref:
                    map_file_info = next((f for f in zip_ref.infolist() if Path(f.filename).name == 'interface_map.json'), None)
                    if map_file_info:
                        # If the map exists, read it and pass it to the main task
                        with zip_ref.open(map_file_info) as map_file:
                            interface_map = json.load(map_file)
                        print("[WORKFLOW] interface_map.json found. Starting full analysis.")
                        task = run_full_analysis_for_program.delay(program.id, interface_map)
                        return redirect('analysis_status_view', task_id=task.id)
                    else:
                        # If no map, run the discovery task
                        print("[WORKFLOW] interface_map.json NOT found. Starting discovery.")
                        task = discover_required_mappings.delay(program.id)
                        return redirect('discovery_status_view', task_id=task.id)
            except zipfile.BadZipFile:
                return render(request, 'core/upload.html', {'error': 'Invalid ZIP file uploaded.'})
            
    return render(request, 'core/upload.html')

def discovery_status_view(request, task_id):
    """Monitors the discovery task and redirects to the mapping form when ready."""
    task_result = AsyncResult(task_id)
    if task_result.ready():
        try:
            program = Program.objects.latest('id')
            return redirect('mapping_view', program_id=program.id)
        except Program.DoesNotExist:
            return render(request, 'core/error.html', {'message': 'Could not find program after discovery.'})
    return render(request, 'core/status.html',  {'task_id': task_id,'message': 'Step 1: Discovering reusable test functions...'})

    
def mapping_view(request, program_id):
    """Displays the mapping form and triggers the final analysis."""
    program = Program.objects.get(id=program_id)
    if request.method == 'POST':
        # --- THIS LOGIC IS NOW SIMPLER ---
        # Build the map dictionary from the form
        interface_map = {
            "module_name": request.POST.get('module_name'),
            "class_name": request.POST.get('class_name'),
            "function_mappings": {}
        }
        for key, value in request.POST.items():
            if key.startswith('func_'):
                old_name = key.replace('func_', '')
                if value:
                    interface_map["function_mappings"][old_name] = value
        
        # Trigger the main analysis task, passing the map directly
        task = run_full_analysis_for_program.delay(program.id, interface_map)
        return redirect('analysis_status_view', task_id=task.id)

    context = {
        'program': program,
        'mappings': program.required_mappings
    }
    return render(request, 'core/mapping_form.html', context)

def analysis_status_view(request, task_id):
    """Monitors the main analysis task and redirects to the final report."""
    task_result = AsyncResult(task_id)
    if task_result.ready():
        try:
            report = AnalysisReport.objects.latest('created_at')
            return redirect('report_view', program_id=report.target_program.id)
        except AnalysisReport.DoesNotExist:
            return render(request, 'core/error.html', {'message': 'Analysis complete, but no report was found.'})
    return render(request, 'core/status.html', {'task_id': task_id,'message': 'Step 2: Running full analysis with your mapping...'})

    
# def analysis_status_view(request, task_id):
#     """Monitors the main analysis task and redirects to the final report."""
#     task_result = AsyncResult(task_id)
#     if task_result.ready():
#         try:
#             # This logic needs to be more robust to find the correct report
#             report = AnalysisReport.objects.latest('created_at')
#             return redirect('report_view', program_id=report.target_program.id)
#         except AnalysisReport.DoesNotExist:
#             return render(request, 'core/error.html', {'message': 'Analysis complete, but no report was found.'})
#     return render(request, 'core/status.html', {'message': 'Step 2: Running full analysis with your mapping...'})


def status_view(request, task_id):
    """Shows a "processing" page and checks the status of the Celery task."""
    task_result = AsyncResult(task_id)
    if task_result.ready():
        # The task is finished.
        # We need to find the program associated with the analysis to show the report.
        # This is a bit tricky without modifying the task to return the program_id.
        # For now, we'll just find the latest report. A more robust solution
        # would be needed for a multi-user system.
        try:
            latest_report = AnalysisReport.objects.latest('created_at')
            return redirect('report_view', program_id=latest_report.target_program.id)
        except AnalysisReport.DoesNotExist:
            return render(request, 'core/error.html', {'message': 'Analysis complete, but no report was found.'})

    return render(request, 'core/status.html', {'task_id': task_id})

def report_view(request, program_id):
    """Displays the final, color-coded report."""
    try:
        program = Program.objects.get(id=program_id)
        report = AnalysisReport.objects.get(target_program=program)
        context = {
            'program': program,
            'report': report,
            'report_data': report.classification_data,
        }
        return render(request, 'core/report.html', context)
    except (Program.DoesNotExist, AnalysisReport.DoesNotExist):
        return render(request, 'core/error.html', {'message': 'Report not found for this program.'})
def download_suite_view(request, program_id):
    """
    Generates and serves the final, optimized test suite as a ZIP file,
    including the full, adapted code for reusable tests.
    """
    program = Program.objects.get(id=program_id)
    report = AnalysisReport.objects.get(target_program=program)
    
    # Get the interface map that was used for this analysis
    interface_map = program.interface_map

    # Use an in-memory buffer to create the ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        
        # 1. Add the adapted GREEN tests
        green_test_ids = [item['test_id'] for item in report.classification_data if item['status'] == 'GREEN']
        
        # Group tests by their original file to reconstruct them
        adapted_files = {}
        for test_id in green_test_ids:
            app_name, node_id = test_id.split("::", 1)
            file_path_str, func_name = node_id.split("::", 1)
            
            if file_path_str not in adapted_files:
                # Read the original file content
                original_test_file = settings.BASE_DIR.parent / "calculators" / app_name / file_path_str
                with open(original_test_file, 'r', encoding='utf-8') as f:
                    original_code = f.read()
                
                # Adapt the entire file's code at once
                adapted_code = adapt_test_code(original_code, interface_map)
                adapted_files[file_path_str] = adapted_code

        # Write the adapted files to the zip
        for file_path_str, adapted_code in adapted_files.items():
            file_name = Path(file_path_str).name
            zip_file.writestr(f"reused_tests/{file_name}", adapted_code)

        # 2. Add the AI-generated (RED) tests
        red_tests_code = "import pytest\nimport math\n\n"
        red_items = [item for item in report.classification_data if item['status'] == 'RED']
        
        for item in red_items:
            red_tests_code += f"# Suggestion for: {item['suggestion_title']}\n"
            red_tests_code += item['suggestion_code'] + "\n\n"
            
        if red_items:
             zip_file.writestr("generated_tests/test_generated_gaps.py", red_tests_code)

    # Prepare the HTTP response to trigger a download
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{program.name}_optimized_suite.zip"'
    return response
