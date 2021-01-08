from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.urls import reverse


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
    ('Very Important', 'ver important'),
    ('Somewhat Important', 'somewhat important'),
    ('Not important', 'not important'),
)


class UserAnswer(models.Model):

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name=_("Question"), on_delete=models.CASCADE)
    my_answer = models.ForeignKey(Answer, verbose_name=_("Answer"), on_delete=models.CASCADE, related_name="user_answer")
    my_answer_importance = models.CharField(_("My Answer Importance"), max_length=50, choices=LEVELS)
    their_answer = models.ForeignKey(Answer, verbose_name=_("Their answer"), 
                                    on_delete=models.CASCADE, 
                                    related_name="match_answer",
                                    null=True, blank=True
                                    )
    their_answer_importance = models.CharField(_("Their answer importants"), max_length=50, choices=LEVELS)
    timestamp = models.DateField(_("Timestamp"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("useranswer")
        verbose_name_plural = _("useranswers")

    def __str__(self):
        return self.my_answer.text[0:10]

    def get_absolute_url(self):
        return reverse("useranswer_detail", kwargs={"pk": self.pk})
