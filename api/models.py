from django.contrib.auth.models import User

class Exam(models.Model):
    title = models.CharField(max_length=255)
    duration = models.IntegerField(help_text="Duration in minutes")
    course = models.CharField(max_length=255)
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=[('multiple_choice', 'Multiple Choice'), ('text', 'Text')])
    expected_answer = models.TextField()

    def __str__(self):
        return self.question_text[:50]

class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    answers = models.JSONField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Submission by {self.student.username} for {self.exam.title}"
=======
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Exam(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    course = models.CharField(max_length=255, db_index=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True, help_text="Exam submission deadline")

    class Meta:
        indexes = [
            models.Index(fields=['course', 'title']),
        ]

    def __str__(self):
        return self.title

    def is_expired(self):
        """Check if the exam deadline has passed"""
        if self.deadline:
            return timezone.now() > self.deadline
        return False

    def time_remaining(self):
        """Calculate time remaining until deadline"""
        if self.deadline:
            remaining = self.deadline - timezone.now()
            return max(remaining, timedelta(0))
        return None

class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=[('multiple_choice', 'Multiple Choice'), ('text', 'Text')], db_index=True)
    expected_answer = models.TextField()
    options = models.JSONField(blank=True, null=True, help_text="Multiple choice options")
    points = models.FloatField(default=1.0, help_text="Points for this question")

    def __str__(self):
        return self.question_text[:50]

class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    answers = models.JSONField()
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)
    grade = models.FloatField(null=True, blank=True, db_index=True)
    is_late = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['student', 'exam']),
            models.Index(fields=['submitted_at']),
        ]
        unique_together = ['student', 'exam']

    def __str__(self):
        return f"Submission by {self.student.username} for {self.exam.title}"

    def save(self, *args, **kwargs):
        # Check if submission is late
        if self.exam.deadline and self.submitted_at > self.exam.deadline:
            self.is_late = True
        super().save(*args, **kwargs)
