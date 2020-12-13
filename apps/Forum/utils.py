from apps.UserMechanics.models import ActionPostLike


def is_post_liked(post, user):
    if not user.is_authenticated:
        return False
    return ActionPostLike.objects.filter(autor = user).filter(post = post).exists()