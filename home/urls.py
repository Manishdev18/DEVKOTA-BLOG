from django.contrib import admin
from django.urls import path, include
from home import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserListView, LikeRedirect, SearchListView
urlpatterns = [
    path("",PostListView.as_view(),name='home'),
    
    path("about",views.about,name='about'),
    path("travel",views.travel,name='travel'),
    path("food",views.food,name='food'),
    path('user/<str:username>', UserListView.as_view(), name='user_post'),
    path('search', SearchListView.as_view(), name='search'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    #path('blogpost-like/<int:pk>', views.bloglike, name="blogpost_like"),
    path('blogpost-like/<int:pk>/', LikeRedirect.as_view(),name='blogpost_like'),
    #path('blogpost-like/', views.bloglike, name="blogpost_like"),
    path("post/new/",PostCreateView.as_view(),name='post-create'),
    path("post/<int:pk>/update/",PostUpdateView.as_view(),name='post-update'),
    path("post/<int:pk>/delete/",PostDeleteView.as_view(),name='post-delete'),
    path('register',views.register,name='register'),

   
]
