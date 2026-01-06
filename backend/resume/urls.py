from django.urls import path
from .views import test_api, upload_resume, compare_resume

urlpatterns = [
    path('test/', test_api),
    path('upload_resume/', upload_resume),  # make sure this matches exactly
    path('compare_resume/', compare_resume),
]
