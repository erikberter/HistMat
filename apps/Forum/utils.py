from django import template
from apps.UserMechanics.models import ActionPostLike


def is_post_liked(post, user):
    return ActionPostLike.objects.filter(autor = user).filter(post = post).exists()