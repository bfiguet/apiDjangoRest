from rest_framework import serializers
from shop.models import Category, Product, Article

class CategoryListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'date_created', 'date_updated','name']

	def validate_name(self, value):
		if Category.objects.filter(name=value).exists():
			raise serializers.ValidationError('Category already exists')
		return value

	def validate(self, data):
		if data['name'] not in data['description']:
			raise serializers.ValidationError('Name must be in description')
		return data

class CategoryDetailSerializer(serializers.ModelSerializer):
	 # En utilisant un `SerializerMethodField', il est nécessaire d'écrire une méthode
    # nommée 'get_XXX' où XXX est le nom de l'attribut, ici 'products'
	products = serializers.SerializerMethodField()

	class Meta:
		model = Category
		fields = ['id', 'date_created', 'date_updated','name', 'products']

	def get_products(self, instance):
		# Le paramètre 'instance' est l'instance de la catégorie consultée.
		# Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
		# d'entités dans la liste

		# On applique le filtre sur notre queryset pour n'avoir que les produits actifs
		queryset = instance.products.filter(active=True)
		# Le serializer est créé avec le queryset défini et toujours défini en tant que many=True

		serializer = ProductSerializer(queryset, many=True)
		# la propriété '.data' est le rendu de notre serializer que nous retournons ici
		return serializer.data

class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'ecoscore']


class ProductDetailSerializer(serializers.ModelSerializer):

    articles = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'articles']

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data

class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = ['id', 'date_created', 'name', 'price', 'product']
	
	def validate_price(self, value):
		if value < 1:
			raise serializers.ValidationError('Price must be greater than 1')
		return value

	def validate_product(self, value):
		if value.active is False:
			raise serializers.ValidationError('Inactive product')
		return value