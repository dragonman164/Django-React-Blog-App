from rest_framework import serializers
from .models import BlogUser, User,Blog

class BlogUserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = BlogUser
        fields = ['name','email','phoneno','address','profession','dob','gender']

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User 
        fields = ['username','email','is_member']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

class BlogSerializer(serializers.ModelSerializer):
    user = BlogUserSerializer(read_only = True)
    class Meta: 
        model = Blog
        fields = '__all__'

# class Comment(serializers.ModelSerializer):

