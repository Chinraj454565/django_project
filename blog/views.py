from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import date
from .models import Post
from django.views.generic import ListView, DetailView, View
from .form import CommentForm

# Create your views here.



class StartingPageView(ListView):
    model=Post
    template_name="blog/index.html"
    context_object_name="posts"
    ordering=["-date"]

    def get_queryset(self):
        queryset=super().get_queryset()
        data=queryset[:3]
        return data


class AllPostView(ListView):
    model=Post
    template_name="blog/all-posts.html"
    ordering=["-date"]
    context_object_name="all_posts"



class PostDetailView(View):

    def is_read(self, request, post_id):
        session_list=request.session.get("stored_post")

        if session_list is None:
            is_read_later=False

        else:
            is_read_later=post_id in session_list

        return is_read_later


    def get(self,request, slug):
        post=get_object_or_404(Post, slug=slug)
        tags=post.tags.all()
        comments=post.comments.all().order_by("-id")
        context={
            "post":post,
            "post_tags": tags,
            "comment_form":CommentForm(),
            "comments": comments,
            "is_read_later": self.is_read(request, post.id)
        }
        return render(request, "blog/post-detail.html",context)
    
    def post(self, request, slug):
        form=CommentForm(request.POST)
        posting=get_object_or_404(Post, slug=slug)
        comments=posting.comments.all().order_by("-id")
        if form.is_valid():
            post_save=form.save(commit=False)
            post_save.post=posting
            post_save.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        
        tags=posting.tags.all()
        context={
            "post":posting,
            "post_tags": tags,
            "comment_form":form,
            "comments": comments,
            "is_read_later": self.is_read(request, posting.id)
        }
        return render(request, "blog/post-detail.html",context)


class ReadLaterPost(View):
    def get(self,request):
        stored_posts=request.session.get("stored_post")

        context={}

        if stored_posts is None or len(stored_posts)==0:
            context["posts"]=[]
            context["has_post"]=False

        else:
            posts=Post.objects.filter(id__in=stored_posts)
            context["posts"]=posts
            context["has_post"]=True

        return render(request, "blog/stored-posts.html", context)

            
            

    def post(self,request):
        stored_post=request.session.get("stored_post")
        
        if stored_post is None:
            stored_post=[]

        post_id=int(request.POST.get("post_id"))
        
        if post_id not in stored_post:
            stored_post.append(post_id)
            
        else:
            stored_post.remove(post_id)

        request.session["stored_post"]=stored_post
        
        return HttpResponseRedirect("/")



# def post_detail(request, slug):
#     dedicated_post=get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-detail.html", {"post":dedicated_post, "post_tags": dedicated_post.tags.all()})