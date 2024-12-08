from django.test import TestCase
from products.models import Product, Category
class ProductCreationTestCase(TestCase):
    def setUp(self):
        """Set up any initial conditions for the tests."""
        # Any pre-test setup (if needed) goes here. For example:
        # self.user = User.objects.create_user('username', 'password')
        self.category = Category.objects.create(name='Electronics')
        

    def test_create_product(self):
        """Test creating a product in the database."""
        product_data = {
            'name': 'Test Product',
            'description': 'This is a test product',
            'price': 19.99,
            'discount_price': 300,
            'category': self.category,
            'rating': 4,
            'stock': 40,
            'status': 1
        }

        product = Product.objects.create(**product_data)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.category.name, 'Electronics')