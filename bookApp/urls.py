from django.urls import path
from .views import (PhotoView,BlogView, DetailViews,SearchView, CategoryDetailView, SubcriptionView, CreatePostView, likePostView, viewerPostView,
 UpdatePostView, DeletePostView, AuthorDetailView, CommentsDetailView,AllArticleView, AllPostView, AboutView, ContactView, ContactFormView, CommentFormView)

from . import views

urlpatterns = [
    path('', BlogView.as_view(), name='home'),
    path('<int:pk>/article/post', DetailViews.as_view(), name='blog-details'),
    path('post/<slug:pk>/comment/', CommentsDetailView.as_view(), name='commen'),
    path('<int:pk>/like/post', likePostView, name='like'),
    path('<int:pk>/view/post', viewerPostView, name='viewer'),
    path('article/post/photography', PhotoView.as_view(), name='photo'),
    path('article/post/all-article', AllArticleView.as_view(), name='article'),
    path('article/post/list-post', AllPostView.as_view(), name='post'),
    path('article/post/search', SearchView.as_view(), name='search'),
    path('article/post/subcribe',  SubcriptionView.as_view(), name='emailforms'),
    path('about-author', AboutView.as_view(), name='about'),
    path('contactform', ContactFormView.as_view(), name='contactform'),
    path('article/post/<int:pk>/comment/', CommentFormView.as_view(), name='commentform'),
    path('contact-infomation', ContactView.as_view(), name='contact'),
    path('article/post/create-post', CreatePostView.as_view(), name='create-post'),
    path('article/post/update/<slug:slug>', UpdatePostView.as_view(), name='update-post'),
    path('article/post/delete/<slug:slug>', DeletePostView.as_view(), name='delete-post'),
    path('article/post/tag/<slug:slug>', CategoryDetailView.as_view(), name='cat'),
    path('author/<int:pk>', AuthorDetailView.as_view(), name='author-detail'),
    
]

