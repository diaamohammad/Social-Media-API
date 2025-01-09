from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import User, Post, Follow
from .serializers import UserSerializer, PostSerializer, FollowSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        # إظهار المنشورات الخاصة بالمستخدم فقط
        return Post.objects.filter(user=self.request.user)

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        following_user = User.objects.get(id=pk)
        if request.user == following_user:
            return Response({'error': 'لا يمكنك متابعة نفسك!'}, status=400)
        follow, created = Follow.objects.get_or_create(follower=request.user, following=following_user)
        return Response({'status': 'متابعة تم بنجاح'}, status=201)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        following_user = User.objects.get(id=pk)
        follow = Follow.objects.filter(follower=request.user, following=following_user)
        follow.delete()
        return Response({'status': 'إلغاء المتابعة تم بنجاح'}, status=200)
