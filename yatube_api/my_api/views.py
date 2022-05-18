from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import User, Group, Post
from .serializers import GroupSerializer, PostSerializer, \
    UserSerializer, CommentSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_destroy(serializer)


class CommentsListAPIView(APIView):
    def get(self, request, post_id):
        comments = Post.objects.get(pk=post_id).comments
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        serializer = CommentSerializer(data=request.data)
        post = Post.objects.get(pk=post_id)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsDetailAPIView(APIView):
    def get(self, request, post_id, comment_id):
        post = Post.objects.get(pk=post_id)
        comment = post.comments.filter(pk=comment_id).first()
        # ??????? без мени тру не пашет
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, post_id, comment_id):
        post = Post.objects.get(pk=post_id)
        comment = post.comments.filter(pk=comment_id).first()  # дичь
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.instance.author != self.request.user:
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, post_id, comment_id):
        post = Post.objects.get(pk=post_id)
        comment = post.comments.filter(pk=comment_id).first()  # дичь
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            if serializer.instance.author != self.request.user:
                return Response(serializer.data,
                                status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, comment_id):
        post = Post.objects.get(pk=post_id)
        comment = post.comments.filter(pk=comment_id).first()  # дичь
        # ??????? без мени тру не пашет
        serializer = CommentSerializer(comment)
        if serializer.instance.author != self.request.user:
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
