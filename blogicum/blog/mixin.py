from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Post, Comment


class PostVisibilityMixin:
    """Миксин для проверки видимости поста."""

    def check_post_visibility(self, post, user):
        if user == post.author:
            return True
        if not post.is_published or post.pub_date > now():
            return False
        if not post.category.is_published:
            return False
        return True


class AuthorRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки авторства объекта, у которого есть поле 'author'."""

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author


class SinglePostObjectMixin:
    """Миксин для получения поста по pk или post_pk."""

    def get_post(self):
        post_id = self.kwargs.get('post_pk') or self.kwargs.get('pk')
        return get_object_or_404(Post, pk=post_id)

    def get_object(self, queryset=None):
        return self.get_post()


class SingleCommentObjectMixin:
    """Миксин для получения комментария по comment_pk и post_pk."""

    def get_comment(self):
        comment_id = self.kwargs.get('comment_pk')
        post_id = self.kwargs.get('post_pk') or self.kwargs.get('pk')
        return get_object_or_404(Comment, id=comment_id, post__pk=post_id)

    def get_object(self, queryset=None):
        return self.get_comment()
