import django_filters
from .models import Category, Product


class ProductsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    keyword = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains")
    maxPrice = django_filters.NumberFilter(field_name="price" or 0, lookup_expr="lte")

    minPrice=django_filters.NumberFilter(field_name="price" or 10000 ,lookup_expr="gte")

    class Meta:
        model = Product

        # fields = ['name', 'price', 'category',"id"]
        fields = ('name', 'price', 'category', 'id', 'keyword','maxPrice' ,'minPrice')
