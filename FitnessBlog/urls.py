from . import views
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, LikeView


urlpatterns = [
    # Returns HttpResponse from the view page that we are on the index page
    path('', PostListView.as_view(), name='FitnessBlog-index'),
    path('like/<int:pk>/', LikeView, name='like_post'),
    path('user/<str:username>', UserPostListView.as_view(), name='individual_posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    # Returns HttpResponse from the view page that we are on the routine page
    path('routine/', views.routine, name='FitnessBlog-routine'),
    path('routine_advice/', views.routine_advice, name='FitnessBlog-routine_advice'),
    path('nutritional_advice/', views.nutritional_advice, name='FitnessBlog-nutritional_advice'),


]

