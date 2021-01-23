from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db import models
from django.urls import reverse
from decimal import Decimal
import datetime


from .utils import get_match
from .signals import user_matches_update
from jobs.models import Job, Location, Employer

# get_or_create looking for two user now i'm goging to look just for one of them.
class MatchQuerySet(models.query.QuerySet):
    def matches(self, user):
        q1 = self.filter(user_a=user).exclude(user_b=user)
        q2 = self.filter(user_b=user).exclude(user_a=user)
        return (q1|q2).distinct()

class MatchManager(models.Manager):

    def get_queryset(self):
        return MatchQuerySet(self.model, using=self._db)

    def get_or_create_match(self, user_a=None, user_b=None):
        try:
            obj = self.get(user_a=user_a, user_b=user_b)
        except:
            obj = None 
        try:
            obj2 = self.get(user_a=user_b, user_b=user_a)
        except:
            obj2 = None 
        # now we should know that whater it's created or not 
        if obj and not obj2:
            # it means that it's not creating it's getting it.
            # obj is gonna be the instance which that's returning and obj exist but obj2 does not exits
            # because we are using get or create that's the only possibility. 
            obj.check_update()
            return obj, False
        elif not obj and obj2: 
            # it means that it wasn't created
            obj2.check_update()
            return obj2, False
        else:
            # now i'm creating an instance
            # the line bellow if you reverse the 'user_a' and 'user_b' places also it doesn't matter 
            # because of the try and except that i implemented before
            new_instance = self.create(user_a=user_a, user_b=user_b)
            # do match
            new_instance.do_match()
            # match_decimal, num_of_questions = get_match(user_a, user_b)
            # new_instance.match_decimal = match_decimal
            # new_instance.question_answered = num_of_questions
            # new_instance.save()
            return new_instance, True
    
    # this is gonna update all the matches for the user that they already have
    # it's not creating it's just updating for every single user
    def update_for_user(self, user):
        qs = self.get_queryset().matches(user)
        for instance in qs:
            instance.do_match()
        return True

    def update_all(self):
        queryset = self.all()
        # i don't wanna available this for every match, just wanna implement for specific time
        now = timezone.now()
        offset = now - datetime.timedelta(hours=12)
        offset2 = now - datetime.timedelta(hours=36)
        queryset.filter(updated__gt=offset2).filter(updated__lte=offset)
        if queryset.count > 0:
            for i in queryset:
                i.check_update()

    def get_matches(self, user):
        qs = self.get_queryset().matches(user).order_by('-match_decimal')
        matches = []
        for match in qs:
            if match.user_a == user:
                items_wanted = [match.user_b]
                matches.append(items_wanted)
            elif match.user_b == user:
                items_wanted = [match.user_a]
                matches.append(items_wanted)
            else:
                pass 
        return matches

    def get_matches_with_percent(self, user):
        qs = self.get_queryset().matches(user).order_by('-match_decimal')
        matches = []
		# id don't wanna show my percentage for my self as well so for that reason i have to implement this
        for match in qs:
            if match.user_a == user:
                items_wanted = [match.user_b, match.get_percent]
                matches.append(items_wanted)
            elif match.user_b == user:
                items_wanted = [match.user_a, match.get_percent]
                matches.append(items_wanted)
            else:
                pass 
        return matches


class Match(models.Model):

    user_a = models.ForeignKey(User, verbose_name=_("User A"), related_name="match_user_a", on_delete=models.CASCADE)
    user_b = models.ForeignKey(User, verbose_name=_("User B"), related_name="match_user_b", on_delete=models.CASCADE)
    match_decimal = models.DecimalField(_("Percentage"), max_digits=16, decimal_places=8, default=0.00) #default is zero no question answered
    question_answered = models.IntegerField(_("Answered Question"), default=0)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)
    
    class Meta:
        verbose_name = _("match")
        verbose_name_plural = _("matchs")

    objects = MatchManager()

    @property
    def get_percent(self):
        new_decimal = Decimal(self.match_decimal) * Decimal(100)
        return f'{new_decimal:.2f}%'

    def do_match(self):
        # do match update 
        user_a = self.user_a 
        user_b = self.user_b 
        match_decimal, num_of_questions = get_match(user_a, user_b)
        self.match_decimal = match_decimal
        self.question_answered = num_of_questions
        self.save()
        # what if i don't have already positions --> so do the following
        PositionMatch.objects.update_top_suggestions(self.user_a, 6)
        PositionMatch.objects.update_top_suggestions(self.user_b, 6)
    
    def check_update(self):
        # if update id needed
        now = timezone.now()
        # i'm gonna updated this on every 12 hour
        offset = now - datetime.timedelta(hours=12)
        if self.updated <= offset or self.match_decimal == 0.00:
            self.do_match()
        else:
            print("Already updated")

    def __str__(self):
        # return "%.2f" % (self.match_decimal)
        return f'{(self.match_decimal):.2f}'

    def get_absolute_url(self):
        return reverse("match_detail", kwargs={"pk": self.pk})


def user_matches_update_receiver(sender, user, *args, **kwargs):
    updated = Match.objects.update_for_user(user)
    print(updated)

user_matches_update.connect(user_matches_update_receiver)


class PositionMatchManager(models.Manager):
    def update_top_suggestions(self, user, match_int):
        matches = Match.objects.get_matches(user)[:match_int]
        for match in matches:
			# the above line bring match user object and percent but i want the first one which is match user
            job_set = match[0].userjob_set.all()
            if job_set.count()>0:
                for job in job_set:
                    try:
                        the_job = Job.objects.get(title__iexact=job.position)
                        positionmatch, created = self.get_or_create(user=user, job=the_job)
                    except:
                        pass
                    try:
                        the_loc = Location.objects.get(name__iexact=job.location)
                        locmatch, created = LocationMatch.objects.get_or_create(user=user, location = the_loc)
                    except:
                        pass 
                    try:
                        the_employer = Employer.objects.get(name__iexact=job.employer_name)
                        employermatch = EmployerMatch.objects.get_or_create(user=user, employer=the_employer)
                    except:
                        pass


class PositionMatch(models.Model):

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    job = models.ForeignKey(Job, verbose_name=_("Job"), on_delete=models.CASCADE)
    hidden = models.BooleanField(_("Hidden"), default=False)
    liked = models.BooleanField(_("Liked"), null=True) # liked or saved
    updated = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

    objects = PositionMatchManager()

    def check_update(self, match_int):
        now = timezone.now()
        offset = now - datetime.timedelta(hours=12)
        if self.updated <= offset:
            PositionMatch.objects.update_top_suggestions(self.user, match_int)


    class Meta:
        verbose_name = _("PositionMatch")
        verbose_name_plural = _("PositionMatchs")

    def __str__(self):
        return self.job.title

    @property
    def get_match_url(self):
        return reverse("matches:PositionMatch_detail", kwargs={"slug": self.job.slug})



class EmployerMatch(models.Model):

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, verbose_name=_("Employer"), on_delete=models.CASCADE)
    hidden = models.BooleanField(_("Hidden"), default=False)
    liked = models.BooleanField(_("Liked"), null=True)
    
    class Meta:
        verbose_name = _("EmployerMatch")
        verbose_name_plural = _("EmployerMatchs")

    def __str__(self):
        return self.user.username

    @property
    def get_match_url(self):
        return reverse("matches:EmployerMatch_detail", kwargs={"slug": self.employer.slug})


class LocationMatch(models.Model):

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    location = models.ForeignKey(Location, verbose_name=_("Location"), on_delete=models.CASCADE)
    hidden = models.BooleanField(_("Hidden"), default=False)
    liked = models.BooleanField(_("Liked"), null=True)

    class Meta:
        verbose_name = _("LocationMatch")
        verbose_name_plural = _("LocationMatchs")

    def __str__(self):
        return self.user.username

    @property
    def get_match_url(self):
        return reverse("matches:LocationMatch_detail", kwargs={"slug": self.location.slug})
