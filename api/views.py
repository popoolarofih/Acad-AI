from rest_framework import generics
from .models import Exam, Submission
from .serializers import ExamSerializer, SubmissionSerializer, StudentExamSerializer
from .permissions import IsOwner
from .grading import grade_submission

class ExamListView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = StudentExamSerializer

class ExamDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = StudentExamSerializer

class SubmissionCreateView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        submission = serializer.save(student=self.request.user)
        grade_submission(submission)

class SubmissionDetailView(generics.RetrieveAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsOwner]
