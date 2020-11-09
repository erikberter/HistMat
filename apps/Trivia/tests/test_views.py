from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

from apps.Trivia.models import *
from apps.Trivia.views import * 

from apps.Users.models import Profile


DEFAULT_QUIZ_DATA = {
    "quiz_pk" : "",
    "question_number" : ""
    }

AYAX_COM = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}


# TODO add context check
# https://docs.djangoproject.com/en/3.1/topics/testing/advanced/

class QuizHomeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")

        cls.url = '/trivia/home/'

        cls.user2 = Profile.objects.create_user(username="test_user_2", password="test_pass_2")
        cls.user3 = Profile.objects.create_user(username="test_user_3", password="test_pass_2")

        cls.quiz_1 = Quiz.objects.create(name="test_quiz_1", status = "publish", creator=cls.user)
        cls.quiz_2 = Quiz.objects.create(name="test_quiz_2", status = "publish", creator=cls.user2)
        cls.quiz_draft_3 = Quiz.objects.create(name="test_quiz_3", status = "draft", creator=cls.user)

        cls.mc_question_1_quiz_1 = MultiChoiceQuestion.objects.create(question="test_question", quiz=cls.quiz_1)
        cls.mc_question_1_quiz_1_answer_1 = MultiChoiceAnswer.objects.create(answer="test_answer_1", question=cls.mc_question_1_quiz_1)
        cls.mc_question_1_quiz_1_answer_2 = MultiChoiceAnswer.objects.create(answer="test_answer_2", question=cls.mc_question_1_quiz_1)
        cls.textquestion_2_quiz_1 = TextQuestion.objects.create(question="test_question_2",quiz=cls.quiz_1)
        cls.textquestion_2_quiz_2 = TextQuestion.objects.create(question="test_question_3",quiz=cls.quiz_2)


    def setUp(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')

        
    def test_user_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_returns_200(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        response = QuizHomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_returns_correct_html(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'Trivia/home.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_contains_quiz_logo(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Diamat quiz")

    def test_page_contains_search_bar(self):
        pass

    def test_page_search_redirects_to_search(self):
        pass

    def test_user_contains_my_quiz_section(self):
        pass

    def test_user_my_quiz_redirects_to_my_quiz(self):
        pass
    
    def test_anonymous_not_contains_my_quiz_section(self):
        pass

    def test_contains_popular_quizes(self):
        pass
    
    def test_contains_quiz(self):
        response = self.client.get(self.url)
        self.assertContains(response, "test_quiz_1")

    def test_not_contains_draft_quiz(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "test_quiz_3")

    def test_contains_quiz_url(self):
        pass

    # TODO Change to popular categories by modifying the categories to add visits
    def test_contains_categories(self):
        pass

class QuizListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")

        cls.url = '/trivia/quiz/list/'

        cls.user2 = Profile.objects.create_user(username="test_user_2", password="test_pass_2")
        cls.user3 = Profile.objects.create_user(username="test_user_3", password="test_pass_2")

        cls.quiz_1 = Quiz.objects.create(name="test_quiz_1", status = "publish", creator=cls.user)
        cls.quiz_2 = Quiz.objects.create(name="test_quiz_2", status = "publish", creator=cls.user2)
        cls.quiz_draft_3 = Quiz.objects.create(name="test_quiz_3", status = "draft", creator=cls.user)

        cls.mc_question_1_quiz_1 = MultiChoiceQuestion.objects.create(question="test_question", quiz=cls.quiz_1)
        cls.mc_question_1_quiz_1_answer_1 = MultiChoiceAnswer.objects.create(answer="test_answer_1", question=cls.mc_question_1_quiz_1)
        cls.mc_question_1_quiz_1_answer_2 = MultiChoiceAnswer.objects.create(answer="test_answer_2", question=cls.mc_question_1_quiz_1)
        cls.textquestion_2_quiz_1 = TextQuestion.objects.create(question="test_question_2",quiz=cls.quiz_1)
        cls.textquestion_2_quiz_2 = TextQuestion.objects.create(question="test_question_3",quiz=cls.quiz_2)


    def setUp(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')

    def test_user_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_returns_200(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        response = QuizListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_returns_correct_html(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'Trivia/Quiz/list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_contains_quiz_logo(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Diamat quiz")

    def test_page_contains_search_bar(self):
        pass

    def test_returns_correct_quiz_by_search(self):
        pass

    def test_does_not_return_invalid_quiz_by_search(self):
        pass

    def test_contains_mode_selector(self):
        pass


class QuizCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")

        cls.url = '/trivia/quiz/create/'

        cls.user2 = Profile.objects.create_user(username="test_user_2", password="test_pass_2")
        cls.user3 = Profile.objects.create_user(username="test_user_3", password="test_pass_2")

        cls.quiz_1 = Quiz.objects.create(name="test_quiz_1", status = "publish", creator=cls.user)
        cls.quiz_2 = Quiz.objects.create(name="test_quiz_2", status = "publish", creator=cls.user2)
        cls.quiz_draft_3 = Quiz.objects.create(name="test_quiz_3", status = "draft", creator=cls.user)

        cls.mc_question_1_quiz_1 = MultiChoiceQuestion.objects.create(question="test_question", quiz=cls.quiz_1)
        cls.mc_question_1_quiz_1_answer_1 = MultiChoiceAnswer.objects.create(answer="test_answer_1", question=cls.mc_question_1_quiz_1)
        cls.mc_question_1_quiz_1_answer_2 = MultiChoiceAnswer.objects.create(answer="test_answer_2", question=cls.mc_question_1_quiz_1)
        cls.textquestion_2_quiz_1 = TextQuestion.objects.create(question="test_question_2",quiz=cls.quiz_1)
        cls.textquestion_2_quiz_2 = TextQuestion.objects.create(question="test_question_3",quiz=cls.quiz_2)

    def test_user_returns_200(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_returns_302(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
    
    def test_returns_correct_html(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'Trivia/Quiz/create.html')
        self.assertTemplateUsed(response, 'base.html')

class QuizUpdateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")

        cls.url = '/trivia/quiz/%s/update/'

        cls.user2 = Profile.objects.create_user(username="test_user_2", password="test_pass_2")
        cls.user3 = Profile.objects.create_user(username="test_user_3", password="test_pass_2")

        cls.quiz_1 = Quiz.objects.create(name="test_quiz_1", status = "publish", creator=cls.user)
        cls.quiz_2 = Quiz.objects.create(name="test_quiz_2", status = "publish", creator=cls.user2)
        cls.quiz_draft_3 = Quiz.objects.create(name="test_quiz_3", status = "draft", creator=cls.user)

        cls.mc_question_1_quiz_1 = MultiChoiceQuestion.objects.create(question="test_question", quiz=cls.quiz_1)
        cls.mc_question_1_quiz_1_answer_1 = MultiChoiceAnswer.objects.create(answer="test_answer_1", question=cls.mc_question_1_quiz_1)
        cls.mc_question_1_quiz_1_answer_2 = MultiChoiceAnswer.objects.create(answer="test_answer_2", question=cls.mc_question_1_quiz_1)
        cls.textquestion_2_quiz_1 = TextQuestion.objects.create(question="test_question_2",quiz=cls.quiz_1)
        cls.textquestion_2_quiz_2 = TextQuestion.objects.create(question="test_question_3",quiz=cls.quiz_2)

    def test_user_returns_200(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertEqual(response.status_code, 200)

    def test_fake_quiz_user_returns_404(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % ('123456789'))
        self.assertEqual(response.status_code, 404)

    def test_anonymous_returns_302(self):
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertEqual(response.status_code, 302)
    
    def test_fake_quiz_anonymous_returns_302(self):
        response = self.client.get(self.url % ('123456789'))
        self.assertEqual(response.status_code, 302)

    def test_returns_correct_html(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertTemplateUsed(response, 'Trivia/Quiz/update.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_contains_quiz_data(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertContains(response, self.quiz_1.name)
        self.assertContains(response, self.quiz_1.creator)
        self.assertContains(response, self.quiz_1.description)

    def test_contains_correct_fields(self):
        pass

class QuizDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")

        cls.url = '/trivia/quiz/%s/confirm_delete/'

        cls.user2 = Profile.objects.create_user(username="test_user_2", password="test_pass_2")
        cls.user3 = Profile.objects.create_user(username="test_user_3", password="test_pass_2")

        cls.quiz_1 = Quiz.objects.create(name="test_quiz_1", status = "publish", creator=cls.user)
        cls.quiz_2 = Quiz.objects.create(name="test_quiz_2", status = "publish", creator=cls.user2)
        cls.quiz_draft_3 = Quiz.objects.create(name="test_quiz_3", status = "draft", creator=cls.user)

        cls.mc_question_1_quiz_1 = MultiChoiceQuestion.objects.create(question="test_question", quiz=cls.quiz_1)
        cls.mc_question_1_quiz_1_answer_1 = MultiChoiceAnswer.objects.create(answer="test_answer_1", question=cls.mc_question_1_quiz_1)
        cls.mc_question_1_quiz_1_answer_2 = MultiChoiceAnswer.objects.create(answer="test_answer_2", question=cls.mc_question_1_quiz_1)
        cls.textquestion_2_quiz_1 = TextQuestion.objects.create(question="test_question_2",quiz=cls.quiz_1)
        cls.textquestion_2_quiz_2 = TextQuestion.objects.create(question="test_question_3",quiz=cls.quiz_2)


    def setUp(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')

    def test_user_returns_200(self):
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertEqual(response.status_code, 200)

    def test_fake_quiz_user_returns_404(self):
        response = self.client.get(self.url % ('123456789'))
        self.assertEqual(response.status_code, 404)

    def test_anonymous_returns_302(self):
        request = self.factory.get(self.url % (self.quiz_1.slug))
        request.user = AnonymousUser()
        response = QuizDeleteView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_fake_quiz_anonymous_returns_404(self):
        request = self.factory.get(self.url % ('123456789'))
        request.user = AnonymousUser()
        response = QuizDeleteView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_returns_correct_html(self):
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertTemplateUsed(response, 'Trivia/Quiz/confirm_delete.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_contains_quiz_name(self):
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertContains(response, self.quiz_1.name)
    
    def test_contains_quiz_logo(self):
        pass


class QuizDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")

        cls.url = '/trivia/quiz/%s/detail/'

        cls.user2 = Profile.objects.create_user(username="test_user_2", password="test_pass_2")
        cls.user3 = Profile.objects.create_user(username="test_user_3", password="test_pass_2")

        cls.quiz_1 = Quiz.objects.create(name="test_quiz_1", status = "publish", creator=cls.user)
        cls.quiz_2 = Quiz.objects.create(name="test_quiz_2", status = "publish", creator=cls.user2)
        cls.quiz_draft_3 = Quiz.objects.create(name="test_quiz_3", status = "draft", creator=cls.user)

        cls.mc_question_1_quiz_1 = MultiChoiceQuestion.objects.create(question="test_question", quiz=cls.quiz_1)
        cls.mc_question_1_quiz_1_answer_1 = MultiChoiceAnswer.objects.create(answer="test_answer_1", question=cls.mc_question_1_quiz_1)
        cls.mc_question_1_quiz_1_answer_2 = MultiChoiceAnswer.objects.create(answer="test_answer_2", question=cls.mc_question_1_quiz_1)
        cls.textquestion_2_quiz_1 = TextQuestion.objects.create(question="test_question_2",quiz=cls.quiz_1)
        cls.textquestion_2_quiz_2 = TextQuestion.objects.create(question="test_question_3",quiz=cls.quiz_2)

    def test_user_returns_200(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertEqual(response.status_code, 200)

    def test_fake_quiz_user_returns_404(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % ('123456789'))
        self.assertEqual(response.status_code, 404)

    def test_anonymous_returns_200(self):
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertEqual(response.status_code, 200)

    def test_fake_quiz_anonymous_returns_404(self):
        response = self.client.get(self.url % ('123456789'))
        self.assertEqual(response.status_code, 404)

    def test_returns_correct_html(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertTemplateUsed(response, 'Trivia/Quiz/detail.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_contains_quiz_details(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertContains(response, self.quiz_1.name)
        self.assertContains(response, self.quiz_1.creator)
        self.assertContains(response, self.quiz_1.description)

    def test_contains_play_button(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertContains(response, "quiz-play-button")
        # TODO Add check for functionality

    def test_contains_leaderboard(self):
        pass

    def test_contains_last_played(self):
        pass


class QuizPlayTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")

        cls.url = '/trivia/quiz/%s/play/'

        cls.user2 = Profile.objects.create_user(username="test_user_2", password="test_pass_2")
        cls.user3 = Profile.objects.create_user(username="test_user_3", password="test_pass_2")

        cls.quiz_1 = Quiz.objects.create(name="test_quiz_1", status = "publish", creator=cls.user)
        cls.quiz_2 = Quiz.objects.create(name="test_quiz_2", status = "publish", creator=cls.user2)
        cls.quiz_draft_3 = Quiz.objects.create(name="test_quiz_3", status = "draft", creator=cls.user)

        cls.mc_question_1_quiz_1 = MultiChoiceQuestion.objects.create(question="test_question", quiz=cls.quiz_1)
        cls.mc_question_1_quiz_1_answer_1 = MultiChoiceAnswer.objects.create(answer="test_answer_1", question=cls.mc_question_1_quiz_1)
        cls.mc_question_1_quiz_1_answer_2 = MultiChoiceAnswer.objects.create(answer="test_answer_2", question=cls.mc_question_1_quiz_1)
        cls.textquestion_2_quiz_1 = TextQuestion.objects.create(question="test_question_2",quiz=cls.quiz_1)
        cls.textquestion_2_quiz_2 = TextQuestion.objects.create(question="test_question_3",quiz=cls.quiz_2)
        

    def test_user_returns_200(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertEqual(response.status_code, 200)

    def test_fake_quiz_user_returns_404(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % ('123456789'))
        self.assertEqual(response.status_code, 404)

    def test_anonymous_returns_200(self):
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertEqual(response.status_code, 200)

    def test_fake_quiz_anonymous_returns_404(self):
        response = self.client.get(self.url % ('123456789'))
        self.assertEqual(response.status_code, 404)

    def test_returns_correct_html(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertTemplateUsed(response, 'Trivia/Quiz/play.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_contains_quiz_name(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertContains(response, self.quiz_1.name)

    def test_contains_question(self):
        pass

    def test_contains_question_answer_input(self):
        pass

    def test_contains_next_button(self):
        pass

    def test_contains_back_button(self):
        pass

"""
class QuizModels(TestCase):

    def setUp(self):
        self.user = Profile.objects.create_user(username="test_user_1", password="test_pass_1")
        login = self.client.login(username='test_user_1', password='test_pass_1')

        self.user2 = Profile.objects.create_user(username="test_user_2", password="test_pass_2")
        self.user3 = Profile.objects.create_user(username="test_user_3", password="test_pass_2")

        self.quiz_1 = Quiz.objects.create(name="test_quiz_1", status = "publish", creator=self.user)
        self.quiz_2 = Quiz.objects.create(name="test_quiz_2", status = "publish", creator=self.user2)
        self.quiz_draft_3 = Quiz.objects.create(name="test_quiz_3", status = "draft", creator=self.user)

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

"""