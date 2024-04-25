from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from shop.models import Category, Product, Article
from shop.serializers import CategoryListSerializer, CategoryDetailSerializer, ProductDetailSerializer, \
	ProductListSerializer, ArticleSerializer

class MultipleSerializerMixin:
	# Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent

    detail_serializer_class = None

    def get_serializer_class(self):
		# Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
			# Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()

class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):

	serializer_class = CategoryListSerializer
	detail_serializer_class = CategoryDetailSerializer
	queryset = Category.objects.all()

class CategoryViewset(ReadOnlyModelViewSet):
	serializer_class = CategoryListSerializer
	# Ajoutons un attribut de classe qui nous permet de définir notre serializer de détail
	detail_serializer_class = CategoryDetailSerializer

	def get_queryset(self):
		#return Category.objects.all()
		return Category.objects.filter(active=True)

	@action(detail=True, methods=['post'])
	def disable(self, request, pk):
		# Nous pouvons maintenant simplement appeler la méthode disable
		self.get_object().disable()
		# Retournons enfin une réponse (status_code=200 par défaut) pour indiquer le succès de l'action
		return Response()

class ProductViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
	serializer_class = ProductListSerializer
	detail_serializer_class = ProductDetailSerializer

	def get_queryset(self):
	#recuper tous les produits ds une vqr queryset
		queryset = Product.objects.filter(active=True)
		# Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
		category_id = self.request.GET.get('category_id')
		if category_id is not None:
			queryset = queryset.filter(category_id=category_id)
		#return Product.objects.all()
		return queryset

	@action(detail=True, methods=['post'])
	def disable(self, request, pk):
		self.get_object().disable()
		return Response()

class ArticleViewset(ReadOnlyModelViewSet):
	serializer_class = ArticleSerializer

	def get_queryset(self):
		queryset = Article.objects.filter(active=True)
		product_id = self.request.GET.get('product_id')
		if product_id is not None:
			queryset = queryset.filter(product_id=product_id)
		return queryset

class AdminArticleViewset(ModelViewSet):
	serializer_class = ArticleSerializer
	queryset = Article.objects.all()