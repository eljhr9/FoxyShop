from django.contrib import admin
from .models import Product, Brand, Rubric

class ProductAdmin(admin.ModelAdmin):
	list_display = ('title', 'price', 'availability', 'date_added', 'brand', 'rubric')
	list_display_links = ('title', 'availability')
	search_fields = ('title', 'availability', 'date_added', 'brand', 'rubric')

admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Rubric)
