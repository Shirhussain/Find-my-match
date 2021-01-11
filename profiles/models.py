from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

def upload_location(instance, filename):
    # extention = filename.split(".")[1]   #if you want to extract the extention as will
    username = str(instance.user.username)
    # return "%s/%s" %(username, filename)
    # return f"{username}/profile.{extention}"
    return f"{username}/{filename}"


class Profile(models.Model):
    """Model definition for Profile."""

    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    picture = models.ImageField(_("Picture"), upload_to=upload_location, height_field=None, width_field=None, max_length=None)
    location = models.CharField(_("Location"), max_length=100, null=True, blank=True)

    class Meta:
        """Meta definition for Profile."""

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Unicode representation of Profile."""
        return self.user.username
