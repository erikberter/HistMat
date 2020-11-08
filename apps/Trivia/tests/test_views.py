from django.test import TestCase

from apps.Trivia.models import *
from apps.Users.models import Profile

DEFAULT_QUIZ_DATA = {
    "quiz_pk" : "",
    "question_number" : ""
    }

AYAX_COM = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

class QuizHomeTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")
        login = self.client.login(username='test_user_1', password='test_pass_1')

        self.user2 = Profile.objects.create_user(username="test_user_2", password="test_pass_2")
        self.user3 = Profile.objects.create_user(username="test_user_3", password="test_pass_2")

        self.quiz_1 = Quiz.objects.create(name="test_quiz_1", status = "publish", user=self.user)
        self.quiz_2 = Quiz.objects.create(name="test_quiz_2", status = "publish", user=self.user2)
        self.quiz_draft_3 = Quiz.objects.create(name="test_quiz_3", status = "draft", user=self.user)

        self.mc_question_1_quiz_1 = MultiChoiceQuestion.objects.create(question="test_question", quiz=self.quiz_1)
        self.mc_question_1_quiz_1_answer_1 = MultiChoiceAnswer.objects.create(answer="test_answer_1", question=self.mc_question_1_quiz_1)
        self.mc_question_1_quiz_1_answer_2 = MultiChoiceAnswer.objects.create(answer="test_answer_2", question=self.mc_question_1_quiz_1)
        self.textquestion_2_quiz_1 = TextQuestion.objects.create(question="test_question_2",quiz=self.quiz_1)
        self.textquestion_2_quiz_2 = TextQuestion.objects.create(question="test_question_3",quiz=self.quiz_2)

    def test_user_returns_200(self):
        pass

    def test_anonymous_returns_200(self):
        pass

    def test_returns_correct_html(self):
        pass

    def test_contains_quizz_logo(self):
        pass

    def test_page_contains_search_bar(self):
        pass

    def test_user_contains_my_quizz_section(self):
        pass
    
    def test_anonymous_not_contains_my_quizz_section(self):
        pass

    def test_contains_popular_quizzes(self):
        pass

    # TODO Change to popular categories by modifying the categories to add visits
    def test_contains_categories(self):
        pass

class QuizListTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")
        login = self.client.login(username='test_user_1', password='test_pass_1')

        self.user2 = Profile.objects.create_user(username="test_user_2", password="test_pass_2")
        self.user3 = Profile.objects.create_user(username="test_user_3", password="test_pass_2")

        self.quiz_1 = Quiz.objects.create(name="test_quiz_1", status = "publish", user=self.user)
        self.quiz_2 = Quiz.objects.create(name="test_quiz_2", status = "publish", user=self.user2)
        self.quiz_draft_3 = Quiz.objects.create(name="test_quiz_3", status = "draft", user=self.user)

        self.mc_question_1_quiz_1 = MultiChoiceQuestion.objects.create(question="test_question", quiz=self.quiz_1)
        self.mc_question_1_quiz_1_answer_1 = MultiChoiceAnswer.objects.create(answer="test_answer_1", question=self.mc_question_1_quiz_1)
        self.mc_question_1_quiz_1_answer_2 = MultiChoiceAnswer.objects.create(answer="test_answer_2", question=self.mc_question_1_quiz_1)
        self.textquestion_2_quiz_1 = TextQuestion.objects.create(question="test_question_2",quiz=self.quiz_1)
        self.textquestion_2_quiz_2 = TextQuestion.objects.create(question="test_question_3",quiz=self.quiz_2)

    def test_user_returns_200(self):
        pass

    def test_anonymous_returns_200(self):
        pass

    def test_returns_correct_html(self):
        pass

    def test_contains_quizz_logo(self):
        pass

    def test_page_contains_search_bar(self):
        pass

class QuizModels(TestCase):

    def setUp(self):
        self.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")
        login = self.client.login(username='test_user_1', password='test_pass_1')

        self.user2 = Profile.objects.create_user(username="test_user_2", password="test_pass_2")
        self.user3 = Profile.objects.create_user(username="test_user_3", password="test_pass_2")

        self.quiz_1 = Quiz.objects.create(name="test_quiz_1", status = "publish", user=self.user)
        self.quiz_2 = Quiz.objects.create(name="test_quiz_2", status = "publish", user=self.user2)
        self.quiz_draft_3 = Quiz.objects.create(name="test_quiz_3", status = "draft", user=self.user)

        self.mc_question_1_quiz_1 = MultiChoiceQuestion.objects.create(question="test_question", quiz=self.quiz_1)
        self.mc_question_1_quiz_1_answer_1 = MultiChoiceAnswer.objects.create(answer="test_answer_1", question=self.mc_question_1_quiz_1)
        self.mc_question_1_quiz_1_answer_2 = MultiChoiceAnswer.objects.create(answer="test_answer_2", question=self.mc_question_1_quiz_1)
        self.textquestion_2_quiz_1 = TextQuestion.objects.create(question="test_question_2",quiz=self.quiz_1)
        self.textquestion_2_quiz_2 = TextQuestion.objects.create(question="test_question_3",quiz=self.quiz_2)


    ### QUIZ LIST ###

    def test_quiz_list_returns_200(self):
        response = self.client.get('/trivia/quiz_list/')
        self.assertEqual(response.status_code, 200)

    def test_quiz_list_contains_publish_quiz(self):
        response = self.client.get('/trivia/quiz_list/')
        self.assertIn("test_quiz_1", response.content.decode())
        self.assertContains(response, "test_quiz_2")

    def test_quiz_list_not_contains_draft_quiz(self):
        response = self.client.get('/trivia/quiz_list/')
        self.assertNotContains(response, "test_quiz_3")

    def test_quiz_list_contains_only_user_with_quiz(self):
        response = self.client.get('/trivia/quiz_list/')
        self.assertContains(response, "test_user_1")
        self.assertContains(response, "test_user_2")
        self.assertNotContains(response, "test_user_3")

    def test_quiz_list_contains_publish_quiz_url(self):
        response = self.client.get('/trivia/quiz_list/')
        self.assertContains(response, self.quiz_1.get_absolute_url())
        self.assertContains(response, self.quiz_2.get_absolute_url())
    
    def test_quiz_list_not_contains_draft_quiz_url(self):
        response = self.client.get('/trivia/quiz_list/')
        self.assertNotContains(response, self.quiz_draft_3.get_absolute_url())
    
    def test_quiz_list_returns_correct_html(self):
        response = self.client.get('/trivia/quiz_list/')
        self.assertTemplateUsed(response, 'Trivia/quiz_list.html')
        self.assertTemplateUsed(response, 'base.html')

    ### QUIZ DETAIL###

    def test_publish_quiz_detail_returns_200(self):
        response = self.client.get(self.quiz_1.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_fake_quiz_detail_returns_404(self):
        response = self.client.get('/trivia/quiz/5/')
        self.assertEqual(response.status_code, 404)

    def test_draft_quiz_detail_returns_404(self):
        response = self.client.get(self.quiz_draft_3.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_quiz_detail_contains_only_user_of_quiz(self):
        response = self.client.get(self.quiz_1.get_absolute_url())
        self.assertContains(response, "test_user_1")
        self.assertNotContains(response, "test_user_2")
        self.assertNotContains(response, "test_user_3")

    def test_quiz_detail_returns_correct_html(self):
        response = self.client.get(self.quiz_1.get_absolute_url())
        self.assertTemplateUsed(response, 'Trivia/quiz_detail.html')
        self.assertTemplateUsed(response, 'base.html')
    
    ###  QUIZ ###

    def test_quiz_returns_200(self):
        response = self.client.get(self.quiz_1.get_questions_url())
        self.assertEqual(response.status_code, 200)

    def test_draft_quiz_returns_404(self):
        response = self.client.get(self.quiz_draft_3.get_questions_url())
        self.assertEqual(response.status_code, 404)

    def test_quiz_returns_correct_html(self):
        response = self.client.get(self.quiz_1.get_questions_url())
        self.assertTemplateUsed(response, 'Trivia/quiz.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_quiz_returns_questions(self):
        data = DEFAULT_QUIZ_DATA.copy()
        data["quiz_pk"] = self.quiz_1.pk
        data["question_number"] = 0

        response = self.client.post(f'/trivia/quiz/{self.quiz_1.pk}/questions/', data, **AYAX_COM)
        self.assertContains(response, self.mc_question_1_quiz_1.question)
        print(response.content.decode())
        self.assertContains(response, self.mc_question_1_quiz_1_answer_1.answer)
        self.assertContains(response, self.mc_question_1_quiz_1_answer_2.answer)

        data["question_number"] = 1
        response = self.client.post(f'/trivia/quiz/{self.quiz_1.pk}/questions/', data, **AYAX_COM)
        self.assertContains(response, self.textquestion_2_quiz_1.question)

    def test_quiz_returns_only_one_questions(self):
        data = DEFAULT_QUIZ_DATA.copy()
        data["quiz_pk"] = self.quiz_1.pk
        data["question_number"] = 0
        response = self.client.post('/trivia/quiz/question/', data, **AYAX_COM)
        self.assertEqual(response.content.decode().count("question-id"), 1)
    
    def test_quiz_without_ajax_no_questions(self):
        response = self.client.get('/trivia/quiz/question/')
        self.assertEqual(response.content.decode().count("question-id"), 0)