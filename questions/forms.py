from django import forms 
from .models import LEVELS, Question, Answer

class UserResponseForm(forms.Form):
    question_id = forms.IntegerField()
    answer_id = forms.IntegerField()
    importants_level = forms.ChoiceField(choices=LEVELS)
    their_answer_id = forms.IntegerField()
    their_importants_level = forms.ChoiceField(choices=LEVELS)

    def clean_question_id(self):
        question_id = self.cleaned_data.get('question_id')
        try:
            obj = Question.objects.get(id=question_id)
        except:
            raise forms.ValidationError("There was an error with this question please try again.")
        return question_id

    def clean_answer_id(self):
        answer_id = self.cleaned_data.get('answer_id')
        try:
            obj = Answer.objects.get(id=answer_id)
        except:
            raise forms.ValidationError("There was an error with Answer pleas try again")
        return answer_id

    def clean_their_answer_id(self):
        their_answer_id = self.cleaned_data.get('their_answer_id')
        try:
            obj = Answer.objects.get(id=their_answer_id)
        except:
            raise forms.ValidationError("There was an error with the answer you provide for them.")
        return their_answer_id
