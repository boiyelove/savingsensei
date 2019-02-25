from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from .models import Post, Comment

# Create your views here.

def blogIndex(request):
	post_list = Post.objects.order_by('-created')
	paginator = Paginator(post_list, 5)
	page = request.GET.get('page')
	try:
		postlist = paginator.page(page)
	except PageNotAnInteger:
		postlist = paginator.page(1)
	except EmptyPage:
		postlist = paginator.page(paginator.num_pages)
	context = {'all_posts' : postlist}
	template = 'blog.html'
	return render(request, template, context)


@login_required
@require_POST
def blogComment(request, slug):
	if request.POST:
		comment = CommentForm(request.POST)
		if comment.is_valid():
			postitem = get_object_or_404(Post, slug = slug)
			Comment.objects.create(author = request.user, body=comment.get_Clean_data('body'), post=postitem)
			message.success('Your comment was added')
			return reverse('blogpost_detail', kwargs={'slug':slug})
	else:
		raise Http404



class BlogPostDetailView(DetailView):
	model = Post
	context_object_name = 'blog_item'
	tenplate_name = 'blog_single.html'

	def get_object(self):
		post = super(PostDetailView, self).get_object()
		post.views += 1
		post.save()
		return post 



