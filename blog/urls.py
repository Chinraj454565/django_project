from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("posts", views.AllPostView.as_view(), name="posts-page"),
    path("post/<slug:slug>", views.PostDetailView.as_view(), name="post-detail-page"),
    path("read-later" , views.ReadLaterPost.as_view(), name="read-later")
]

