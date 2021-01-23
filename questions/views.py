from django.shortcuts import Http404, get_object_or_404, redirect, render, reverse
from .models import Question, Answer, UserAnswer 
from .forms import UserResponseForm

def single(request, id):
    if request.user.is_authenticated:
        queryset = Question.objects.all().order_by('-timestamp')
        instance = get_object_or_404(Question, id=id)

        # we are working with pre existing UserAnswer or creating a new one 
        # and that's what try block is going to do for us
        try:
            user_answer = UserAnswer.objects.get(user=request.user, question=instance)
        except UserAnswer.DoesNotExist:
            user_answer = UserAnswer()
        except UserAnswer.MultipleObjectsReturned:
            user_answer = UserAnswer.objects.filter(user=request.user, question=instance)[0]
        except:
            user_answer = UserAnswer()

        form = UserResponseForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
            print("This is the request: ",request.POST)
            # question_id = form.cleaned_data.get('question_id')
            # answer_id = form.cleaned_data.get('answer_id')
            # question_instance = Question.objects.get(id=question_id)
            # answer_instance = Answer.objects.get(id=answer_id)
            # or you can do as follows as well

            question_id = form.cleaned_data['question_id']
            answer_id = form.cleaned_data['answer_id'] 
            importants_level = form.cleaned_data['importants_level']
            their_answer_id = form.cleaned_data['their_answer_id']
            their_importants_level = form.cleaned_data['their_importants_level']

            question_instance = Question.objects.get(id=question_id)
            answer_instance = Answer.objects.get(id=answer_id)
            
            user_answer = UserAnswer()
            user_answer.user = request.user
            user_answer.question = question_instance
            user_answer.my_answer = Answer.objects.get(id=answer_id)
            user_answer.my_answer_importance = importants_level
            if their_answer_id != -1:
                their_answer_instance = Answer.objects.get(id=their_answer_id)
                user_answer.their_answer = their_answer_instance
                user_answer.their_answer_importance = their_importants_level
            else:
                user_answer.their_answer = None
                user_answer.their_answer_importance = "not important"
            user_answer.save()

            next_q = Question.objects.get_unanswered(request.user).order_by('?')
            if next_q.count()>0:
                next_q_instance = next_q.first()
                return redirect(reverse("questions:single", kwargs = {'id':next_q_instance.id})) 
            else:
                return redirect(reverse("home"))

        context = {
            'form': form,
            'instance': instance,
            'user_answer': user_answer
        }
        return render(request, "questions/single.html", context)
    else:
        raise Http404


def home(request):
    if request.user.is_authenticated:
        form = UserResponseForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
            # question_id = form.cleaned_data.get('question_id')
            # answer_id = form.cleaned_data.get('answer_id')
            # question_instance = Question.objects.get(id=question_id)
            # answer_instance = Answer.objects.get(id=answer_id)
            question_id = form.cleaned_data['question_id']
            answer_id = form.cleaned_data['answer_id']
            question_instance = Question.objects.get(id=question_id)
            answer_instance = Answer.objects.get(id=answer_id)
            print(question_instance.text)
            print(answer_instance.text)
        queryset = Question.objects.all().order_by('-timestamp')
        instance = queryset[1]
        context = {
            'form': form,
            'instance': instance
        }
        return render(request, "questions/home.html", context)
    else:
        raise Http404

