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
        
    def test_user_returns_200(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_returns_correct_html(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'Trivia/home.html')
        self.assertTemplateUsed(response, 'Trivia/base.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_contains_quiz_logo(self):
        response = self.client.get(self.url)
        self.assertContains(response, "quiz-logo")

    def test_page_contains_search_bar(self):
        response = self.client.get(self.url)
        self.assertContains(response, "quiz-search-bar")

    def test_page_search_redirects_to_search(self):
        pass

    def test_user_contains_my_quiz_section(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url)
        self.assertContains(response, "my-quiz-section")

    def test_user_contains_my_quiz_contains_create_quiz(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url)
        self.assertContains(response, "Create Quiz")
        self.assertContains(response, "quiz/create/")

    def test_user_my_quiz_redirects_to_my_quiz(self):
        pass
    
    def test_anonymous_not_contains_my_quiz_section(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "my-quiz-section")

    def test_contains_popular_quizes(self):
        response = self.client.get(self.url)
        self.assertContains(response, "popular-quiz-section")

    def test_contains_popular_categories(self):
        response = self.client.get(self.url)
        self.assertContains(response, "popular-category-section")
    
    def test_contains_quiz(self):
        response = self.client.get(self.url)
        self.assertContains(response, "test_quiz_1")

    def test_not_contains_draft_quiz_for_non_user(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "test_quiz_3")

    def test_contains_draft_quiz_for_user(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url)
        self.assertContains(response, "test_quiz_3")

    def test_contains_quiz_url(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url)
        self.assertContains(response, self.quiz_1.get_absolute_url())

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

    def test_empty_search_print_empty_message(self):
        pass

    def test_contains_quiz(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url)
        self.assertContains(response, self.quiz_1.get_absolute_url())
        self.assertContains(response, self.quiz_1.name)

    def test_not_contains_quiz_draft(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url)
        self.assertNotContains(response, self.quiz_draft_3.name)

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

    def test_contains_create_button(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url)
        self.assertContains(response, "btn-create-quiz")

    def test_contains_form(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url)
        self.assertContains(response, "form")
        self.assertContains(response, 'id="id_name"')
        self.assertContains(response, 'id="id_description"')
        
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

    def test_contains_delete_button(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertContains(response, "btn-delete-quiz")

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

    def test_fake_quiz_anonymous_returns_404(self):
        response = self.client.get(self.url % ('123456789'))
        self.assertEqual(response.status_code, 302)

    def test_returns_correct_html(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertTemplateUsed(response, 'Trivia/Quiz/confirm_delete.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_contains_quiz_name(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertContains(response, self.quiz_1.name)
    
    def test_contains_confirm_delete_button(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.url % (self.quiz_1.slug))
        self.assertContains(response, "btn-confirm-delete")

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

    def test_quiz_get_absolute_returns_200(self):
        login = self.client.login(username='test_user_1', password='test_pass_1')
        response = self.client.get(self.quiz_1.get_absolute_url())
        self.assertEqual(response.status_code, 200)

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
