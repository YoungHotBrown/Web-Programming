from django.contrib import admin

from .models import Member, Article

#admin login details username: admin, password: password
# Register your models here.

admin.site.register(Member)
admin.site.register(Article)