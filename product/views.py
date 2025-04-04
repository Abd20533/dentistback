from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .filters import ProductsFilter

from .serializers import ProductSerializers
from rest_framework.pagination import  PageNumberPagination


# Create your views here.
@api_view(['GET'])
def get_all_prodect(request):
    products = Product.objects.all()
    serializers = ProductSerializers(products, many=True)
    # print(products)
    return Response({"products": serializers.data})


@api_view(['GET'])
def get_by_id(request, pk):
    products = get_object_or_404(Product, id=pk)
    serializers = ProductSerializers(products, many=False)
    print(products)
    return Response({"products": serializers.data})


@api_view(['GET'])
def get_all_prodect_filters(request):
    filterset=ProductsFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    # filterset = ProductsFilter(request.GET, queryset=Product.objects.all())

    serializers = ProductSerializers(filterset.qs, many=True)
    return Response({"products": serializers.data})


@api_view(['GET'])
def get_all_prodect_Pagenation(request):
    filterset=ProductsFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    count=filterset.qs.count()
    
    resPage=2
    paginnator=PageNumberPagination()
    paginnator.page_size = resPage
       
    queryset=paginnator.paginate_queryset(filterset.qs, request)
    serializers = ProductSerializers(queryset, many=True)
    return Response({"products": serializers.data,"per page":count})
    # 
    # return Response({"products": serializers.data})
    
    
