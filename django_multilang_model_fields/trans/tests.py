from django.test import TestCase
from . import models


class TransTestCase(TestCase):
    def test_translations(self):
        content = models.Content.objects.create()
        models.ContentTranslation.objects.create(
            name='Some name',
            full_name='Full name',
            description='Description',
            main_model=content,
            lang='en'
        )
        q = models.Content.objects.all()
        self.assertEqual(q.count(), 1)
        content = list(q)[0]
        self.assertEqual(content.name, 'Some name')
        self.assertEqual(content.full_name, 'Full name')
        self.assertEqual(content.description, 'Description')
        self.assertEqual(content.lang, 'en')
