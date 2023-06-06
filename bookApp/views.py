from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

# Django.contrib
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

# Django.views.generic module
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Model module
from django.db.models import Count
from .models import Author, Category, Post, Subcriber, Comment, Contact, Like, Viewer

# Forms module
from .form import CreatPostForm, MassageForm

# Like postview
def likePostView(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    new_like = post.like
    liked = Like.objects.filter(user=user, post=post).count()
    if not liked:
        liked = Like.objects.create(user=user, post=post)
        new_like+=1

    post.like = new_like
    post.save()
    return HttpResponseRedirect(reverse('blog-details', args=[pk]))

# Viewers postview
def viewerPostView(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    new_viewer = post.viewer
    viewered= Viewer.objects.filter(user=user, post=post).count()
    if not viewered:
        viewered = Viewer.objects.create(user=user, post=post)
        new_viewer+=1

    post.viewer = new_viewer
    post.save()
    return HttpResponseRedirect(reverse('blog-details', args=[pk]))

# Index page
class BlogView(ListView):
    model = Post
    queryset = Post.objects.all().order_by('-id')
    context_object_name = 'prints'
    template_name = 'bookApp/index.html'
    paginate_by = 12
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(id=1)
        context['auth'] = Author.objects.all()
        #context['comment'] = context['prints'].comment.all().count()
        context['commentcount'] = Comment.objects.values('post__title').annotate(Count('post__title'))
        context['sidebar'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        return context

# About page   
class AboutView(ListView):
    model = Author
    template_name = 'bookApp/about.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(id=1)
        context['sidebar'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        return context

# Contact-FormView
class ContactFormView(View):
    def post(self, request):
        names = request.POST.get('name')
        mails = request.POST.get('mail')
        subjects = request.POST.get('subject')
        messages = request.POST.get('message')
        new_contact =  Contact.objects.create(name=names, mail=mails, subject=subjects, message=messages)
        new_contact.save()
        return  redirect('home')

    def get(self, request):
        name = Contact.objects.all().order_by('-id')
        return render(request, 'bookApp/includes/contactform.html')

# Contact viewpage
class ContactView(ListView):
    model = Post
    template_name = 'bookApp/contact.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(id=1)
        context['sidebar'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        return context

    
# Photo viewpage
class PhotoView(ListView):
    queryset = Post.objects.all().order_by('-id')
    context_object_name = 'photos'
    template_name = 'bookApp/photography.html'
    paginate_by = 12
 
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(id=1)
        context['sidebar'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        return context

# Allarticle viewpage
class AllArticleView(ListView):
    queryset = Post.objects.all().order_by('-id')
    context_object_name = 'printers'
    template_name = 'bookApp/all-article.html'
    paginate_by = 12
 
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(id=1)
        context['print'] = Post.objects.order_by('-id')[0:4]
        context['move'] = Post.objects.order_by('?')[0:6]
        context['deprint'] = Post.objects.order_by('?')[0:3]
        context['sidetag'] = Category.objects.order_by('?')[0:9]
        context['sidebar'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        return context
        
# Allpost viewpage
class AllPostView(ListView):
    queryset = Post.objects.all().order_by('-id')
    context_object_name = 'printers'
    template_name = 'bookApp/all-post.html'
    paginate_by = 6
 
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(id=1)
        context['print'] = Post.objects.order_by('-id')[0:4]
        context['move'] = Post.objects.order_by('?')[0:6]
        context['deprint'] = Post.objects.order_by('?')[0:3]
        context['sidetag'] = Category.objects.order_by('?')[0:9]
        context['commentst'] = Comment.objects.values('post__title').annotate(Count('post__title'))
        context['sidebar'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        return context
        
# Search viewpage
class SearchView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'printers'
    template_name = 'bookApp/show-searched-list.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(id=1)
        context['auth'] = Author.objects.all()
        context['printfail'] = Post.objects.order_by('?')
        context['move'] = Post.objects.order_by('?')[0:6]
        context['deprint'] = Post.objects.order_by('?')[0:3]
        context['print'] = Post.objects.order_by('-id')[0:4]
        context['sidetag'] = Category.objects.order_by('?')[0:9]
        context['sidebar'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        searcher = self.request.GET.get('searchs') or ''
        if searcher:
            context['printers'] = context['printers'].filter(title__istartswith=searcher)
            context['count'] = context['printers'].filter(title__icontains=searcher).count()
        context['searcher'] = searcher
        return context

# Post detail viewpage
class DetailViews(View):
    def get(self, request, pk):
        context = {}
        context['form'] = MassageForm()
        context['detail'] = Post.objects.get(pk = pk)
        context['mover'] = Post.objects.order_by('?')[0:6]
        context['sidetag'] = Category.objects.order_by('?')[0:9]
        context['author'] = Author.objects.get(id=1)
        context['sidebar'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        context['comment'] = context['detail'].comment.all().count()
        context['print'] = Post.objects.order_by('-id')[0:4]
        context['deprint'] = Post.objects.order_by('?')[0:3]
        return render(request,'bookApp/read-more-page.html', context)

    def post(self, request, pk):
        form = MassageForm(request.POST)
        if form.is_valid():
            form.instance.user = self.request.user
            form.instance.post_id = self.kwargs['pk']
            form.save()
            return HttpResponseRedirect(reverse('blog-details', args=[pk]))
        return render(request, 'bookApp/read-more-page.html', )

# Category detail viewpage
class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'printer'
    template_name = 'bookApp/category.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(id=1)
        context['sidebar'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        context['print'] = Post.objects.order_by('-id')[0:4]
        context['deprint'] = Post.objects.order_by('?')[0:3]
        #context['move'] = Post.objects.order_by('?')[0:6]
        context['sidetag'] = Category.objects.order_by('?')[0:9]
        return context

#Post create viewpage
class CreatePostView(CreateView):
    model = Post
    form_class = CreatPostForm
    template_name = 'bookApp/create-post.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(id=1)
        context['sidebar'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        return context

    def form_valid(self, forms):
        forms.instance.user = self.request.user
        return super().form_valid(forms)

# Subcribers viewpage
class SubcriptionView(View):
    def post(self, request):
        emailing = request.POST.get('emailer')
        new_email =  Subcriber.objects.create(emailing=emailing)
        new_email.save()
        return  redirect('home')

    def get(self, request):
        new_email = Subcriber.objects.all().order_by('-id')
        return render(request, 'bookApp/includes/subcribe.html')

# Post update viewpage
class UpdatePostView(UpdateView):
    model = Post
    form_class = CreatPostForm
    template_name = 'bookApp/update.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(id=1)
        context['sidebar'] = Post.objects.values('categories__title').annotate(Count('categories__title'))
        return context

# Post delete viewpage
class DeletePostView(DeleteView):
    model = Post
    template_name = 'bookApp/delete.html'
    context_object_name = 'delete'
    success_url = reverse_lazy('article')    

# Comment create viewpage
class CommentFormView(CreateView):
    model = Comment
    form_class = MassageForm
    template_name = 'bookApp/commentform.html'
    def form_valid(self, forms):
        forms.instance.user = self.request.user
        forms.instance.post_id = self.kwargs['pk']
        return super().form_valid(forms)
        
    def get_success_url(self):
        return reverse('blog-details', kwargs={'pk': self.kwargs['pk'],}) 
   
# Comment detail viewpage
class CommentsDetailView(DetailView):
    queryset = Comment.objects.all()
    context_object_name = 'details'
    template_name = 'bookApp/read-more-page.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['massages'] = context['detail'].count()
        return context


'''
class ReplyCommentsView(ListView):
    queryset = ReplyCommentsModel.objects.all()
    context_object_name = 'detail'
    template_name = 'myApp/blog-details.html'
    
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['massage'] = context['detail'].commentMode.count()
        return context
'''

# Author detail viewpage
class AuthorDetailView(DetailView):
    model = Author
    context_object_name = 'detail'
    template_name = 'myApp/profile.html'