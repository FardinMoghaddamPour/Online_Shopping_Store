from django.test import TestCase
from .models import (
    Category,
    Inventory
)


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


class InventoryModelTest(TestCase):

    def test_create_inventory(self):

        inventory = Inventory.objects.create(name='Test Inventory', capacity=100)

        self.assertEqual(inventory.name, 'Test Inventory')
        self.assertEqual(inventory.capacity, 100)

    def test_read_inventory(self):

        inventory = Inventory.objects.create(name='Test Inventory', capacity=100)

        retrieved_inventory = Inventory.objects.get(name='Test Inventory')

        self.assertEqual(inventory, retrieved_inventory)

    def test_update_inventory(self):

        inventory = Inventory.objects.create(name='Test Inventory', capacity=100)

        inventory.name = 'Updated Test Inventory'
        inventory.capacity = 200
        inventory.save()

        updated_inventory = Inventory.objects.get(name='Updated Test Inventory')

        self.assertEqual(updated_inventory.name, 'Updated Test Inventory')
        self.assertEqual(updated_inventory.capacity, 200)

    def test_delete_inventory(self):

        inventory = Inventory.objects.create(name='Test Inventory', capacity=100)

        inventory.delete()

        # noinspection PyTypeChecker
        with self.assertRaises(Inventory.DoesNotExist):
            Inventory.objects.get(name='Test Inventory')
