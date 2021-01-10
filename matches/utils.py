from django.contrib.auth import get_user_model
from decimal import Decimal

from questions.models import UserAnswer

# new algorithm 
def get_points(user_a, user_b):
	a_answers = UserAnswer.objects.filter(user=user_a)
	b_answers = UserAnswer.objects.filter(user=user_b)
	a_total_award=0
	a_points_possible=0
	num_question=0
	for a in a_answers:
		for b in b_answers:
			num_question += 1
			if a.question.id == b.question.id:
				a_pref = a.their_answer
				b_answer = b.my_answer
				if a_pref == b_answer:
					'''
					award points for current answer
					'''
					a_total_award += a.their_points
				'''
				assigning total points
				'''
				a_points_possible += a.their_points
	print(f"{user_a} has awarded {a_total_award} points {a_points_possible} to {user_b}")
	percent = a_total_award/Decimal(a_points_possible)
	print("The percentage: ", percent)
	print("The numer ob questions: ", num_question)
	# some time if we don't have nay match so our percentage is "0" then if we put 0 to our formola
	# it defiantly make everything equal to 0 so it's better to give it a small number which is equal to 0
	if percent == 0:
		percent = 0.000000001
	return percent, num_question


def get_match(user_a, user_b):
    a = get_points(user_a, user_b)
    b = get_points(user_b, user_a)
    # bot 'a' and 'b' which is get_points return two value --> percent and num_question
    # her i'm gonna user geometric mean
    # a[0]=decimal match value
    number_of_questions = b[1] # a[1] or b[1] is number of question answered 
    # match_decimal it means it's percentage
    match_decimal = (Decimal(a[0])*Decimal(b[0]))**(1/Decimal(number_of_questions)) #geometric mean in respeacts to number ob question answered
    return match_decimal, number_of_questions
