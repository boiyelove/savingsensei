from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from .forms import ContactForm, NewsletterForm

# Create your views here.
def index(request):

	return render(request, template, context)
	
def about(request):
	template = 'about.html'
	context = {'page_title' : 'About US'}
	return render(request, template, context)

def newsletter_signup(request):
	source = request.META.get('HTTP_REFERER')
	news_signup = NewsletterForm(request.POST or None)
	if news_signup.is_valid():
		email = news_signup.clean_data.get('email')
		obj, created = EmailMarketingSignUp.objects.get_or_create(email = email)
		if created:
			messages.success(request, "You are now on our list, you'll hear from us from time to time")
		elif not created and obj:
			messages.success(request, "You already subscribed to our list. We'll now send you updates")
		else:
			messages.error(request, "Oh! something went wrong. Sorry about that.")
	else:
		messages.error(request, "Oh! something went wrong. Sorry about that.")
	return HttpResponseRedirect(source)

def contact(request):
	new_contact = ContactForm(request.POST or None)
	if new_contact.is_valid():
		new_contact.save()
		messages.success(request, "Thank you for contacting us, we'll reply to your enquiry as soon as we can")
		return HttpResponseRedirect('/')
	if new_contact.errors:
		messages.warning(request, "Sorry Something went wrong")
	template = 'contact.html'
	context = {'contactform' : new_contact}
	return render(request, template, context)



def handler400(request):
	template = '400.html'
	context = {}
	return render(request, template, context)

def handler403(request):
	template = '403.html'
	context = {}
	return render(request, template, context)

def handler404(request):
	template = '404.html'
	context = {}
	return render(request, template, context)

def handler500(request):
	template = '500.html'
	context = {}
	return render(request, template, context)
