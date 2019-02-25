import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View, DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ReviewForm, ProductForm, ReviewProfileForm
from .models import Product, Review, Tag, Category, ReviewProfile

# Create your views here.
def search(request):
	if request.GET:
		searchitem = request.GET['q']
		product = Product.objects.filter(business_name__iexact = searchitem )
		paginated = Paginator(product, 6)
		page = request.GET.get('page')
		try:
			postlist = paginated.page(page)
		except PageNotAnInteger:
			postlist = paginated.page(1)
		except EmptyPage:
			postlist = paginated.page(page.num_page)
	page_title = 'Search results for ' + searchitem
	revws = Product.objects.order_by('-created')[:5]
	categories = Category.objects.all()[:5]
	topreviews = Product.objects.order_by('views')[:4]
	template = 'search.html'
	context = {'results' : postlist,
				'recentreviews': revws,
				'categories': categories,
				'topreviews': topreviews,
			'page_title': page_title}
	return render(request, template, context)

class DashboardView(LoginRequiredMixin, TemplateView):
	template_name = 'dashboard.html'

	def get_context_data(self, **kwargs):
		context = super(DashboardView, self).get_context_data(**kwargs)
		user = self.request.user
		context['review_count'] = Review.objects.filter(author = user).count()
		return context


class IndexView(TemplateView):
	template_name = 'frontpage.html'

	def get_context_data(self, *args, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['page_title'] = 'Home'
		context['newlyadded'] = Product.objects.all().order_by('created')[:12]
		context['popularreviews'] = Product.objects.all().order_by('views')[:12]
		context['featured'] = Product.objects.filter(featured = True)
		return context


class CreateProduct(LoginRequiredMixin, CreateView):
	model = Product
	fields = ['business_name', 'logo', 'desc', 'link',]
	template_name = ''

	def get_success_url(self):
		return reverse ('review_product_detail')


class ProductList(ListView):
	model = Product
	context_object_name = 'all_products'
	template_name = "reviews/all_post.html"


class ProductDetail(DetailView):
	model = Product
	template_name = "single.html"
	context_object_name = "product"

	def get_context_data(self, **kwargs):
		context = super(ProductDetail, self).get_context_data(**kwargs)
		context['recentreviews'] = Product.objects.order_by('-created')[:5]
		context['categories'] = Category.objects.all()[:5]
		context['topreviews'] = Product.objects.order_by('views')[:4]
		return context

	# def post(self, request, *args, **kwargs):
	# 	form = ReviewForm(request.POST)
	# 	if form.is_valid():
	# 		thisobj = super(ProductDetail, self).get_object()
	# 		review = Review.objects.create(comment = form.cleaned_data.get('comment'),
	# 			rating = form.cleaned_data.get('score'), 
	# 			post = thisobj,
	# 			author = request.user)
	# 		context = super(ProductDetail, self).get_context_data(**kwargs)
	# 		return self.render_to_response(context = context)
	# 	else:
	# 		context = super(ProductDetail, self).get_context_data(**kwargs)
	# 		context['form'] = form
	# 		return self.render_to_response(context = context)


class MyReviews(ListView):
	template_name = 'myreviewlist.html'
	context_object_name = 'myreviews_list'

	def get_queryset(self):
		return Review.objects.filter(author = self.request.user)

class CreateReview(LoginRequiredMixin, View):

	def get_object(self, **kwargs):
		slug = self.kwargs.get("slug")
		return Product.objects.get(slug = slug)

	def get(self, request, *args, **kwargs):
		product = self.get_object()
		reviewform = ReviewForm()
		template = 'review.html'
		context = {'product' : product,
					'form' : reviewform}
		return render(request, template, context)

	def post(self, request, *args, **kwargs):
		review = ReviewForm(request.POST)
		if review.is_valid():
			comment = review.cleaned_data.get('comment')
			print(comment, 'check')
			score = review.cleaned_data.get('score')
			print (score, 'check')
			author = request.user
			print (author, 'check')
			post = self.get_object()
			print(post, 'check')
			newreview = Review.objects.create(post = post,
											score = score,
											author = author,
											comment = comment,
											)
			print(newreview, 'created')
			return HttpResponseRedirect(reverse('review_detail', kwargs = {'pk' : newreview.pk, }))
		else:
			product = self.get_object()
			template = 'review.html'
			context = {'product' : product,
						'form' : review}
			return render(request, template, context)

			


class ReviewDetail(DetailView):
	model = Review
	template_name = 'thisreview.html'
	context_object_name = 'thisreview'

	def get_context_data(self, **kwargs):
		context = super(ReviewDetail, self).get_context_data(**kwargs)
		context['recentreviews'] = Product.objects.order_by('-created')[:5]
		context['categories'] = Category.objects.all()[:5]
		context['topreviews'] = Product.objects.order_by('views')[:4]
		return context

class ReviewUpdate(LoginRequiredMixin, UpdateView):
	model = Review
	form_class = ReviewForm
	template_name = ''

class ReviewDelete(LoginRequiredMixin, DeleteView):
	model = Review
	success_url = reverse_lazy('my_reviews')

class CategoryList(ListView):
	model = Category

class TagList(ListView):
	model = Tag


class ReviewProfileView(LoginRequiredMixin, UpdateView):
	form_class = ReviewProfileForm
	template_name = "profile.html"
	context_object_name = "form"

	def get_object(self, queryset=None):
		obj, created = ReviewProfile.objects.get_or_create(user = self.request.user)
		return obj

class CategoryProducts(View):


	def get(self, request, *args, **kwargs):
		context_object_name = 'all_products'
		template = "search.html"
		slug  = self.kwargs.get('slug')
		print('slug is ', slug)
		cat = Category.objects.get(slug = slug)
		products = Product.objects.filter(category = cat)
		paginated = Paginator(products, 6)
		page = request.GET.get('page')
		try:
			postlist = paginated.page(page)
		except PageNotAnInteger:
			postlist = paginated.page(1)
		except EmptyPage:
			postlist = paginated.page(paginated.num_pages)
		page_title = 'Category: ' + cat.name
		revws = Product.objects.order_by('-created')[:5]
		categories = Category.objects.all()[:5]
		topreviews = Product.objects.order_by('views')[:4]
		context = {'results':postlist,
			'recentreviews': revws,
			'categories': categories,
			'topreviews': topreviews,
			'page_title': page_title}
		return render(request, template, context)