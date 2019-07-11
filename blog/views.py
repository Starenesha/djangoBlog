from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Post, Tag
from django.views.generic import View
from .utils import *
from .forms import TagForm, PostForm
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q


def post_list(request):
    search_query = request.GET.get('search','')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query)) #филтр поиска по названию или по телу поста
    else:
        posts = Post.objects.all()

#    page_obj = Post.objects.all()
    paginator = Paginator(posts,1)

    page_number = request.GET.get('page',1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context ={
        'page_obj': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }
    return render(request,'blog/index.html', context=context)

def tags_list(request):
    tags = Tag.objects.all()
    return render(request,'blog/tags_list.html', context={'tags':tags})


class PostCreate(ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post_create_form.html'


class PostUpdate(ObjectUpdateMixin,View):
    model = Post
    template = 'blog/post_update.html'
    form_model = PostForm

class PostDelete(ObjectDeleteMixin,View):
    model = Post
    redirect_url = 'post_list_url'
    template = 'blog/post_delete_form.html'

class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'

class PostDetail(ObjectDetailMixin, View):

    model = Post
    template = 'blog/post_detail.html'

class TagCreate(ObjectCreateMixin, View):

    form_model = TagForm
    template = 'blog/tag_create.html'


class TagUpdate(ObjectUpdateMixin,View):
    model = Tag
    template = 'blog/tag_update.html'
    form_model = TagForm


class TagDelete(ObjectDeleteMixin,View):
    model = Tag
    redirect_url = 'tags_list_url'
    template = 'blog/tag_delete_form.html'





#from django.views import View
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.core.mail import EmailMessage


def home(request):
    return HttpResponse("Home Page!")

def hello(request):
    return HttpResponse("Home Page")



class Signup(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'Signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create an inactive user with no password:
            user = form.save(commit=False)
            user.is_active = False
            user.set_unusable_password()
            user.save()

            # Send an email to the user with the token:
            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = "{0}/?uid={1}&token{2}".format(current_site, uid, token)
            message = "Hello {0},\n {1}".format(user.username, activation_link)
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

    #    else:
    #        form = SignupForm()
    #    args = {'form': form}
    #    return render(request, 'Signup.html', args)

from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token

User = get_user_model()

class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            login(request, user)

            form = PasswordChangeForm(request.user)
            return render(request, 'acc_active_email.html', {'form': form})

        else:
            return HttpResponse('Activation link is invalid!')

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Important, to update the session with the new password
            return HttpResponse('Password changed successfully')