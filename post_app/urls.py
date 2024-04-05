from django.urls import path, include
from .views import PostViewSet, AuthorViewSet, PostsViewSet, Create_post, login_page, SignUpView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='home_page')

urlpatterns = [
    path('', include(router.urls)),
    path('post/<int:author_id>/', AuthorViewSet, name='author_viewset'),
    path('posts/all/', PostsViewSet, name='posts_viewset'),
    path('posts/create/', Create_post, name='create_post'),
    path('login_page/', login_page, name='login_page'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
