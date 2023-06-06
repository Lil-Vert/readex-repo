from django.contrib import admin
from .models import Author, Post, Category, Subcriber, Contact, Comment
# Register your models here.
admin.site.register([Author,Subcriber, Contact, Post])
@admin.register(Comment)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','comment', 'post', 'timestamp']

@admin.register(Category)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','slug','thumbnail', 'timestamp']