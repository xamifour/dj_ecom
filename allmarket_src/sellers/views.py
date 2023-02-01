from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)

from isMarket.decorators import seller_required
from sellers.models import ProductBatch
from .models import Seller, User
from .forms import SellerForm, ProductBatchForm



#Views Here

def sellerStatView(request):
    if request.user.is_authenticated:
    	if request.user.is_seller:
    		context = {}	
    		return render(request, "sellers/seller_stat.html", context)
    	else:
	    	return render(request, 'index.html')
    else:
    	return render(request, 'index.html')    	


@method_decorator([login_required, seller_required], name='dispatch')
class SellerCreateView(CreateView):
    model   = Seller
    form_class = SellerForm
    template_name = 'sellers/seller_form.html'

    def form_valid(self, form):
        seller = form.save(commit=False)
        seller.owner = self.request.user
        seller.save()
        messages.success(self.request, 'The seller was created with success! Go ahead and add some batch now.')
        return redirect('sellers:seller_list')


@method_decorator([login_required, seller_required], name='dispatch')
class SellerListView(ListView):
    model = Seller
    ordering = ('title', )
    context_object_name = 'sellers'
    template_name = 'sellers/seller_list.html'
    #template_name = 'sellers/seller_product_list.html'

    def get_queryset(self):
        queryset = self.request.user.seller.all()
        return queryset
   
    def get_success_url(self):
        return reverse('seller_update', kwargs={'pk': self.object.pk})


def sellerDetailsView(request, seller_id):
    if request.user.is_authenticated:
        if request.user.is_seller:
            try:
                seller = Seller.objects.get(pk=seller_id)
            except seller.DoesNotExist:
                raise Http404("seller does not exist") 
            context = {
                "seller": seller,
                "batch_seller": seller.batch_seller.all(),
            }
            return render(request, "sellers/seller_details.html", context)
        else:
            return render(request, 'index.html')            
    else:
        return render(request, 'index.html')


@method_decorator([login_required, seller_required], name='dispatch')
class SellerUpdateView(UpdateView):
    models              = Seller
    fields              = '__all__' #('title',)
    context_object_name = 'seller'
    template_name       = 'sellers/seller_form.html'
 
    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing seller that belongs
        to the logged in user.
        '''
        #return seller.objects.filter(owner=self.request.user)
        return self.request.user.seller.all()

    def get_success_url(self):
        #return redirect('sellers:seller_details', seller.pk)
        return reverse('sellers:seller_list')
        

@method_decorator([login_required, seller_required], name='dispatch')
class SellerDeleteView(DeleteView):
    model = Seller
    context_object_name = 'seller'
    template_name = 'sellers/seller_delete_confirm.html'
    success_url = reverse_lazy('sellers:seller_list')

    def delete(self, request, *args, **kwargs):
        seller = self.get_object()
        messages.success(request, 'The seller %s was deleted with success!' % seller.title)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.seller.all()

'''
def delete_seller(request, seller_id):
    seller = Seller.objects.get(pk=seller_id)
    seller.delete()
    sellers = Seller.objects.filter(user=request.user)
    messages.success(request, 'The seller %s was deleted with success!' % seller.title)
    return render(request, 'seller/index.html', {'sellers': sellers})
    '''



    
#------------------------------------------------------------------- Product Batch

@login_required
@seller_required
def productBatchAddView(request, pk):
    # By filtering the seller by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # seller will be able to add product batchs to it.
    seller = get_object_or_404(Seller, pk=pk, owner=request.user)
    form = ProductBatchForm(request.POST)
    
    if request.method == 'POST':
        if form.is_valid():
            productbatch = form.save(commit=False)
            productbatch.seller = seller
            productbatch.save()
            messages.success(request, 'Product Batch added successfully, you may now add products to the product batch.')
            return redirect('sellers:seller_details', seller.pk)
    else:
        form = ProductBatchForm()

    return render(request, 'sellers/productbatch_form.html', {'seller': seller, 'form': form})


#@login_required
#@seller_required
def productBatchDetailsView(request, seller_id, productbatch_id):
    if request.user.is_authenticated:
        if request.user.is_seller:
        # Simlar to the `productbatch_add` view, this view is also managing
        # the permissions at object-level. By querying both `seller` and
        # `productbatch` we are making sure only the owner of the seller can
        # change its details and also only productbatchs that belongs to this
        # specific seller can be changed via this url (in cases where the
        # user might have forged/player with the url params.
            seller = get_object_or_404(Seller, pk=seller_id, owner=request.user)
            productbatch = get_object_or_404(ProductBatch, pk=productbatch_id, seller=seller)

            context = {
                "seller"       : seller,
                "productbatch"   : productbatch,
                "products"       : productbatch.product_batch.all(),       
            }

            return render(request, "sellers/productbatch_details.html", context)
        else:
            return render(request, 'index.html')            
    else:
        return render(request, 'index.html')    


@login_required
@seller_required
def productBatchUpdateView(request, seller_id, productbatch_id):
    # Simlar to the `productbatch_add` view, this view is also managing
    # the permissions at object-level. By querying both `seller` and
    # `productbatch` we are making sure only the owner of the seller can
    # change its details and also only productbatchs that belongs to this
    # specific seller can be changed via this url (in cases where the
    # user might have forged/player with the url params.
    seller = get_object_or_404(Seller, pk=seller_id, owner=request.user)
    productbatch = get_object_or_404(ProductBatch, pk=productbatch_id, seller=seller)
    form = ProductBatchForm(request.POST, instance=productbatch)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Batch successfully updated!')
            return redirect('sellers:productbatch_details', seller.pk, productbatch.pk)
       
    else:
        form = ProductBatchForm(instance=productbatch)

    return render(request, 'sellers/productbatch_form.html', {
        'seller'       : seller,
        'productbatch'   : productbatch,
        'form'           : form,
    })


@method_decorator([login_required, seller_required], name='dispatch')
class ProductBatchDeleteView(DeleteView):
    model = ProductBatch
    context_object_name = 'productbatch'
    template_name = 'sellers/productbatch_delete_confirm.html'
    #success_url = reverse_lazy('sellers:seller_list')
    pk_url_kwarg = 'productbatch_id'

    def get_context_data(self, **kwargs):
        productbatch = self.get_object()
        kwargs['seller'] = productbatch.seller
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        productbatch = self.get_object()
        messages.success(request, 'The product batch %s was successfully deleted!' % productbatch.title)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return ProductBatch.objects.filter(seller__owner=self.request.user)

    def get_success_url(self):
        productbatch = self.get_object()
        return reverse('sellers:seller_list')

'''
def delete_song(request, album_id, song_id):
    seller = get_object_or_404(Seller, pk=seller_id)
    productbatch = ProductBatch.objects.get(pk=productbatch_id)
    productbatch.delete()
    return render(request, 'sellers/seller_list.html', {'seller': seller})
'''
'''
    def get_success_url(self):
        productbatch = self.get_object()
        return reverse('sellers:seller_details', kwargs={'pk': productbatch.seller_id})
'''