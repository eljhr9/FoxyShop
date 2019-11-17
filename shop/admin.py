from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
	list_display = ('title', 'text', 'price', 'availability', 'date_added')
	list_display_links = ('title', 'text')
	search_fields = ('title', 'text', 'availability', 'date_added', )

admin.site.register(Product, ProductAdmin)