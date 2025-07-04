from urllib import request
from django.shortcuts import render,redirect
from django.views import generic
from django.core import paginator
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.utils.text import slugify
from store.models import (Product)
from category.models import Category
from cart.models import Cart, CartItem
from cart.views import _cart_id
from django.http import HttpResponse

# Create your views here.
def Store(request,category_slug=None):
        categories = None
        products = None
        if category_slug != None:
            categories = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(category=categories, is_available= True)
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            page_products = paginator.get_page(page)
            product_count= products.count()
        else:      
            products= Product.objects.all().filter(is_available=True).order_by('id')
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            page_products = paginator.get_page(page)
            product_count= products.count()
        context={
            'products':page_products,
            'product_count':product_count,
        }
        return render(request, 'store/store.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        products = Product.objects.order_by('created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        product_count= products.count()
    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'index.html', context)
    


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        #return HttpResponse(in_cart)
        #exit()
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
    }
    return render(request, 'store/product_detail.html', context)
