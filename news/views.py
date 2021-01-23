from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail

from news.forms import ContactForm, SignUpForm
from news.models import SignUp
from questions.models import Question
from matches.models import Match, LocationMatch, PositionMatch, EmployerMatch
from jobs.models import Job, Employer, Location
from likes.models import UserLike

# Create your views here.
def home(request):
	title = 'Sign Up Now'
	form = SignUpForm(request.POST or None)
	context = {
		"title": title,
		"form": form
	}
	if form.is_valid():
		instance = form.save(commit=False)

		full_name = form.cleaned_data.get("full_name")
		if not full_name:
			full_name = "New full name"
		instance.full_name = full_name
		instance.save()
		context = {
			"title": "Thank you"
		}

	if request.user.is_authenticated:
		# PositionMatch.objects.update_top_suggestions(request.user, 20)
		matches = Match.objects.get_matches_with_percent(request.user)[:6]
		positions = PositionMatch.objects.filter(user=request.user)[:6]
		if positions.count()>0:
			# [0] --> because i need just the user position --> if you want to check just preint it
			positions[0].check_update(20) #20 match total
		locations = LocationMatch.objects.filter(user=request.user)[:6]
		employers = EmployerMatch.objects.filter(user=request.user)[:6]
		# suggested jobs, location and employer
		# positions = []
		# locations = []
		# employers = [] 
		# for match in matches: 
		# 	# the above line bring match user object and percent but i want the first one which is match user
		# 	job_set = match[0].userjob_set.all()
		# 	if job_set.count()>0:
		# 		for job in job_set:
		# 			if job.position not in positions:
		# 				positions.append(job.position)
		# 				try:
		# 					the_job = Job.objects.get(title__iexact=job.position)
		# 					positionmatch, created = PositionMatch.objects.get_or_create(user=request.user, job=the_job)
		# 					print("Job match are: ", positionmatch)
		# 				except:
		# 					pass
		# 			if job.location not in locations:
		# 				locations.append(job.location)
		# 				try:
		# 					the_loc = Location.objects.get(name__iexact=job.location)
		# 					locmatch, created = LocationMatch.objects.get_or_create(user=request.user, location = the_loc)
		# 					print("Local match are: ", locmatch)
		# 				except:
		# 					pass 
		# 			if job.employer_name not in employers:
		# 				employers.append(job.employer_name)
		# 				try:
		# 					the_employer = Employer.objects.get(name__iexact=job.employer_name)
		# 					employermatch = EmployerMatch.objects.get_or_create(user=request.user, employer=the_employer)
		# 					print("Employer match are: ", employermatch)
		# 				except:
		# 					pass


		queryset = Question.objects.all().order_by('-timestamp') 
		context = {
			"queryset": queryset, 
			'matches': matches,
			'positions': positions,
			'locations': locations,
			'employers': employers,
		}
		return render(request, "questions/home.html", context)

	return render(request, "home.html", context)


def contact(request):
	title = 'Contact Us'
	title_align_center = True
	form = ContactForm(request.POST or None)
	if form.is_valid():
		# for key, value in form.cleaned_data.iteritems():
		# 	print key, value
		# 	#print form.cleaned_data.get(key)
		form_email = form.cleaned_data.get("email")
		form_message = form.cleaned_data.get("message")
		form_full_name = form.cleaned_data.get("full_name")
		# print email, message, full_name
		subject = 'Site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'youotheremail@email.com']
		contact_message = "%s: %s via %s"%( 
				form_full_name, 
				form_message, 
				form_email)
		some_html_message = """
		<h1>hello</h1>
		"""
		send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, 
				html_message=some_html_message,
				fail_silently=True)

	context = {
		"form": form,
		"title": title,
		"title_align_center": title_align_center,
	}
	return render(request, "forms.html", context)



def about(request):
	return render(request, "about.html", {})