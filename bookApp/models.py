from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField


#The Author model that contain all informations
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=False, null=True)
    last_name = models.CharField(max_length=20, blank=False, null=True)
    about = models.TextField(blank=False, null=True)
    address = models.TextField(blank=False, null=True)
    street = models.TextField(blank=False, null=True)
    website_name = models.TextField(default='Elen', blank=True, null=True)
    facebook_url = models.CharField(max_length=225, blank=True, null=True)
    twitter_url = models.CharField(max_length=225, blank=True, null=True)
    telegram_url = models.CharField(max_length=225, blank=True, null=True)
    linkdin_url = models.CharField(max_length=225, blank=True, null=True)
    telgram_url = models.CharField(max_length=225, blank=True, null=True)
    tel = models.IntegerField(default="(234) ", null=True)
    image = models.ImageField(upload_to='myApp/image',  blank=False, null=True)
    
    def __str__(self):
        return self.user.username

#The Category model that contain all informations
class Category(models.Model):
    title = models.CharField(max_length=20, blank=False, null=True)
    description = models.TextField(blank=False, null=True)
    slug = models.SlugField( blank=False, null=True)
    thumbnail = models.ImageField( blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('cate-detail', kwargs={slug:'self.slug'})

#The Post model that contain all informations
class Post(models.Model):
    title = models.CharField(max_length=100, blank=False, null=True)
    overview = RichTextField(blank=False, null=True)
    updatetime = models.DateTimeField(auto_now=True, blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    like = models.IntegerField(default=0)
    viewer = models.IntegerField(default=0)
    author = models.ForeignKey(Author, related_name='post', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='myApp/image', blank=False, null=True)
    slug = models.SlugField(null=True)
    categories = models.ManyToManyField(Category, related_name="categories")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

#The Like model that contain all informations
class Like(models.Model):
    user = models.ForeignKey(User, related_name='user_like', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_like', on_delete=models.CASCADE)

#The Viewer model that contain all informations
class Viewer(models.Model):
    user = models.ForeignKey(User, related_name='user_viewer', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_viewer', on_delete=models.CASCADE)

#The Comments model that contain all informations
class Comment(models.Model):
    user = models.ForeignKey(User,blank=False,   null=True, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    
    def __str__(self):
        return self.massage

    class Meta:
        ordering=['-timestamp']

'''
class ReplyCommentsModel(models.Model):
    replymassage = models.TextField(blank=False, null=True)
    Comment = models.ForeignKey(Comment, related_name='replycommentmodel', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    
    def __str__(self):
        return self.replymassage
'''

#The Subcribers model that contain all informations
class Subcriber(models.Model):
    emailing = models.CharField(max_length=255, blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    
    def __str__(self):
        return self.emailing

    def get_absolute_url(self):
        return reverse('blog-details', kwargs={'slug':self.slug})

#The Contact model that contain all informations
class Contact(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    mail = models.CharField(max_length=255, blank=False, null=True)
    subject = models.CharField(max_length=255, blank=False, null=True)
    message = models.TextField(max_length=255, blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    
    def __str__(self):
        return self.name
