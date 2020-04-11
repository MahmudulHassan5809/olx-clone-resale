from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from products.forms import AdPostForm
from accounts.mixins import AictiveUserRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
import random
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import generic
from django.views import View

# Create your views here.


class AdList(generic.ListView):
    model = Product
    context_object_name = 'ad_list'
    paginate_by = 10
    template_name = 'ads/ad_list.html'

    def get_queryset(self):
        return Product.active_objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - All Ads'
        return context


class AdDetail(generic.DetailView):
    model = Product
    template_name = 'ads/ad_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['related_products'] = list(
            Product.active_objects.filter(category=self.object.category))[:3]
        return context


class UserProduct(generic.ListView):
    model = Product
    context_object_name = 'ad_list'
    paginate_by = 10
    template_name = 'ads/ad_list.html'

    def get_queryset(self):
        username = self.kwargs.get('username')
        user_obj = get_object_or_404(User, username=username)

        ad_list = Product.active_objects.filter(owner=user_obj)
        return ad_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['title'] = f'{username} Products'
        return context


class CategoryProduct(generic.ListView):
    model = Product
    context_object_name = 'ad_list'
    paginate_by = 10
    template_name = 'ads/ad_list.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        category_obj = get_object_or_404(Category, slug=category_slug)

        ad_list = Product.active_objects.filter(category=category_obj)
        return ad_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        context['title'] = f'{category_slug} Products'
        return context


class PostAd(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ad_post_form = AdPostForm()
        context = {
            'title': 'Ad Post',
            'ad_post_form': ad_post_form
        }

        return render(request, 'ads/post_ad.html', context)

    def post(self, request, *args, **kwargs):
        ad_post_form = AdPostForm(request.POST, request.FILES)

        if ad_post_form.is_valid():
            ad_post = ad_post_form.save(commit=False)
            ad_post.owner = request.user
            ad_post.save()

            for afile in request.FILES.getlist('images'):
                ad_post.product_images.create(image=afile)

            messages.success(request, 'Ad Posted Succesfully')
            return redirect('products:post_ad')
        else:
            context = {
                'title': 'Ad Post',
                'ad_post_form': ad_post_form
            }

            return render(request, 'ads/post_ad.html', context)


class UpdateProduct(generic.edit.UpdateView):
    model = Product
    fields = ['title', 'price', 'description', 'brand', 'city', 'area']
    template_name = 'ads/update_ad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class DeleteAdd(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        product_obj = get_object_or_404(Product, id=product_id)

        product_obj.delete()
        messages.success(request, f'{product_obj.title} Deleted Successfully Succesfully')
        return redirect('accounts:my_products')


@method_decorator(csrf_exempt, name='dispatch')
class SearchProduct(View):
    def get(self, request, *args, **kwargs):
        area = request.GET.get('area')
        city = request.GET.get('city')
        search = request.GET.get('search')
        category_id = request.GET.get('category')
        category_obj = get_object_or_404(Category, id=category_id)

        category_products = category_obj.category_products.all()

        search_products = category_products.filter(
            Q(title__icontains=search) | Q(description__icontains=search), city=city, area=area)

        context = {
            'title': 'Search Result',
            'search_products': search_products
        }

        return render(request, 'ads/search_result.html', context)


class ProductMonthArchiveView(generic.dates.MonthArchiveView):
    queryset = Product.active_objects.all()
    template_name = 'ads/archive.html'
    date_field = "created_at"
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Archive Ads'
        context['year'] = self.kwargs.get('year')
        context['month'] = self.kwargs.get('month')
        return context
