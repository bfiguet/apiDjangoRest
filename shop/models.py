import requests
from django.db import models, transaction


class Category(models.Model):

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	active = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	@transaction.atomic
	def disable(self):
		if self.active is False:
		# do nothing if categorie is not activate
			return
		self.active = False
		self.save()
		self.products.update(active=False)

	
class Product(models.Model):

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	active = models.BooleanField(default=False)

	category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, related_name='products')

	def __str__(self):
		return self.name

	@transaction.atomic
	def disable(self):
		if self.active is False:
			return
		self.active = False
		self.save()
		self.articles.update(active=False)

	def call_externam_api(self, method, url):
		# l'appel doit être le plus petit possible car appliquer un mock va réduire la couverture de tests
		# C'est cette méthode qui va être monkey patchée
		return requests.request(method, url)

	@property
	def ecoscore(self):
		#appel a open food fact
		response = self.call_externam_api('GET', 'https://world.openfoodfacts.org/api/v0/product/3229820787015.json')
		if response.status_code == 200:
			return response.json()['product']['ecoscore_grade']



class Article(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.name
