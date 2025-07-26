from django.contrib import admin
from .models import InspirationVideo

@admin.register(InspirationVideo)
class InspirationVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')  
    list_filter = ('category',)          
    search_fields = ('title',)    