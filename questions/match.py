from django.contrib.auth import get_user_model
from decimal import Decimal

from questions.models import UserAnswer


User = get_user_model()

users = User.objects.all() #[user1, user2,]
all_user_answers = UserAnswer.objects.all().order_by("user__id") #[useranswer1, useranswer2,]


shir = users[0]
amir = users[1]
bill = users[2]
elon = users[3]
jef = users[4]


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

a = get_points(shir, elon)
b = get_points(jef, bill)
c = get_points(elon, jef)
d = get_points(shir,jef)
e = get_points(bill, jef)

# This is based on "geometic mean"
# when i use power her so ust need to take the number of question so i use a[1] 
# i doesn't matter what ever you choose a,b,c.. just to take the number
# match_percentage = f'{(Decimal(a[0])*Decimal(b[0])*Decimal(c[0])*Decimal(d[0])*Decimal(e[0]))**(1/Decimal(a[1])):.2f}'
match_percentage = "%.2f" % (Decimal(a[0])*Decimal(b[0])*Decimal(c[0])*Decimal(d[0])*Decimal(e[0]))**(1/Decimal(a[1]))


# the old way 
# UserAnswer.objects.filter(user=shir)
# UserAnswer.objects.filter(user=elon)


# shir_ans1 = shir.useranswer_set.all()[0]
# elon_ans1 = elon.useranswer_set.all()[0]


# shir_ans1.question.id == elon_ans1.question.id

# shir_answer = shir_ans1.my_answer

# shir_pref = shir_ans1.their_answer

# elon_answer = elon_ans1.my_answer

# elon_pref = elon_ans1.their_answer


# shir_answer == elon_pref
# shir_pref == elon_answer


# def get_match(user_a, user_b):
# 	user_a_answers = UserAnswer.objects.filter(user=user_a)[0]
# 	user_b_answers = UserAnswer.objects.filter(user=user_b)[0]
# 	if user_a_answers.question.id == user_b_answers.question.id:
# 		user_a_answer = user_a_answers.my_answer
# 		user_a_pref = user_a_answers.their_answer
# 		user_b_answer = user_b_answers.my_answer
# 		user_b_pref = user_b_answers.their_answer
# 		user_a_total_award=0
# 		user_b_total_award=0
# 		if user_a_answer == user_b_pref:
# 			user_b_total_award += user_a_answers.their_points
# 			print(f" {user_a} fits with {user_b}")
# 		if user_a_pref == user_b_answer:
# 			user_a_total_award += user_b_answers.their_points
# 			print(f"{user_a} fits with user {user_b}")
# 		if user_a_answer == user_b_pref and user_a_pref == user_b_answer:
# 			print(f"both {user_a} and {user_b} ideal with each other")
# 		print(user_a, user_a_total_award, user_b)
# 		print(user_b, user_b_total_award, user_a)


# get_match(shir, elon)
# get_match(shir, bill)
# get_match(shir, jef)
# get_match(jef,elon)
# get_match(bill, jef)
