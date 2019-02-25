from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db import models
from django.db.models import Avg
from django.conf import settings
from django.utils.text import slugify
# Create your models here.

class Product(models.Model):
	business_name = models.CharField(max_length = 120)
	logo = models.ImageField(upload_to = 'imagesUploads/logos/')
	desc = models.TextField()
	link = models.URLField()
	slug = models.SlugField(unique = True, null = True)
	tags = models.ManyToManyField('Tag')
	category = models.ForeignKey('Category', null = True)
	featured = models.BooleanField(default = False)
	active = models.BooleanField(default = True)
	views = models.PositiveIntegerField(default = 0)
	updated = models.DateTimeField(auto_now_add = True, editable = False)
	created = models.DateTimeField(auto_now = True, editable = False)
	rate = models.FloatField(null = True)

	def __str__(self):
		return self.business_name

	def get_absolue_url(self):
		return reverse ('review_product_detail', kwargs={'slug': self.slug})

	def get_reviewscore(self):
		review_avg = self.review_set.all().aggregate(Avg('score'))
		return review_avg.values()

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super(Product, self).save(*args, **kwargs)

	#we are nbnot aggregating on the save method because of race condition





class Review(models.Model):
	post = models.ForeignKey(Product)
	score = models.FloatField()
	comment = models.TextField()
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	updated = models.DateTimeField(auto_now_add = True, editable = False)
	created = models.DateTimeField(auto_now = True, editable = False)

	def __str__(self):
		return self.comment

	def get_absolute_url(self):
		return reverse ('review_detail', kwargs={'pk':self.id})




class Tag(models.Model):
	name = models.CharField(max_length = 40, null = True)
	slug = models.SlugField(unique = True, null = True)
	updated = models.DateTimeField(auto_now_add = True, editable = False)
	created = models.DateTimeField(auto_now = True, editable = False)

	def __str__(self):
		return self.name


class Category(models.Model):
	name = models.CharField(max_length = 50, null = True)
	slug = models.SlugField(unique = True, null = True)
	updated = models.DateTimeField(auto_now_add = True, editable = False)
	created = models.DateTimeField(auto_now = True, editable = False)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def get_productscore(self):
		nviews = self.product_set.all().aggregate(Avg('views'))
		return nviews.items()

	def get_absolute_url(self):
		return reverse('nav_categories', kwargs = {'slug': self.slug})


class ReviewProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	myname = models.CharField(max_length=30, null=True, blank = True)
	completeprofile = models.BooleanField(default = False, editable = False)
	searched = models.BooleanField(default = False, editable = False)
	headshot = models.ImageField(upload_to = "imagesUploads/headshots")
	bio = models.TextField(null=True, blank=True)
	updated = models.DateTimeField(auto_now_add = True, editable = False)
	created = models.DateTimeField(auto_now = True, editable = False)

	def get_absolute_url(self):
		return reverse('mprofile')

	def save(self, *args, **kwargs):
		try:
			this = ReviewProfile.objects.get(id = self.id)
			if this.headshot != self.headshot:
				this.headshote.delete(save = False)
		except:
			pass
		super(ReviewProfile, self).save(*args, **kwargs)

class FavoriteReview(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	item = models.ForeignKey(Review)
	updated = models.DateTimeField(auto_now_add = True, editable = False)
	created = models.DateTimeField(auto_now = True, editable = False)