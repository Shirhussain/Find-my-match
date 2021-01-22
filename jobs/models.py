from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import pre_save, post_save 


# if you want to add some phone number regex or some local state you can use loclaflavor 
# as example here i use US but in the future for Afghanistan i can do the same 
# although it doesn't have Afghanistan right now in the future i will add.
from localflavor.us.models import USStateField

class Job(models.Model):

    title = models.CharField(_("Title"), max_length=200, unique=True)
    slug = models.SlugField(_("Slug"))
    active = models.BooleanField(_("Active"), default=True) #show or not
    flagged = models.ManyToManyField(User, verbose_name=_("Flagged"), blank=True) # warning 
    # users = models.ManyToManyField(User, verbose_name=_(""))

    class Meta:
        verbose_name = _("job")
        verbose_name_plural = _("jobs")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"pk": self.pk})

def pre_save_job(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)
pre_save.connect(pre_save_job, sender=Job)


class Location(models.Model):

    name = models.CharField(_("Name"), max_length=255, unique=True)
    slug = models.SlugField(_("Slug"))
    active = models.BooleanField(_("Active"), default=True)
    flagged = models.ManyToManyField(User, verbose_name=_("Flagged"), blank=True)

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("location_detail", kwargs={"pk": self.pk})

def pre_save_location(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)
pre_save.connect(pre_save_location, sender=Location)


class Employer(models.Model):

    name = models.CharField(_("Name"), max_length=50)
    slug = models.SlugField(_("Slug"))
    location = models.ForeignKey(Location, verbose_name=_("Location"), on_delete=models.CASCADE)
    # state = USStateField(null=True, blank=True)
    # website
    # lat_lang 

    class Meta:
        verbose_name = _("employer")
        verbose_name_plural = _("employers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("employer_detail", kwargs={"pk": self.pk})

def pre_save_employer(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)
pre_save.connect(pre_save_employer, sender=Employer)
