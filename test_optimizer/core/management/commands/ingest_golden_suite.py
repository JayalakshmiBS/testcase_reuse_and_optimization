# core/management/commands/ingest_golden_suite.py
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings # <-- Import Django's settings
from core.models import Program, TestCase, CoveredElement

# --- CORRECTED PATH LOGIC ---
# Use Django's BASE_DIR for a reliable path.
# BASE_DIR points to 'D:\Testcase\test_optimizer'
# .parent goes up one level to 'D:\Testcase'
# Then we append the 'calculators' folder name.
CALCULATORS_ROOT = settings.BASE_DIR.parent / "calculators"

class Command(BaseCommand):
    help = 'Ingests all coverage data from the original calculator apps.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("--- Starting Golden Suite Ingestion ---")
        self.stdout.write(f"Looking for assets in: {CALCULATORS_ROOT}")

        # Load the perfected minimized suite
        minimized_suite_path = CALCULATORS_ROOT / "minimized_suite.json"
        if not minimized_suite_path.exists():
            self.stderr.write(self.style.ERROR(f"FATAL: minimized_suite.json not found at {minimized_suite_path}"))
            self.stderr.write(self.style.ERROR("Please ensure the 'calculators' folder is next to your 'test_optimizer' project folder and contains the minimized_suite.json file."))
            return

        with open(minimized_suite_path, 'r') as f:
            golden_test_ids = set(json.load(f))
        self.stdout.write(f"Loaded {len(golden_test_ids)} golden test case IDs.")

        # Clear old data
        self.stdout.write("Clearing old data from the database...")
        Program.objects.all().delete()
        # TestCase and CoveredElement are deleted automatically due to cascading deletes

        # Process each calculator app
        for app_dir in CALCULATORS_ROOT.iterdir():
            if not app_dir.is_dir() or not app_dir.name.startswith("Calculator"):
                continue
            
            self.stdout.write(f"Processing app: {app_dir.name}")

            program, _ = Program.objects.get_or_create(
                name=app_dir.name,
                defaults={'is_golden_source': True, 'source_zip': ''}
            )

            report_dir = app_dir / "individual_coverage_reports"
            if not report_dir.exists(): continue

            for report_file in report_dir.glob("*.json"):
                with open(report_file, 'r') as f:
                    data = json.load(f)

                test_id = data.get("meta", {}).get("test_id")
                if not test_id: continue

                test_case, _ = TestCase.objects.get_or_create(
                    test_id=test_id,
                    program=program,
                    defaults={'is_in_golden_suite': test_id in golden_test_ids}
                )

                for filename, file_data in data.get("files", {}).items():
                    if "src" not in Path(filename).parts: continue

                    full_path = (Path(program.name) / filename).as_posix()
                    for line_num in file_data.get("executed_lines", []):
                        element_id = f"{full_path}:line_{line_num}"
                        element, _ = CoveredElement.objects.get_or_create(element_id=element_id)
                        element.tests.add(test_case)

        self.stdout.write(self.style.SUCCESS("✅ Successfully ingested all data."))