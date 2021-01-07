from django.db import models
from django.utils.translation import gettext as _


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
