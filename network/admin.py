from django.contrib import admin
from .models import Posts, Profile, User

# Register your models here.
admin.site.register(Posts)
admin.site.register(User)
admin.site.register(Profile)