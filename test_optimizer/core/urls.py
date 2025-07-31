# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_view, name='upload_view'),
    path('discover/status/<str:task_id>/', views.discovery_status_view, name='discovery_status_view'),
    path('mapping/<int:program_id>/', views.mapping_view, name='mapping_view'),
    path('analysis/status/<str:task_id>/', views.analysis_status_view, name='analysis_status_view'),
    path('report/<int:program_id>/', views.report_view, name='report_view'),
    path('report/<int:program_id>/download/', views.download_suite_view, name='download_suite'),
]
