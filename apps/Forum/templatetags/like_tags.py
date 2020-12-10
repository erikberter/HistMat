from django import template
from apps.UserMechanics.models import ActionPostLike
from apps.Forum.utils import *

register = template.Library()

@register.simple_tag
def is_liked(post, user):
    return is_post_liked(post, user)

        