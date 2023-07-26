from django.contrib import admin
from .models import User,BlogUser,Blog,Comment,LikeDisklike


# Register your models here.
admin.site.register(User)
admin.site.register(BlogUser)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(LikeDisklike)