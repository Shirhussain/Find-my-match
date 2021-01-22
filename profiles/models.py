from django.db.models.signals import post_save, pre_save
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.urls import reverse

from jobs.models import Job, Location, Employer

def upload_location(instance, filename):
    # extention = filename.split(".")[1]   #if you want to extract the extention as will
    username = str(instance.user.username)
    # return "%s/%s" %(username, filename)
    # return f"{username}/profile.{extention}"
    return f"{username}/{filename}"


class Profile(models.Model):
    """Model definition for Profile."""

    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    picture = models.ImageField(_("Picture"), upload_to=upload_location,
                                default="avatar.jpeg",
                                height_field=None, 
                                width_field=None, 
                                max_length=None,
                                blank=True, null=True
                                )
    location = models.CharField(_("Location"), max_length=100, null=True, blank=True)

    class Meta:
        """Meta definition for Profile."""

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Unicode representation of Profile."""
        return self.user.username
    
    def get_absolute_url(self):
        return reverse("profiles:profile", kwargs={"username": self.user.username})
    

# why i don't use foreign key? because jobs.models are just for our own  taging of diffrent jobs
# when we add a job also we add those three models and that's the only time we add those staff.
class UserJob(models.Model):

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    position = models.CharField(_("Position"), max_length=50)
    location = models.CharField(_("Location"), max_length=50)
    employer_name = models.CharField(_("Employer Name"), max_length=50)

    class Meta:
        verbose_name = _("userjob")
        verbose_name_plural = _("userjobs")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("userjob_detail", kwargs={"pk": self.pk})


def post_save_user_job(sender, instance, created, *args, **kwargs):
    job = instance.position.lower() 
    location = instance.location.lower()
    employer_name = instance.employer_name.lower()
    new_job, created = Job.objects.get_or_create(title=job)
    new_location, created = Location.objects.get_or_create(name=location)
    new_employer = Employer.objects.get_or_create(name=employer_name, location=new_location) 

post_save.connect(post_save_user_job, sender=UserJob)
