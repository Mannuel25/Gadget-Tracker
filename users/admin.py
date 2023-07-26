from django.contrib import admin
from .models import User

class userAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'picture']

admin.site.register(User, userAdmin)
