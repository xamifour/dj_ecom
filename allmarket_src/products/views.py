from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views.generic import ListView, DetailView, View

#from orders.models import Order, OrderItem
from .models import Product, ProductCategory, SubCategory, Review, DisplayImage
from .forms import ReviewForm



class HomeView(ListView):
    model = Product
    #paginate_by = 8
    template_name = "index.html"


def homeView(request):
    context = {
        'object_list': Product.objects.all(),
        'display_images': DisplayImage.objects.all(),
    }
    return render(request, 'index.html', context)


class ProductSearchView(ListView):
    template_name = "products/product_search.html"
    #model = Product
    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        input_queried = self.request.GET.get('productSearch')
        products = Product.objects.all()
        category = self.request.GET.get('category', None)

        if category:
            category_qs = products.filter(
                           Q(category__title=category) |
                           Q(sub_category__title=category)).distinct()
            return category_qs

        if input_queried != '' and input_queried is not None:
            return Product.objects.search(input_queried) 
        else:
            return ''   
        
        #return Product.objects.all()
        #return Product.objects.featured()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductSearchView, self).get_context_data(*args, **kwargs)
        input_queried = self.request.GET.get('productSearch')
        context['input_queried'] = input_queried
        context.update({
            #'categories': ProductCategory.objects.values("title"),
            'sub_categories': SubCategory.objects.values("title"),
        })
        return context

'''
class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_details.html"
'''

def productDetailView(request, slug):
    model = Product
    paginate_by = 1
    product = get_object_or_404(Product, slug=slug)
    context = {
        'object': product,
        'product_reviews':  product.review_set.all(),
    }
    return render(request, "products/product_details.html", context)


class ProductComparisonView(ListView):
    template_name = "products/product_comparison.html"
    model = Product


@login_required
def reviewCreateView(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ReviewForm(request.POST)
    #review_user = request.user
    if request.method == 'POST':
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            #review.review_user = review_user
            review.save()
            messages.success(request, 'Product review added successfully')
            return redirect('products:productDetails', slug=slug)
    else:
        form = ReviewForm()

    return render(request, 'products/product_review_form.html', {'product': product, 'form': form})


'''
@login_required
def stock_management(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=True)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderProduct.objects.filter(
                item=item,
                user=request.user,
                ordered=True
            )[0]
            if order_item.quantity > 1:
                # checking if stock is not zero
                while item.stock_initial >= 1:
                    item.stock_initial -= order_item.quantity
                    item.save()
            else:
                item.stock_initial == 0:          
                messages.info(request, 'This item is finished.')
                return redirect('products:productDetails', slug=slug)
            messages.info(request, 'This item is finished.')
            return redirect('products:productDetails', slug=slug)
        else:
            messages.info(request, 'This item was not in your cart')
            return redirect('products:productDetails', slug=slug)
    else:
        messages.info(request, 'You do not have an active order')
        return redirect('products:productDetails', slug=slug)
'''
