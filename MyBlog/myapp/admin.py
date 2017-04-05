from django.contrib import admin

# Register your models here.
from .models import Post



# from .forms import SignUpForm
# from .models import SignUp


# from django.contrib.auth.admin import UserAdmin
# from .models import UserProfile


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title","updated","timestamp"]
    list_display_links = ["updated"]
    list_filter = ["updated","timestamp"]
    list_editable = ["title"]

    search_fields = ["title", "content"]
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)



# class SignUpAdmin(admin.ModelAdmin):
#     list_display = ["__unicode__", "timestamp", "updated"]
#     form = SignUpForm
#     # class Meta:
#     # 	model = SignUp
#
# admin.site.register(SignUp, SignUpAdmin)

