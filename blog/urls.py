from django.conf.urls import url
from . import views




urlpatterns = [
	url(r'^(?P<slug>.*)/comment/$', views.blogComment, name="blogpost_comment"),
	url(r'^(?P<slug>.*)/$', views.BlogPostDetailView.as_view(), name="blogpost_detail"),
	url(r'^$', views.blogIndex, name='blogpost_index'),

]