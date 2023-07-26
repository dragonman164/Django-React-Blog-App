from django.shortcuts import render,HttpResponse
from django.contrib.auth.hashers import make_password


from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import filters


from .serializers import BlogUserSerializer,UserSerializer,BlogSerializer
from .models import BlogUser,Blog

# Create your views here.
def index(request):
    return HttpResponse("<h1>Backend for Blog is running!!</h1>")


class BlogUserRegistrationView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data = request.data)
        if request.data.get('password') is None: 
            return Response({
                "message" : "Password is missing!!"
            },status = status.HTTP_400_BAD_REQUEST)
        password = request.data['password']
        password = make_password(password=password)
        request.data.update({'is_member' : True})
        if user_serializer.is_valid():
            bloguser_serializer = BlogUserSerializer(data = request.data)
            if bloguser_serializer.is_valid():
                user = user_serializer.save(password = password)
                bloguser_serializer.save(member = user)
                return Response(bloguser_serializer.data,status = status.HTTP_201_CREATED)
            else: 
                return Response(bloguser_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        return Response(user_serializer.errors, status = status.HTTP_400_BAD_REQUEST)


# View details of the self
class BlogUserView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]

    def get(self, request):
        user = self.request.user
        bloguser = BlogUser.objects.get(member = user)
        bloguser_serializer = BlogUserSerializer(bloguser)
        return Response(bloguser_serializer.data, status = status.HTTP_200_OK)

# Blog View for user only for their blogs with CRUD Operations
class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = self.request.user
        blogs = Blog.objects.filter(user__member = user)
        blog_serializer = BlogSerializer(blogs,many = True)
        return Response(blog_serializer.data, status = status.HTTP_200_OK)

    def put(self, request):
        pass 

    def post(self, request):
        user = self.request.user
        blog_serializer = BlogSerializer(data = request.data)
        if blog_serializer.is_valid():
            blog_serializer.save(user = BlogUser.objects.get(member = user))
            return Response(blog_serializer.data, status = status.HTTP_201_CREATED)
        return Response(blog_serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

    # def delete(self, request):
    #     user = self.request.user
    #     if request.data.get('id') is None: 
    #         return Response({
    #             "message" : "Please Specify ID for blog deletion"
    #         },status = status.HTTP_400_BAD_REQUEST)
    #     blog = Blog.objects.get(id = request.data.get('id'))

    #     if blog is None: 
    #         return Response({
    #             "message" : "Blog ID not present for deletion"
    #         })


# User List View with all relevant filters (to be fixed, showing all user details)
class BlogUserListView(ListAPIView):
    queryset = BlogUser.objects.all()
    serializer_class = BlogUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

# Blog List View with all relevant filters
class BlogListView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['topic','user__name']

## Todo 
# 1. Put , delete, method for updating or deleting user
# 2. Blog User List view should only show names and nothing else