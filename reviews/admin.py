from django.contrib import admin
from .models import Product, Review, Tag, Category, ReviewProfile, FavoriteReview
from .forms import ProductForm, ReviewForm



# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	form = ProductForm
	list_display = ('business_name', 'views', 'created', 'updated', )
	prepopulated_fields = {'slug': ('business_name',)}
	radio_fields = {'category': admin.VERTICAL}
	readonly_fields = ('views', 'created', 'updated',)

	class Meta:
		model = Product

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ('post', 'comment', 'score', 'author', 'created', 'updated')
	exclude = ('author', 'created', 'updated',)

	def save_model(self, request, obj, form, change):
		if not obj.author:
			obj.author = request.user
			obj.save()

admin.site.register(FavoriteReview)
admin.site.register(ReviewProfile)
admin.site.register(Tag)
admin.site.register(Category)

