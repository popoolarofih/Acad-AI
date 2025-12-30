from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Exam, Question, Submission
from .grading import grade_submission
from unittest.mock import patch

class ExamAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.exam = Exam.objects.create(title='Test Exam', duration=60, course='Test Course')
        self.question = Question.objects.create(exam=self.exam, question_text='Test Question?', question_type='text', expected_answer='Test Answer')

    def test_exam_list(self):
        response = self.client.get('/api/exams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_exam_detail(self):
        response = self.client.get(f'/api/exams/{self.exam.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Exam')
        self.assertNotIn('expected_answer', response.data['questions'][0])

    @patch('api.grading.grade_text_answer', return_value=0.9)
    def test_submission_create(self, mock_grade_text_answer):
        data = {
            'exam': self.exam.id,
            'answers': {str(self.question.id): 'Test Answer'}
        }
        response = self.client.post('/api/submissions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Submission.objects.count(), 1)

        submission = Submission.objects.first()
        self.assertIsNotNone(submission.grade)

    def test_submission_security(self):
        submission = Submission.objects.create(student=self.user, exam=self.exam, answers={})

        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.force_authenticate(user=other_user)

        response = self.client.get(f'/api/submissions/{submission.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class GradingTestCase(TestCase):
    def setUp(self):
        self.exam = Exam.objects.create(title='Grading Test Exam', duration=60, course='Test Course')
        self.question1 = Question.objects.create(exam=self.exam, question_text='Q1', question_type='text', expected_answer='apple')
        self.question2 = Question.objects.create(exam=self.exam, question_text='Q2', question_type='multiple_choice', expected_answer='b')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    @patch('api.grading.grade_text_answer', return_value=0.9)
    def test_grading_logic(self, mock_grade_text_answer):
        answers = {
            str(self.question1.id): 'an apple a day',
            str(self.question2.id): 'b'
        }
        submission = Submission.objects.create(student=self.user, exam=self.exam, answers=answers)
        grade = grade_submission(submission)

        self.assertIsNotNone(grade)
        self.assertGreater(grade, 0)
