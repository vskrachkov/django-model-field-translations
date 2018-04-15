from django.test import TestCase
from . import models


class TransTestCase(TestCase):
    def setUp(self):
        content = models.Content.objects.create()
        models.ContentTranslation.objects.create(
            name='Some name',
            full_name='Full name',
            description='Description',
            main_model=content,
            lang='en'
        )

    def tearDown(self):
        models.Content.objects.all().delete()

    def test_translation_retrieve(self):
        # retrieve translation
        q = models.Content.objects.all()
        self.assertEqual(q.count(), 1)
        c = list(q)[0]
        self.assertEqual(c.name, 'Some name')
        self.assertEqual(c.full_name, 'Full name')
        self.assertEqual(c.description, 'Description')
        self.assertEqual(c.lang, 'en')

    def test_translation_update(self):
        # update translation via main model
        q = models.Content.objects.all()
        q.update(name='New name', full_name='New full name')
        c = models.Content.objects.all().first()
        self.assertEqual(c.name, 'New name')
        self.assertEqual(c.full_name, 'New full name')
        self.assertEqual(c.description, 'Description')
        self.assertEqual(c.lang, 'en')

    def test_translation_create(self):
        # create new translation via updating existing content object
        q = models.Content.objects.all()
        q.update(name='Имя', full_name='Полное имя', lang='ru')
        self.assertEqual(models.Content.objects.all().count(), 2)
        c = models.Content.objects.filter(lang='ru').first()
        self.assertEqual(c.name, 'Имя')
        self.assertEqual(c.full_name, 'Полное имя')
        self.assertEqual(c.description, '') # text field is empty by default
        self.assertEqual(c.lang, 'ru')
