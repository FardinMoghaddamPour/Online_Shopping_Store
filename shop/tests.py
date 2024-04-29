from django.test import TestCase
from .models import Category


class CategoryModelTest(TestCase):

    def test_create_category(self):

        category = Category.objects.create(name='Test Category')

        self.assertEqual(category.name, 'Test Category')

    def test_read_category(self):

        category = Category.objects.create(name='Test Category')

        retrieved_category = Category.objects.get(name='Test Category')

        self.assertEqual(category, retrieved_category)

    def test_update_category(self):

        category = Category.objects.create(name='Test Category')

        category.name = 'Updated Test Category'
        category.save()

        updated_category = Category.objects.get(name='Updated Test Category')

        self.assertEqual(updated_category.name, 'Updated Test Category')

    def test_delete_category(self):

        category = Category.objects.create(name='Test Category')

        category.delete()

        # noinspection PyTypeChecker
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(name='Test Category')
