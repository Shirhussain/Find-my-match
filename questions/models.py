from django.db import models
from django.db.models.signals import post_save, pre_save

from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.urls import reverse
from django.dispatch import receiver


class Question(models.Model):
    text = models.TextField(_("Text"))
    active = models.BooleanField(_("Active"), default=True)
    draft  = models.BooleanField(_("Draft"), default=False)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now=False, auto_now_add=True)


    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.text[:10]


class Answer(models.Model):
    """Model definition for Answer."""

    question = models.ForeignKey(Question, verbose_name=_("Question"), on_delete=models.CASCADE)
    text = models.CharField(_("Text"), max_length=250)
    active = models.BooleanField(_("Active"), default=True)
    draft  = models.BooleanField(_("Draft"), default=False)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Answer."""

        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        """Unicode representation of Answer."""
        return self.text[:10]


LEVELS = (
    ('Mandatory', 'Mandatory'),
    ('Very Important', 'Very Important'),
    ('Somewhat Important', 'Somewhat Important'),
    ('Not important', 'Not important'),
)


class UserAnswer(models.Model):

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name=_("Question"), on_delete=models.CASCADE)
    my_answer = models.ForeignKey(Answer, verbose_name=_("Answer"), on_delete=models.CASCADE, related_name="user_answer")
    my_answer_importance = models.CharField(_("My Answer Importance"), max_length=50, choices=LEVELS)
    # to undrestand the weight of every answer we have to measure them with points
    # i put the default value to "-1" it means that our score never hits "-1" and also never gonna be "-1" after we save too
    # because i put it "300, 200, ..." if i put "0" so it clash with my code because i have already defined "0" 
    my_points = models.IntegerField(_("My points"), default=-1, null=True, blank=True) 
    their_answer = models.ForeignKey(Answer, verbose_name=_("Their answer"), 
                                    on_delete=models.CASCADE, 
                                    related_name="match_answer",
                                    null=True, blank=True
                                    )
    their_answer_importance = models.CharField(_("Their answer importants"), max_length=50, choices=LEVELS)
    timestamp = models.DateField(_("Timestamp"), auto_now=False, auto_now_add=True)
    their_points = models.IntegerField(_("My points"), default=-1, blank=True, null=True) 


    class Meta:
        verbose_name = _("useranswer")
        verbose_name_plural = _("useranswers")

    def __str__(self):
        return self.my_answer.text[0:10]

    def get_absolute_url(self):
        return reverse("useranswer_detail", kwargs={"pk": self.pk})


def score_importance(importants_level):
    if importants_level == "Mandatory":
        points = 300 
    elif importants_level == "Very Important":
        points = 200
    elif importants_level == "Somewhat Important":
        points = 50
    elif importants_level == "Not important":
        points = 0
    else:
        points = 0
    return points

@receiver(pre_save, sender=UserAnswer)
def update_user_answer_score(sender, instance, *args, **kwargs):
    my_points = score_importance(instance.my_answer_importance)
    instance.my_points = my_points
    their_points = score_importance(instance.their_answer_importance)
    instance.their_points = their_points
# instead of @receiver you can use the line bellow as well
# pre_save.connect(update_user_answer_score, sender=UserAnswer)

# sender is the model and instance is the instance of model and created is a boolean value
# def update_user_answer_score(sender, instance, created, *args, **kwargs):
# 	# my_points = score_importance(instance.my_answer_importance)
# 	# instance.my_points = my_points
# 	# their_points = score_importance(instance.their_importance)
# 	# instance.their_points = their_points
# 	# instance.save() ## don't save like this
# 	if created:
# 		if instance.my_points == -1:
# 			my_points = score_importance(instance.my_answer_importance)
# 			instance.my_points = my_points
# 			instance.save()

# 		if instance.their_points == -1:
# 			their_points = score_importance(instance.their_answer_importance)
# 			instance.their_points = their_points
# 			instance.save()

# post_save.connect(update_user_answer_score, sender=UserAnswer)