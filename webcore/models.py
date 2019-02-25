from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
 
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    photo = models.ImageField(upload_to='profile_photo', null=True)
 
    def __str__(self):
        return "{}'s profile".format(self.user.username)
 
    class Meta:
        db_table = 'user_profile'
 
    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False
    # def profile_image_url(self):

    # 	fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
    # 	if len(fb_uid):
    #     	return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)
 
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

# Create your models here.
class EmailMarketingSignUp(models.Model):
	email = models.EmailField()
	created = models.DateTimeField(auto_now = True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now = False, auto_now_add=True)
	active = models.BooleanField(default = False)

	def __str__(self):
		return self.email


class Banner(models.Model):
	title = models.CharField(max_length = 30)
	desc = models.CharField(max_length = 60)
	btn_link = models.URLField()
	btn_title = models.CharField(max_length = 18)
	created = models.DateTimeField(auto_now = True, auto_now_add=False)
	updated = models.DateTimeField(auto_now = False, auto_now_add=True)


class Contact(models.Model):
	name = models.CharField(max_length = 30, null=True)
	email =models.EmailField()
	subject = models.CharField(max_length = 30)
	content = models.TextField()
	created = models.DateTimeField(auto_now = True, auto_now_add=False)
	updated = models.DateTimeField(auto_now = False, auto_now_add=True)

	def __str__(self):
		return( '%s - %s', self.email, self.subject)

class EmailMarketingConfirmed(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	activation_key = models.CharField(max_length=200)
	confirmed = models.BooleanField(default=False)

	def __str__(self):
		return self.confirmed

	def activate_user_email(self):
		activation_url = "%s%s" %(settings.SITE_URL, reverse("marketingactivation_view", args[self.activation_key]))
		context = {
			"activation_key": self.activation_key,
			"activation_url": activation_url,
			"user": self.user.first_name,
		}
		message = render_to_string("newslettersignup/activation_message.txt", context)
		subject = "Activate your email"
		self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.user.email], kwargs)

class About_website(models.Model):
	name  = models.CharField(max_length = 100)
	logo = models.ImageField(upload_to="website_logo")
	about = models.TextField()
	address = models.CharField(max_length=100)
	tel = models.CharField(max_length = 50)
	email = models.EmailField()

	def clean(self):
		validate_only_one_instance(self)


def validate_only_one_instance(obj):
	model = obj.__class__
	if (model.objects.count() > 0 and obj.id != model.objects.get().id):
		raise ValidationError("Can only create on instance of %s" % model.__name__)