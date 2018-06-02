from django.contrib import admin
from .models import Category, Product, Brand, Top_Product, Profile, Variation


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'country', 'state', 'city', 'street', 'home', 'appartment', 'index', 'phone_number']


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}


class VariationItemInline(admin.TabularInline):
    model = Variation
    raw_id_field = ['variation']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'articule', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'articule', 'stock', 'available']
    prepopulated_fields = {'slug': ('name', )}
    inlines = [VariationItemInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Top_Product)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Profile, ProfileAdmin)

