from django.utils.translation import gettext as _
from django.db import models
from django.contrib.auth.models import User


class UserLikeManager(models.Manager):
	def get_all_mutual_likes(self, user):
		qs = user.liker.liked_users.all()
		mutual_users = []
		for other_user in qs:
			try:
				if other_user.liker.get_mutual_like(user):
					mutual_users.append(other_user)
			except:
				pass
		return mutual_users


class UserLike(models.Model):
    """Model definition for UserLike."""

    user = models.OneToOneField(User, verbose_name=_("User"), related_name="liker", on_delete=models.CASCADE)
    liked_users = models.ManyToManyField(User, verbose_name=_("Liked users"), related_name="liked_users")

    def get_mutual_like(self, user_b):
        i_like = False
        you_like = False
        if user_b in self.liked_users.all():
            i_like = True
        liked_user, created = UserLike.objects.get_or_create(user=user_b)
        if self.user in liked_user.liked_users.all():
            you_like = True
        if i_like and you_like:
            return True
        else:
            return False
    
    objects = UserLikeManager()

    class Meta:
        """Meta definition for UserLike."""

        verbose_name = 'UserLike'
        verbose_name_plural = 'UserLikes'

    def __str__(self):
        """Unicode representation of UserLike."""
        return self.user.username
