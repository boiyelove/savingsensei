from django import forms
from django.contrib.auth.models import User
from .models import Product, Review, ReviewProfile


class ReviewForm(forms.ModelForm):

	class Meta:
		model = Review
		fields = ['comment', 'score']

class ProductForm(forms.ModelForm):

	class Meta:
		model = Product
		exclude = ['views', 'created', 'updated']

class ReviewProfileForm(forms.ModelForm):

	class Meta:
		model = ReviewProfile
		exclude = ['user', 'updated', 'created', 'searched', 'completeprofile']