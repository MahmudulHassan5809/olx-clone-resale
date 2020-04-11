from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.AdList.as_view(), name='home'),
    path('detail/<slug:slug>/', views.AdDetail.as_view(), name="ad_detail"),

    path('post-ad/', views.PostAd.as_view(), name='post_ad'),
    path('delete-ad/<int:id>', views.DeleteAdd.as_view(), name='delete_ad'),

    path('user/product/<str:username>/',
         views.UserProduct.as_view(), name="user_product"),

    path('category/product/<str:slug>/',
         views.CategoryProduct.as_view(), name="category_product"),

    path('update/product/<slug:slug>/',
         views.UpdateProduct.as_view(), name="update_product"),


    path('product/search/',
         views.SearchProduct.as_view(), name="search_product"),

    path('ads/<int:year>/<int:month>/', views.ProductMonthArchiveView.as_view(month_format='%m'),
         name="archive_month_ads"),
]
