from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='testpassword')
    self.login_url = reverse('login')

def test_login_page_status_code(self):
    response = self.client.get(self.login_url)
    self.assertEqual(response.status_code, 200)

def test_login_page_uses_correct_template(self):
    response = self.client.get(self.login_url)
    self.assertTemplateUsed(response, 'paginas/login.html')

def test_login_form(self):
    response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword'})
    self.assertRedirects(response, reverse('inicio'))