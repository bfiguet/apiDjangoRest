from unittest import mock
from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from shop.models import Category, Product
from shop.mocks import mock_openfoodfact_success, ECOSCORE_GRADE

class ShopAPITestCase(APITestCase):
	@classmethod
	def setUpTestData(cls):
		# Créons deux catégories dont une seule est active
		cls.category = Category.objects.create(name='Fruits', active=True)
		Category.objects.create(name='Légumes', active=False)

		cls.product = cls.category.products.create(name='Ananas', active=True)
		cls.category.products.create(name='Banane', active=False)

		cls.category_2 = Category.objects.create(name='Légumes', active=True)
		cls.product_2 = cls.category_2.products.create(name='Tomate', active=True)

	def format_datetime(self, value):
    	return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
	
	def get_article_list_data(self, articles):
        return [
            {
                'id': article.pk,
                'name': article.name,
                'date_created': self.format_datetime(article.date_created),
                'date_updated': self.format_datetime(article.date_updated),
                'product': article.product_id
            } for article in articles
        ]

    def get_product_list_data(self, products):
        return [
            {
                'id': product.pk,
                'name': product.name,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'category': product.category_id,
                'articles': self.get_article_list_data(product.articles.filter(active=True))
            } for product in products
        ]

    def get_category_list_data(self, categories):
        return [
            {
                'id': category.id,
                'name': category.name,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated),
            } for category in categories
        ]

	#def get_product_detail_data(self, product):
	#	return {
	#		'id': product.pk,
	#		'name':product.name, 
	#		'date_created': self.format_datetime(product.date_created),
	#		'date_updated': self.format_datetime(product.date_updated),
	#		'category': product.category_id,
	#		'articles': self.get_article_detail_data(product.articles.filter(active=True)),
	#		'ecoscore': ECOSCORE_GRADE
	#	}

class TestCategory(ShopAPITestCase):
	 # stocker url endpoint dans attribut classe
	url = reverse_lazy('category-list')

	def test_line(self):
		# On réalise l’appel en GET en utilisant le client de la classe de test
		response = self.client.get(self.url)
		
		# Nous vérifions que le status code est bien 200
        # et que les valeurs retournées sont bien celles attendues
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['results'], self.get_category_list_data([self.category, self.category_2]))

	def test_created(self):
		# Nous vérifions qu’aucune catégorie n'existe avant de tenter d’en créer une
		category_count = Category.objects.count()
		response = self.client.post(self.url, data={'name': 'Nouvelle categorie'})
		
		# Vérifions que le status code est bien en erreur et nous empêche de créer une catégorie
		self.assertEqual(response.status_code, 405)

		 # Enfin, vérifions qu'aucune nouvelle catégorie n’a été créée malgré le status code 405
		self.assertEqual(Category.objects.count(), category_count)

class testProduct(ShopAPITestCase):
	url = reverse_lazy('product-list')

	#@mock.patch('shop.models.Product.call_external_api', mock_openfoodfact_success)
	#def test_detail(self):
	#	response = self.client.get(reverse('product-detail', kwargs={'pk': self.product.pk}))
	#	self.assertEqual(response.status_code, 200)
	#	self.assertEqual(self.get_product_detail_data(self.product), response,json())

	@mock.patch('shop.models.Product.call_external_api', mock_openfoodfact_success)
	def test_list(self):
		response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_list_data([self.product, self.product_2]), response.json()['results'])

	@mock.patch('shop.models.Product.call_external_api', mock_openfoodfact_success)
	def test_list_filter(self):
		response = self.client.get(self.url + '?category_id=%i' % self.category.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_list_data([self.product]), response.json()['results'])

	def test_create(self):
		product_count = Product.objects.count()
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Product.objects.count(), product_count)

	def test_delete(self):
		response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 405)
        self.product.refresh_from_db()
