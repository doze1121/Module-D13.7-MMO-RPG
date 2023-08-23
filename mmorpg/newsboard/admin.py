from django.contrib import admin

from .forms import PostCreateForm
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostCreateForm


admin.site.register(Category)
admin.site.register(Comment)