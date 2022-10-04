# from django.contrib import admin
# from .models import Category, City, District, Turf, SubCategory

# # Register your models here.
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('category_name',)}
#     list_display = ('category_name','slug')

# class TurfAdmin(admin.ModelAdmin):
#     list_display = ('turf_name','price','category','modified_date','is_available')
#     prepopulated_fields = {'slug':('turf_name',)}
    
# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ('category','name','slug')
#     prepopulated_fields = {'slug':('name',)}

# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Turf, TurfAdmin)
# admin.site.register(SubCategory, SubCategoryAdmin)
# admin.site.register(District)
# admin.site.register(City)