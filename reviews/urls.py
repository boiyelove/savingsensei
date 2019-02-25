from django.conf.urls import url
from . import views



urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='home'),
	url(r'^accounts/profile/$', views.ReviewProfileView.as_view(), name='my_profile'),
	url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
	url(r'^search/$', views.search, name='search_reviews'),
	url(r'^products/add/$', views.CreateProduct.as_view, name='CreateProduct'),
	url(r'^myreviews/$', views.MyReviews.as_view(), name='my_reviews'),
	url(r'^myfavorites/$', views.MyReviews.as_view(), name='my_fav_list'),
	url(r'^all_products/$', views.ProductList.as_view(), name='all_products'),
	url(r'^category/(?P<slug>.*)/$', views.CategoryProducts.as_view() , name='nav_categories'),
	url(r'^reviews/(?P<pk>[0-9]+)/$', views.ReviewDetail.as_view(), name = 'review_detail'),
	url(r'^reviews/(?P<pk>[0-9]+)/delete/$', views.ReviewDelete.as_view(), name = 'review_delete'),
	url(r'^reviews/(?P<pk>[0-9]+)/edit/$', views.ReviewUpdate.as_view(), name = 'review_edit'),
	url(r'^(?P<slug>.*)/add_review/$', views.CreateReview.as_view(), name = 'review_add'),
	url(r'^(?P<slug>.*)/$', views.ProductDetail.as_view(), name = 'review_product_detail'),
]