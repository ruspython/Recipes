from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from recipe.models import Recipe
from django.contrib.sites.models import Site
from django.contrib.flatpages.models import FlatPage


class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()


class RecipeTest(TestCase):
    def test_create_recipe(self):
        recipe = Recipe()
        recipe.title = 'Recipechik'
        recipe.text = 'Some text'
        recipe.timestamp = timezone.now()

        recipe.save()

        all_recipes = Recipe.objects.all()
        the_recipe = Recipe.objects.get(id=recipe.id)
        self.assertEqual(the_recipe.text, recipe.text)


class AdminTest(BaseAcceptanceTest):
    def test_login(self):
        response = self.client.get('/admin/')
        self.client.login(username='vlad', password='123')
        self.assertEqual(response.status_code, 302)


class FlatePageTest(BaseAcceptanceTest):
    def test_create_flat_page(self):
        page = FlatPage()
        page.url = '/about/'
        page.title = 'About me'
        page.content = 'Some words about me and this not perfect world'
        page.save()

        page.sites.add(Site.objects.all()[0])
        page.save()

        all_pages = FlatPage.objects.all()
        self.assertEqual(len(all_pages), 1)
        only_page = all_pages[0]
        self.assertEqual(only_page, page)

        self.assertEqual(only_page.url, '/about/')
        self.assertEqual(only_page.title, 'About me')
        self.assertEqual(only_page.content, page.content)

        page_url = only_page.get_absolute_url()

        response = self.client.get(page_url)
        self.assertEqual(response.status_code, 200)



