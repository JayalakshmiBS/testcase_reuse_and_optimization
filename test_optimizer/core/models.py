# core/models.py
# This file MUST be updated to support the new report format.

from django.db import models

class Program(models.Model):
    name = models.CharField(max_length=100, unique=True)
    source_zip = models.FileField(upload_to='programs/')
    is_golden_source = models.BooleanField(default=False)
    required_mappings = models.JSONField(default=dict, blank=True)
    interface_map = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name

class TestCase(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    test_id = models.CharField(max_length=500, unique=True)
    is_in_golden_suite = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.test_id

class CoveredElement(models.Model):
    element_id = models.CharField(max_length=500, unique=True)
    tests = models.ManyToManyField(TestCase, related_name='covered_elements')

    def __str__(self):
        return self.element_id

# --- THIS MODEL IS UPDATED ---
class AnalysisReport(models.Model):
    target_program = models.OneToOneField(Program, on_delete=models.CASCADE)

    # Stores the list of GREEN, YELLOW, RED test items
    classification_data = models.JSONField(default=list)

    # --- NEW FIELDS FOR VERIFICATION ---
    final_statement_coverage = models.FloatField(null=True, blank=True)
    final_branch_coverage = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.target_program.name}"