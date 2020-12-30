from django.contrib import admin
from home.models import contact
from home.models import profile,Post
# Register your models here.
admin.site.register(contact)
admin.site.register(profile)
admin.site.register(Post)
