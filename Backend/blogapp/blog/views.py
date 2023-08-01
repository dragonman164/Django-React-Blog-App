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


from .serializers import BlogUserSerializer,UserSerializer,BlogSerializer,LikeDislikeSerializer
from .models import BlogUser,Blog,LikeDisklike

# Create your views here.
def index(request):
    return HttpResponse("<h1>Backend for Blog is running!!</h1>")

# Register a new user into the system
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
    
        

# View details of the self user with CRUD operations (C) in register
class BlogUserView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]

    def get(self, request):
        user = self.request.user
        bloguser = BlogUser.objects.get(member = user)
        bloguser_serializer = BlogUserSerializer(bloguser)
        return Response(bloguser_serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request):
        user = self.request.user 
        bloguser = BlogUser.objects.get(member = user)
        bloguser_serializer = BlogUserSerializer(bloguser, data = request.data)
        if bloguser_serializer.is_valid():
            bloguser_serializer.save()
            return Response(bloguser_serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(bloguser_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = self.request.user
        user.delete()
        return Response({
            "message" : "User successfully deleted"
        },status = status.HTTP_204_NO_CONTENT)

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
        user = self.request.user 
        if request.data.get('id') is None: 
            return Response({
                "message" : "Please Specify Blog ID you want to update"
            },status = status.HTTP_400_BAD_REQUEST)
        blog = Blog.objects.filter(id = request.data.get('id'),user__member = user)
        if len(blog) == 0: 
            return Response({
                "message" : "Blog ID not present for update or does not belong to this user"
            },status = status.HTTP_404_NOT_FOUND)
        blog_serializer = BlogSerializer(blog[0], data = request.data)
        if blog_serializer.is_valid():
            blog_serializer.save()
            return Response(blog_serializer.data, status = status.HTTP_202_ACCEPTED)
        return Response(blog_serializer.errors, status = status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        user = self.request.user
        blog_serializer = BlogSerializer(data = request.data)
        if blog_serializer.is_valid():
            blog_serializer.save(user = BlogUser.objects.get(member = user))
            return Response(blog_serializer.data, status = status.HTTP_201_CREATED)
        return Response(blog_serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

    def delete(self, request):
        user = self.request.user
        if request.data.get('id') is None: 
            return Response({
                "message" : "Please Specify ID for blog deletion"
            },status = status.HTTP_400_BAD_REQUEST)
        blog = Blog.objects.filter(id = request.data.get('id'),user__member = user)

        if len(blog) == 0: 
            return Response({
                "message" : "Blog ID not present for deletion or not belongs to this user"
            },status = status.HTTP_404_NOT_FOUND)
        blog[0].delete()
        return Response({
            "message" : "Blog Successfully Deleted"
        },status = status.HTTP_204_NO_CONTENT)

# CRUD Operations for Like Dislike for a particular post
class LikeDislikeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        if request.GET.get('blog') is None: 
            return Response({
                "message" : "Please specify blog id for liking diskling remove"
            },status = status.HTTP_400_BAD_REQUEST)
        blog = Blog.objects.filter(id = request.GET.get('blog'))
        if len(blog) == 0: 
            return Response({
                "message" : "Blog ID not found!!"
            },status = status.HTTP_404_NOT_FOUND)    
 
        like_dislike_object = LikeDisklike.objects.filter(blog = request.GET.get('blog'), user__member = self.request.user)
        if len(like_dislike_object) == 0: 
            return Response({
                "message" : "Like Disklike Data not found for given user and blog"
            },status = status.HTTP_404_NOT_FOUND)
        likedislike_serializer = LikeDislikeSerializer(like_dislike_object[0])
        return Response(likedislike_serializer.data, status = status.HTTP_200_OK)


    def post(self, request):
        if request.data.get('blog') is None: 
            return Response({
                "message" : "Please Specify Blog ID you want to Like /Dislike"
            },status = status.HTTP_400_BAD_REQUEST)

        blog = Blog.objects.filter(id = request.data.get('blog'))
        if len(blog) == 0: 
            return Response({
                "message" : "Blog ID not found!!"
            },status = status.HTTP_404_NOT_FOUND)        
        request.data.update({"user" : BlogUser.objects.get(member = self.request.user).id})
        like_dislike_serializer = LikeDislikeSerializer(data = request.data)
        if like_dislike_serializer.is_valid():
            like_dislike_serializer.save()
            return Response(like_dislike_serializer.data, status = status.HTTP_201_CREATED)
        return Response(like_dislike_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        if request.data.get('blog') is None: 
            return Response({
                "message" : "Please specify blog id for liking diskling remove"
            },status = status.HTTP_400_BAD_REQUEST)
        blog = Blog.objects.filter(id = request.data.get('blog'))
        if len(blog) == 0: 
            return Response({
                "message" : "Blog ID not found!!"
            },status = status.HTTP_404_NOT_FOUND)     
        like_dislike_object = LikeDisklike.objects.filter(blog = request.data.get('blog'), user__member = self.request.user)
        if len(like_dislike_object) == 0: 
            return Response({
                "message" : "Like Disklike Data not found for given user and blog"
            },status = status.HTTP_404_NOT_FOUND)
        like_dislike_serializer = LikeDislikeSerializer(like_dislike_object[0],data = request.data)
        if like_dislike_serializer.is_valid():
            like_dislike_serializer.save()
            return Response(like_dislike_serializer.data,status = status.HTTP_202_ACCEPTED)
        return Response(like_dislike_serializer.errors, status = status.HTTP_400_BAD_REQUEST)     
    
        
    
    def delete(self, request):
        if request.data.get('blog') is None: 
            return Response({
                "message" : "Please specify blog id for liking diskling remove"
            },status = status.HTTP_400_BAD_REQUEST)
        blog = Blog.objects.filter(id = request.data.get('blog'))
        if len(blog) == 0: 
            return Response({
                "message" : "Blog ID not found!!"
            },status = status.HTTP_404_NOT_FOUND)     
        like_dislike_object = LikeDisklike.objects.filter(blog = blog, user__member = self.request.user)
        if len(like_dislike_object) == 0: 
            return Response({
                "message" : "Like Disklike Data not found for given user and blog"
            },status = status.HTTP_404_NOT_FOUND)
        like_dislike_object[0].delete()
        return Response({
            "message" : "Like / Dislike Successfully Removed"
        },status = status.HTTP_204_NO_CONTENT)
    

class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        pass 

    def put(self, request):
        pass 
    
    def post(self, request):
        pass 
    
    def delete(self, request):
        pass 

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
# 1. Blog User List view should only show names and nothing else

