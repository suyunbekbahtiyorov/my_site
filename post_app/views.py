from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from rest_framework import viewsets, status
from .models import Post
from .serializer import PostSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from post_app.permissions import IsStaffOrReadOnly


def login_required_decorator(func):
    return login_required(func, login_url='login_page')

@login_required_decorator
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        author = request.query_params.get('author', None)
        if author:
            self.queryset = self.queryset.filter(author=author)
        return super().list(request, *args, **kwargs)


@login_required_decorator
@api_view(['GET'])
def AuthorViewSet(request, author_id):
    try:
        queryset = Post.objects.get(author=author_id)
    except Post.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    title = queryset.title
    content = queryset.content
    return Response({
        "Title": title,
        "Content": content
    })

@login_required_decorator
@api_view(['GET'])
def PostsViewSet(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@login_required_decorator
@api_view(['POST'])
def Create_post(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def login_page(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            return redirect("home_page")

    return render(request, 'login.html')

# @login_required_decorator
# def home_page():
#     return HttpResponse('<h1>Hello Bro</h1>')

@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect("login_page")



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login_page")
    template_name = "signup.html"


