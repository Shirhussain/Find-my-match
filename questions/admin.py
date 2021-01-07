from django.contrib import admin

from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    '''Tabular Inline View for Answer'''

    model = Answer
    min_num = 3
    max_num = 20
    extra = 1
    # raw_id_fields = (,)



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    class Meta:
        model = Question 

admin.site.register(Answer)
