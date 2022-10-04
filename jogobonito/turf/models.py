# from django.urls import reverse
# from django.db import models
# from django.db.models import Avg,Count
# from accounts.models import Account 

# Create your models here.

# class Category(models.Model):
#     category_name = models.CharField(max_length=50, unique=True)
#     slug = models.SlugField(max_length=100, unique=True)
#     description = models.TextField(max_length=255)
#     cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    
#     class Meta:
#         verbose_name = 'categrory'
#         verbose_name_plural = 'categories'
        
#     def get_url(self):
#         return reverse('turfs_by_category', args=[self.slug])    
#     def __str__(self):
#         return self.category_name


# class SubCategory(models.Model):
#     category=models.ForeignKey(Category,on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     slug = models.SlugField(unique=True)
    
#     def get_url(self):
#         return reverse('turfs_by_subcategory',args=[self.category.slug,self.slug])
    
#     def __str__(self):
#         return self.category.category_name+'/'+self.name




# class Turf(models.Model):
#     turf_name = models.CharField(max_length=200)
#     size = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=200, unique=True)
#     description = models.TextField(max_length=500, blank=True)
#     price = models.IntegerField()
#     image = models.ImageField(upload_to='photos/products')
#     image1 = models.ImageField(upload_to='photos/products')
#     image2 = models.ImageField(upload_to='photos/products')
#     image3 = models.ImageField(upload_to='photos/products')
#     is_available = models.BooleanField(default=False)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     SubCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
#     create_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.turf_name


# class District(models.Model):
#     district = models.CharField(max_length=255)

#     def __str__(self):
#         return self.district

# class City(models.Model):
#     district = models.ForeignKey(District, on_delete=models.CASCADE)
#     city = models.CharField(max_length=255)

#     def __str__(self):
#         return self.city