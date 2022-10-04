from email.policy import default
from accounts.models import Account
from django.db import models
from django.urls import reverse
# Create your models here.


class Vendor(models.Model):
    first_name     = models.CharField(max_length=100)
    last_name      = models.CharField(max_length=100)
    email          = models.CharField(max_length=100, unique=True)
    phone_number   = models.CharField(max_length=100,unique=True)
    password       = models.CharField(max_length=255)
    confirm_password= models.CharField(max_length=255)
    turf_name      = models.CharField(max_length=200)
    district       = models.CharField(max_length=200)
    city           = models.CharField(max_length=200)
    turf_address   = models.TextField(max_length=200)
    description    = models.TextField(max_length=255, blank=True)
    # image          = models.ImageField(upload_to='photos/products')
    create_date    = models.DateTimeField(auto_now_add=True)
    last_login     = models.DateTimeField(auto_now=True)
    modified_date  = models.DateTimeField(auto_now=True)
    is_Vendor      = models.BooleanField(default=True)
    is_Paid        = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=False,blank=True)
    
    def __str__(self):
        return self.email


class VendorToken(models.Model):
    vendor_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    
    class Meta:
        verbose_name = 'categrory'
        verbose_name_plural = 'categories'
        
    def get_url(self):
        return reverse('turfs_by_category', args=[self.slug])    
    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    def get_url(self):
        return reverse('turfs_by_subcategory',args=[self.category.slug,self.slug])
    
    def __str__(self):
        return self.category.category_name+'/'+self.name

class District(models.Model):
    district = models.CharField(max_length=255)

    def __str__(self):
        return self.district

class City(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.city



class Turf(models.Model):
    turf_name = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    image1 = models.ImageField(upload_to='photos/products')
    image2 = models.ImageField(upload_to='photos/products')
    image3 = models.ImageField(upload_to='photos/products')
    is_available = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    SubCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.turf_name

class TurfSlot(models.Model):
    Date = models.DateField()
    Time = models.TimeField()
    Slot_No = models.CharField(max_length=255)
    turf = models.ForeignKey(Turf,blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Account,blank=True, null=True, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor,blank=True, null=True, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    Is_booked = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Slot_No


class VendorOrder(models.Model):
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)
    vendor = models.ForeignKey(Vendor,blank=True, null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_payment_id