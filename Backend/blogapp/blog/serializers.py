from rest_framework import serializers
from .models import BlogUser, User,Blog,LikeDisklike,Comment

class BlogUserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = BlogUser
        fields = ['name','phoneno','address','profession','dob','gender']

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User 
        fields = ['username','email','is_member']
        extra_kwargs = {
            'password' : {'write_only' : True},
            'email' : {'required' : True}
        }

class BlogSerializer(serializers.ModelSerializer):
    user = BlogUserSerializer(read_only = True)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()


    def get_likes(self, data):
        return LikeDisklike.objects.filter(blog = data, like = True).count()
    
    def get_dislikes(self, data):
        return LikeDisklike.objects.filter(blog = data, dislike = True).count() 
    
    class Meta: 
        model = Blog
        fields = '__all__'

class LikeDislikeSerializer(serializers.ModelSerializer):
    blog = BlogSerializer(read_only = True)
    class Meta: 
        model = LikeDisklike
        fields = '__all__'
        extra_kwargs = {'like': {'required': True},'dislike' : {'required' : True}} 

    def validate(self, data):
        if data.get('like') is not None and data.get('dislike') is not None and data.get('like') == data.get('dislike'):
            raise serializers.ValidationError("Like and Disklike both can't be equal")
        return super().validate(data)
    
class CommentSerializer(serializers.ModelSerializer):
    user = BlogUserSerializer(read_only = True)
    blog = BlogSerializer(read_only = True)
    class Meta: 
        model = Comment
        fields = '__all__'
    
class BlogUserCustomSerializer(serializers.ModelSerializer):
    class Meta: 
        model = BlogUser
        fields = ['name','id']