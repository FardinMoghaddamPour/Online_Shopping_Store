from account.models import (
    CustomUser,
    Address
)
from .models import (
    Category,
    Inventory,
    Product,
    Discount,
    Order,
    OrderItem,
    Coupon,
    Cart,
    Wishlist
)
from django.core.exceptions import ValidationError
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


class OrderModelTest(TestCase):

    def test_create_order(self):

        order = Order.objects.create(total_price=50.00)

        self.assertIsNotNone(order)
        self.assertEqual(order.total_price, 50.00)

    def test_read_order(self):

        order = Order.objects.create(total_price=50.00)

        retrieved_order = Order.objects.get(id=order.id)

        self.assertEqual(order, retrieved_order)

    def test_update_order(self):

        order = Order.objects.create(total_price=50.00)

        order.total_price = 60.00
        order.save()

        updated_order = Order.objects.get(id=order.id)

        self.assertEqual(updated_order.total_price, 60.00)

    def test_delete_order(self):

        order = Order.objects.create(total_price=50.00)

        order.delete()

        # noinspection PyTypeChecker
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(id=order.id)


class OrderItemModelTest(TestCase):

    def setUp(self):

        category = Category.objects.create(name='Test Category')
        user = CustomUser.objects.create(username='test-user', email='test@example.com')
        inventory = Inventory.objects.create(name='Test Inventory', capacity=100)

        self.product = Product.objects.create(
            category=category,
            user=user,
            inventory=inventory,
            name='Test Product',
            about='Test Description',
            quantity=10,
            price=20.00
        )
        self.order = Order.objects.create(total_price=0)

    def test_create_order_item(self):

        order_item = OrderItem.objects.create(product=self.product, order=self.order, quantity=2)

        self.assertIsNotNone(order_item)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, 40.00)

    def test_read_order_item(self):

        order_item = OrderItem.objects.create(product=self.product, order=self.order, quantity=2)

        retrieved_order_item = OrderItem.objects.get(id=order_item.id)

        self.assertEqual(order_item, retrieved_order_item)

    def test_update_order_item(self):

        order_item = OrderItem.objects.create(product=self.product, order=self.order, quantity=2)

        order_item.quantity = 3
        order_item.save()

        updated_order_item = OrderItem.objects.get(id=order_item.id)

        self.assertEqual(updated_order_item.quantity, 3)
        self.assertEqual(updated_order_item.price, 60.00)

    def test_delete_order_item(self):

        order_item = OrderItem.objects.create(product=self.product, order=self.order, quantity=2)

        order_item.delete()

        # noinspection PyTypeChecker
        with self.assertRaises(OrderItem.DoesNotExist):
            OrderItem.objects.get(id=order_item.id)

    def test_save_order_item_insufficient_quantity(self):

        with self.assertRaises(ValidationError):
            OrderItem.objects.create(product=self.product, order=self.order, quantity=20)


class CouponModelTest(TestCase):
    def setUp(self):

        self.coupon_data = {
            'amount_of_discount': 50,
        }

    def test_create_coupon(self):

        coupon = Coupon.objects.create(**self.coupon_data)
        self.assertTrue(isinstance(coupon, Coupon))

    def test_coupon_code_generation(self):

        coupon = Coupon.objects.create(**self.coupon_data)
        self.assertIsNotNone(coupon.coupon_code)

    def test_coupon_amount_range(self):

        coupon_data = {
            'amount_of_discount': 1000001,
        }
        with self.assertRaises(ValidationError):
            Coupon.objects.create(**coupon_data)

    def test_coupon_rarity_assignment(self):

        rarity_mapping = {
            5: 'Common',
            50: 'Uncommon',
            500: 'Rare',
            5000: 'Epic',
            50000: 'Legendary'
        }
        for amount, rarity in rarity_mapping.items():
            coupon_data = {'amount_of_discount': amount}

            coupon = Coupon.objects.create(**coupon_data)
            self.assertEqual(coupon.rarity, rarity)

    def test_read_coupon(self):

        coupon = Coupon.objects.create(**self.coupon_data)
        retrieved_coupon = Coupon.objects.get(id=coupon.id)
        self.assertEqual(coupon, retrieved_coupon)

    def test_update_coupon(self):

        coupon = Coupon.objects.create(**self.coupon_data)
        new_discount_amount = 75
        coupon.amount_of_discount = new_discount_amount
        coupon.save()
        updated_coupon = Coupon.objects.get(id=coupon.id)
        self.assertEqual(updated_coupon.amount_of_discount, new_discount_amount)

    def test_delete_coupon(self):

        coupon = Coupon.objects.create(**self.coupon_data)
        coupon_id = coupon.id

        coupon.delete()

        # noinspection PyTypeChecker
        with self.assertRaises(Coupon.DoesNotExist):
            Coupon.objects.get(id=coupon_id)


class CartModelTest(TestCase):

    def setUp(self):

        self.seller_user = CustomUser.objects.create(
            username='seller',
            email='seller@example.com',
            phone_number='+989393214333',
            password='Strong_123_password'
        )

        self.buyer_user = CustomUser.objects.create(
            username='buyer',
            email='buyer@example.com',
            phone_number='+989165412191',
            password='Strong_123_password'
        )

        self.buyer_address = Address.objects.create(
            user=self.buyer_user,
            country='Test Country',
            city='Test City',
            address='123 Test St',
            zipcode='12345',
            is_active=True
        )

        self.category = Category.objects.create(name='Test Category')
        self.inventory = Inventory.objects.create(name='Test Inventory', capacity=100)

        self.coupon = Coupon.objects.create(
            amount_of_discount=10
        )

        self.product = Product.objects.create(
            name='Test Product',
            price=50,
            quantity=20,
            category=self.category,
            inventory=self.inventory,
            user=self.seller_user
        )

        self.order = Order.objects.create(total_price=100)
        self.order_item = OrderItem.objects.create(product=self.product, order=self.order, quantity=2, price=100)

    def test_create_cart(self):

        cart = Cart.objects.create(
            custom_user=self.buyer_user,
            order=self.order,
            address=self.buyer_address,
            coupon=self.coupon,
            quantity=2,
            total_price=100
        )

        self.assertTrue(isinstance(cart, Cart))

    def test_calculate_total_price(self):

        cart = Cart.objects.create(
            custom_user=self.buyer_user,
            order=self.order,
            address=self.buyer_address,
            coupon=self.coupon,
            quantity=2,
            total_price=100
        )

        cart.calculate_total_price()

        self.assertEqual(cart.total_price, 90)

    def test_save_cart_decrease_product_quantity(self):

        initial_quantity = self.product.quantity

        cart = Cart.objects.create(
            custom_user=self.buyer_user,
            order=self.order,
            address=self.buyer_address,
            coupon=self.coupon,
            total_price=100,
            is_active=True
        )

        cart.save()

        cart.is_active = False
        cart.save()

        updated_product = Product.objects.get(id=self.product.id)

        self.assertFalse(cart.is_active)

        self.assertEqual(updated_product.quantity, initial_quantity - self.order_item.quantity)


class WishlistTestCase(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = CustomUser.objects.create(username='test-user', email='test@example.com')

    def test_create_wishlist(self):

        wishlist = Wishlist.objects.create(user=self.user, name='Test Wishlist')

        saved_wishlist = Wishlist.objects.get(id=wishlist.id)

        self.assertEqual(saved_wishlist.name, 'Test Wishlist')
        self.assertEqual(saved_wishlist.user, self.user)

    def test_read_wishlist(self):

        wishlist = Wishlist.objects.create(user=self.user, name='Test Wishlist')

        retrieved_wishlist = Wishlist.objects.get(id=wishlist.id)

        self.assertEqual(retrieved_wishlist.name, 'Test Wishlist')
        self.assertEqual(retrieved_wishlist.user, self.user)

    def test_update_wishlist(self):

        wishlist = Wishlist.objects.create(user=self.user, name='Test Wishlist')

        wishlist.name = 'Updated Wishlist'
        wishlist.save()

        updated_wishlist = Wishlist.objects.get(id=wishlist.id)

        self.assertEqual(updated_wishlist.name, 'Updated Wishlist')

    def test_delete_wishlist(self):

        wishlist = Wishlist.objects.create(user=self.user, name='Test Wishlist')

        wishlist.delete()

        # noinspection PyTypeChecker
        with self.assertRaises(Wishlist.DoesNotExist):
            Wishlist.objects.get(id=wishlist.id)
