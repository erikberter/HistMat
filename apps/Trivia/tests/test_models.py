from django.test import TestCase

from apps.Trivia.models import *
from apps.Users.models import Profile

class QuizModels(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")
        login = self.client.login(username='test_user_1', password='test_pass_1')

    def test_create_quiz(self):
        quiz_test = Quiz.objects.create(name="test_name", user=self.user)
        self.assertEqual(quiz_test.user, self.user)
        self.assertEqual(quiz_test.name,"test_name")
        self.assertEqual(Quiz.objects.count(), 1)
    
    def test_create_multiple_quiz(self):
        quiz_test = Quiz.objects.create(name="test_name", user=self.user)
        quiz_test_1 = Quiz.objects.create(name="test_name_1", user=self.user)
        self.assertEqual(Quiz.objects.count(), 2)
        self.assertEqual(list(Quiz.objects.all()), [quiz_test, quiz_test_1])

class MultipleChoiceModelTest(TestCase):
    
    def setUp(self):
        self.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")
        login = self.client.login(username='test_user_1', password='test_pass_1')

        self.quiz_test = Quiz.objects.create(name="test_name", user=self.user)
        self.quiz_test_1 = Quiz.objects.create(name="test_name_1", user=self.user)
    
    def test_create_mc_question(self):
        mc_question = MultiChoiceQuestion.objects.create(question="test_question", quiz=self.quiz_test)
        self.assertEqual(mc_question.question, "test_question")
        self.assertEqual(MultiChoiceQuestion.objects.count(), 1)
    
    def test_create_multiple_mc_question(self):
        mc_question = MultiChoiceQuestion.objects.create(question="test_question", quiz=self.quiz_test)
        mc_question_1 = MultiChoiceQuestion.objects.create(question="test_question_1", quiz=self.quiz_test_1)
        self.assertEqual(MultiChoiceQuestion.objects.count(), 2)
        self.assertEqual(MultiChoiceQuestion.objects.filter(quiz=self.quiz_test).count(), 1)
        self.assertEqual(list(MultiChoiceQuestion.objects.all()), [mc_question, mc_question_1])

class MultipleChoiceAnswersTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")
        login = self.client.login(username='test_user_1', password='test_pass_1')

        self.quiz_test = Quiz.objects.create(name="test_name", user=self.user)
        self.quiz_test_1 = Quiz.objects.create(name="test_name_1", user=self.user)
        self.mc_question = MultiChoiceQuestion.objects.create(
            question="test_question", quiz=self.quiz_test
            )
        self.mc_question_1 = MultiChoiceQuestion.objects.create(
            question="test_question_1", quiz=self.quiz_test_1
            )

    def test_create_mc_answer(self):
        mc_answer_1_correct = MultiChoiceAnswer.objects.create(
            answer="test_answer_1", question=self.mc_question, is_correct=True
            )
        
        self.assertEqual(MultiChoiceAnswer.objects.count(), 1)
        self.assertEqual(mc_answer_1_correct.answer, "test_answer_1")
        self.assertEqual(mc_answer_1_correct.question, self.mc_question)
        self.assertEqual(mc_answer_1_correct.is_correct, True)
        
        self.assertEqual(list(MultiChoiceAnswer.objects.all()), [mc_answer_1_correct] )

    def test_mc_question_is_answer_correct(self):

        mc_answer_1_correct = MultiChoiceAnswer.objects.create(
            answer="test_answer_1", question=self.mc_question, is_correct=True
            )
        
        mc_answer_2_false = MultiChoiceAnswer.objects.create(
            answer="test_answer_2", question=self.mc_question, is_correct=False
            )
        self.assertTrue(self.mc_question.is_answer_correct({'answer' : mc_answer_1_correct.pk}))
        self.assertFalse(self.mc_question.is_answer_correct({'answer' : mc_answer_2_false.pk}))
        
class TextQuestionTest(TestCase):

    def setUp(self):
        self.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")
        login = self.client.login(username='test_user_1', password='test_pass_1')

        self.quiz_test = Quiz.objects.create(name="test_name", user=self.user)

    def test_create_text_question(self):
        text_question = TextQuestion.objects.create(
            question="test_question", text_answer="test_answer", quiz=self.quiz_test
            )
        self.assertEqual(list(TextQuestion.objects.all()), [text_question])
        self.assertEqual(text_question.question, "test_question")
        self.assertEqual(text_question.text_answer, "test_answer")
        self.assertEqual(text_question.quiz, self.quiz_test)

class TextQuestionAnswerTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")
        login = self.client.login(username='test_user_1', password='test_pass_1')

        self.quiz_test = Quiz.objects.create(name="test_name", user=self.user)
        self.text_question = TextQuestion.objects.create(
            question="test_question", text_answer="test_answer", quiz=self.quiz_test
            )
            
    def test_text_question_is_answer_correct(self):
        self.assertTrue(self.text_question.is_answer_correct({'answer' : "test_answer"}))
    
    def test_text_question_is_answer_incorrect(self):
        self.assertFalse(self.text_question.is_answer_correct({'answer' : "wrong_test_answer"}))

    def test_text_question_is_answer_empty(self):
        self.assertFalse(self.text_question.is_answer_correct({}))

class MultiTypeQuizTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")
        login = self.client.login(username='test_user_1', password='test_pass_1')

        self.quiz_test = Quiz.objects.create(name="test_name", user=self.user)
    
    def test_add_multi_type_question(self):
        text_question = TextQuestion.objects.create(
            question="test_question", text_answer="test_answer", quiz=self.quiz_test
            )
        mc_question = MultiChoiceQuestion.objects.create(
            question="test_question", quiz=self.quiz_test
            )
        mc_answer_1_correct = MultiChoiceAnswer.objects.create(
            answer="test_answer_1", question=mc_question, is_correct=True
            )
        self.assertEqual(
            list(Question.objects.all().values_list('pk', flat=True)),
            [text_question.pk, mc_question.pk]
        )
