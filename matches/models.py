from django.utils.translation import gettext as _
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime

from .utils import get_match



class MatchManager(models.Manager):
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

    def do_match(self):
        # do match update 
        user_a = self.user_a 
        user_b = self.user_b 
        match_decimal, num_of_questions = get_match(user_a, user_b)
        self.match_decimal = match_decimal
        self.question_answered = num_of_questions
        self.save()
    
    def check_update(self):
        # if update id needed
        now = timezone.now()
        # i'm gonna updated this on every 12 hour
        offset = now - datetime.timedelta(hours=2)
        if self.updated <= offset:
            self.do_match()
        else:
            print("Already updated")

    def __str__(self):
        # return "%.2f" % (self.match_decimal)
        return f'{(self.match_decimal):.2f}'

    def get_absolute_url(self):
        return reverse("match_detail", kwargs={"pk": self.pk})