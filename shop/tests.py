from account.models import CustomUser
from .models import (
    Category,
    Inventory,
    Product,
    Discount
)
from django.test import TestCase
from decimal import Decimal


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


class ProductModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='test_user', email='test@example.com')
        self.category = Category.objects.create(name='Test Category')
        self.inventory = Inventory.objects.create(name='Test Inventory', capacity=100)

    def test_create_product(self):

        product = Product.objects.create(
            category=self.category,
            user=self.user,
            inventory=self.inventory,
            name='Test Product',
            about='Test Description',
            quantity=50,
            price=10.99
        )

        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.quantity, 50)
        self.assertEqual(product.price, 10.99)

    def test_read_product(self):

        product = Product.objects.create(
            category=self.category,
            user=self.user,
            inventory=self.inventory,
            name='Test Product',
            about='Test Description',
            quantity=50,
            price=10.99
        )

        retrieved_product = Product.objects.get(name='Test Product')

        self.assertEqual(product, retrieved_product)

    def test_update_product(self):

        product = Product.objects.create(
            category=self.category,
            user=self.user,
            inventory=self.inventory,
            name='Test Product',
            about='Test Description',
            quantity=50,
            price=10.99
        )

        product.name = 'Updated Test Product'
        product.price = 15.99
        product.save()

        updated_product = Product.objects.get(name='Updated Test Product')

        self.assertEqual(updated_product.name, 'Updated Test Product')
        self.assertEqual(updated_product.price, Decimal('15.99'))

    def test_delete_product(self):

        product = Product.objects.create(
            category=self.category,
            user=self.user,
            inventory=self.inventory,
            name='Test Product',
            about='Test Description',
            quantity=50,
            price=10.99
        )

        product.delete()

        # noinspection PyTypeChecker
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(name='Test Product')

        self.assertFalse(product.is_active)
        self.assertTrue(product.is_deleted)


class DiscountModelTest(TestCase):

    def setUp(self):

        category = Category.objects.create(name='Test Category')
        user = CustomUser.objects.create(username='test_user')
        inventory = Inventory.objects.create(name='Test Inventory', capacity=100)

        self.product = Product.objects.create(
            category=category,
            user=user,
            inventory=inventory,
            name='Test Product',
            about='Test Description',
            quantity=50,
            price=10.99
        )

    def test_create_discount(self):

        discount = Discount.objects.create(product=self.product, discount_percentage=20.00)

        self.assertEqual(discount.product.name, 'Test Product')
        self.assertEqual(discount.discount_percentage, 20.00)

    def test_read_discount(self):

        discount = Discount.objects.create(product=self.product, discount_percentage=20.00)

        retrieved_discount = Discount.objects.get(product=self.product)

        self.assertEqual(discount, retrieved_discount)

    def test_update_discount(self):

        discount = Discount.objects.create(product=self.product, discount_percentage=20.00)

        discount.discount_percentage = 30.00
        discount.save()

        updated_discount = Discount.objects.get(product=self.product)

        self.assertEqual(updated_discount.discount_percentage, 30.00)

    def test_delete_discount(self):

        discount = Discount.objects.create(product=self.product, discount_percentage=20.00)

        discount.delete()

        # noinspection PyTypeChecker
        with self.assertRaises(Discount.DoesNotExist):
            Discount.objects.get(product=self.product)
