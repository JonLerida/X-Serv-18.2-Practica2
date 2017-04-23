from django.contrib import admin
from .models import URLModel

# Register your models here.
class URLAdmin(admin.ModelAdmin):
    fieldsets = [
        ('URL Original', {'fields': ['larga']}),
        ('URL Acortada', {'fields': ['corta']}),
        #'classes': ['collapse']}),
    ]
    list_display = ('larga', 'corta')

admin.site.register(URLModel, URLAdmin)
