from math import e
from urllib.parse import quote_plus

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.db.models import Q


from .models import Post
from .forms import PostForm


#from .forms import SignUpForm
#from .models import SignUp

from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.views import generic
#from .forms import UserForm

from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext


from django.template import loader, Context
from django.http import HttpResponse
from .models import Post




# from django.contrib.auth import (
#     authenticate,
#     get_user_model,
#     login,
#     logout,
#     )
# from .forms import UserLoginForm
#

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_create.html", context)

def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
    }
    return render(request, "post_detail.html", context)

    #return HttpResponse("<h1>Detail</h1>")


def post_about(request):

    return render(request,"post_about.html", {})

def post_contact(request):
    return render(request, "post_contact.html", {})

@login_required
def home(request):
    #return render(request, "home.html", {'user': request.user})
    return render_to_response("home.html", {'user': request.user})

# @login_required
# def home(request):
#     return render_to_response(
#         'home.html',
#         {'user': request.user}
#     )



# def registration(request):
#
#     return render(request, "registration.html",{})

def logout(request):
    return render(request, "logout.html", {})



# def logout_page(request):
#     logout(request)
#     return HttpResponseRedirect('/login')


@login_required(login_url='/login/')
def success(request):
    return render(request,"success.html",{})

def login(request):
    form = LoginForm(request.POST)
    context = {
        "form": form,
    }
    return render(request, "login.html", context)



# def login(request):
#     form = RegistrationForm(request.POST)
#     context = {
#         "form": form
#     }
#
#     return render_to_response(
#         'login.html',
#         context,
#     )





#     title = 'Sign Up Now'
#     form = SignUpForm(request.POST or None)
#     context = {
#         "title": title,
#         "form": form
#     }
#     if form.is_valid():
#         # form.save()
#         # print request.POST['email'] #not recommended
#         instance = form.save(commit=False)
#
#         full_name = form.cleaned_data.get("full_name")
#         if not full_name:
#             full_name = "New full name"
#         instance.full_name = full_name
#         # if not instance.full_name:
#         # 	instance.full_name = "Justin"
#         instance.save()
#         context = {
#             "title": "Thank you"
#         }
#
#     if request.user.is_authenticated() and request.user.is_staff:
#         # print(SignUp.objects.all())
#         # i = 1
#         # for instance in SignUp.objects.all():
#         # 	print(i)
#         # 	print(instance.full_name)
#         # 	i += 1
#
#         queryset = SignUp.objects.all().order_by('-timestamp')  # .filter(full_name__iexact="Justin")
#         # print(SignUp.objects.all().order_by('-timestamp').filter(full_name__iexact="Justin").count())
#         context = {
#             "queryset": queryset
#         }
#     return render(request,"login.html",context)


@login_required(login_url='/login/')
def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()  # .order_by("-timestamp")


    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 20)  # Show 8 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "post_list.html", context)

def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form":form,
    }
    return render(request, "post_update.html", context)


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("myapp:list")

# def login_view(request):
#     forms = UserLoginForm(request.POST or None)
#     if forms.is_valid():
#         username = forms.cleaned_data.get("username")
#         password = forms.cleaned_data.get("password")
#     return render(request,"form.html", {})
#
# def logout_view(request):
#     return render(request,"form.html", {})
#
# def register_view(request):
#     return render(request,"form.html", {})


# class UserFormView(View):
#     form_class = UserForm
#     template_name = 'templates/registration_form.html'
#
#
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#
#         if form.is_valid():
#             user = form.save(commit=False)
#
#             username = form.cleaned_data('username')
#             password = form.cleaned_data('password')
#             user.set_password(password)
#             user.save()
#
#             user = authenticate(username=username, password=password)
#
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('myapp:login')
#
#         return render(request, self.template_name, {'form': form})

@csrf_protect
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'registration.html',
        variables,
    )


def register_success(request):
    return render_to_response(
        'registration/success.html',
    )

#
def logout_page(request):
    logout(request)
    return redirect('/')


# @login_required
# def home(request):
#     return render_to_response(
#         'home.html',
#         {'user': request.user}
#     )


#
# logger = login_required('myapp.views')
#
# def archive(request):
#     try:
#         year = request.GET.get('year', None)
#         mouth = request.GET.get('mouth', None)
#         article_list = Post.objects.filter(
#             date_publish__icontains=year + '-' + mouth)
#         article_list = getPage(request, article_list)
#     except (Exception, e):
#         logger.error(e)
#     return render(request, 'archive.html', locals())
#
#
# def getPage(request, article_list):
#     paginator = Paginator(article_list, 5)
#     try:
#         page = int(request.GET.get('page', 1))
#         article_list = paginator.page(page)
#     except (EmptyPage, InvalidPage, PageNotAnInteger):
#         article_list = paginator.page(1)
#     return article_list
#

def archive(request):
    posts = Post.objects.all()
    t = loader.get_template("archive.html")
    c = Context({ 'posts': posts })
    return HttpResponse(t.render(c))

