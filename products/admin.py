from django.contrib import admin
from django.utils.html import escape, mark_safe
from .models import Category, Product, ProductImage


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "image"]
    search_fields = ('name', 'slug',)
    list_filter = ['name']
    exclude = ['slug']
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

    list_display = ["title", "category",
                    "condition", "price", "brand", "active", "created_at"]
    search_fields = ('title', 'slug', 'category__name',
                     'condition', 'brand', 'price', 'active')
    list_filter = ['category__name', 'condition', 'active']
    list_editable = ['active']
    exclude = ['slug']
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        obj.save()

        for afile in request.FILES.getlist('photos_multiple'):
            obj.product_images.create(image=afile)


admin.site.register(Product, ProductAdmin)
