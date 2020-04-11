from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250)
    image = models.ImageField(
        upload_to="category/%Y/%m/%d/", blank=True, null=True)

    class Meta():
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def generate_unique_slug(klass, field):
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    print(unique_slug)
    return unique_slug


class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Product(models.Model):
    CONDITION_CHOICES = (
        ('0', 'Used'),
        ('1', 'New'),
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_products')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category_products')
    description = models.TextField()
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    price = models.FloatField()
    brand = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = models.Manager()
    active_objects = ActiveProductManager()

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if self.slug:
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Product, self.title)
        else:
            self.slug = generate_unique_slug(Product, self.title)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:update_product', args=[str(self.slug)])

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to="product/%Y/%m/%d/")

    def __str__(self):
        return self.product.title
