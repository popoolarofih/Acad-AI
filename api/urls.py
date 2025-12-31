from django.urls import path
from .views import (
    ExamListView, ExamDetailView,
    SubmissionCreateView, SubmissionDetailView, SubmissionListView,
    register_user, login_user
)

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', register_user, name='user-register'),
    path('auth/login/', login_user, name='user-login'),

    # Exam endpoints
    path('exams/', ExamListView.as_view(), name='exam-list'),
    path('exams/<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),

    # Submission endpoints
    path('submissions/', SubmissionCreateView.as_view(), name='submission-create'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
    path('my-submissions/', SubmissionListView.as_view(), name='my-submissions'),
]
