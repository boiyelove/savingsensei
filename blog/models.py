from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from reviews.models import Tag
# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length = 120, null=True)
	tagline = models.CharField(max_length = 120, null=True)
	slug = models.SlugField(unique = True, null=True)
	image = models.ImageField(upload_to = 'imagesUploads/blog/', null=True,)
	tags = models.ManyToManyField(Tag, related_name = 'blog_tags')
	category = models.ForeignKey('BlogCategory', related_name = 'blog_category', null=True)
	content = models.TextField(null=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
	updated = models.DateTimeField(auto_now_add = True, editable=False)
	created = models.DateTimeField(auto_now = True, editable=False)
	views = models.PositiveIntegerField(default=0, editable=False)


	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('post_detail', kwargs= {'slug': self.slug})

	def __str__(self):
		return self.title

class BlogCategory(models.Model):
	name = models.CharField(max_length = 30)
	slug = models.SlugField(unique = True)
	updated = models.DateTimeField(auto_now_add = True, editable=False)
	created = models.DateTimeField(auto_now = True, editable=False)
	views = models.PositiveIntegerField(default=0, editable=False)


class Comment(models.Model):
	post = models.ForeignKey(Post)
	body = models.CharField(max_length = 600)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
	updated = models.DateTimeField(auto_now_add = True, editable=False)
	created = models.DateTimeField(auto_now = True, editable=False)

	def __str__(self):
		return self.comment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   



