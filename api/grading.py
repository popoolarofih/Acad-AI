import os
import re
from groq import Groq

def grade_submission(submission):
    """
    Grades a submission using a mock grading service.
    """
    total_score = 0
    question_count = 0

    exam = submission.exam
    questions = exam.questions.all()
    answers = submission.answers

    for question in questions:
        question_count += 1
        if str(question.id) in answers:
            student_answer = answers[str(question.id)]
            if question.question_type == 'text':
                score = grade_text_answer(question.expected_answer, student_answer)
                total_score += score
            else:
                if student_answer.lower() == question.expected_answer.lower():
                    total_score += 1

    grade = (total_score / question_count) * 100 if question_count > 0 else 0
    submission.grade = grade
    submission.save()
    return grade

def grade_text_answer(expected_answer, student_answer):
    """
    Grades a text answer using Groq API.
    """
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Please rate the similarity between the following two answers on a scale of 0 to 1, where 1 is identical and 0 is completely different. Respond with only the number. \n\nExpected Answer: {expected_answer}\n\nStudent Answer: {student_answer}",
                }
            ],
            model="llama3-8b-8192",
        )
        response_text = chat_completion.choices[0].message.content

        # Use regex to find a float or integer in the response
        match = re.search(r"(\d(?:\.\d+)?)", response_text)
        if match:
            return float(match.group(1))
        else:
            return 0.0 # Return a default score if no number is found
    except Exception as e:
        print(f"Error grading text answer: {e}")
        return 0.0  # Return a default score in case of an error
