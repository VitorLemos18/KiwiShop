from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from .models import Product, Category

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        # Filtro por categoria via GET parameter
        category_slug = self.request.GET.get('category')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug, is_active=True)
            queryset = queryset.filter(category=category)

        # Filtros adicionais (estoque, ordenação)
        stock_filter = self.request.GET.get('stock')
        if stock_filter == 'available':
            queryset = queryset.filter(stock__gt=0)

        sort = self.request.GET.get('sort', '')
        if sort == 'price_low':
            queryset = queryset.order_by('price')
        elif sort == 'price_high':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by('-featured', 'name')

        return queryset.prefetch_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 Categorias com contagem de produtos ativos (para sidebar e footer)
        context['categories'] = Category.objects.filter(is_active=True).annotate(
            active_products_count=Count(
                'products',
                filter=Q(products__is_active=True)
            )
        ).order_by('name')

        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return (
            Product.objects
            .filter(is_active=True)
            .select_related('category')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Produtos relacionados
        context['related_products'] = (
            Product.objects
            .filter(
                category=self.object.category,
                is_active=True
            )
            .exclude(id=self.object.id)
            .select_related('category')
            .order_by('-featured')[:4]
        )

        # Categorias (sidebar/footer)
        context['categories'] = (
            Category.objects
            .filter(is_active=True)
            .annotate(
                active_products_count=Count(
                    'products',
                    filter=Q(products__is_active=True)
                )
            )
            .order_by('name')
        )

        return context
