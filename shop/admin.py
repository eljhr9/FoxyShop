from django.contrib import admin
from .models import Product, Brand

class ProductAdmin(admin.ModelAdmin):
	list_display = ('title', 'text', 'price', 'availability', 'date_added', 'brand')
	list_display_links = ('title', 'text')
	search_fields = ('title', 'text', 'availability', 'date_added', 'brand',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
