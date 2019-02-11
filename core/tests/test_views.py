from django.urls import reverse
from django.test import TestCase


class ViewsTest(TestCase):
    def test_correct_response(self):
        url = reverse('core:home')

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'core/home.html')
