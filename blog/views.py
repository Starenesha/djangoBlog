from .models import *
from django.views.generic import View
from .utils import *
from .forms import TagForm, PostForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def post_list(request):
    search_query = request.GET.get('search','')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

#    page_obj = Post.objects.all()
    paginator = Paginator(posts,4)

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
    return render(request, 'blog/index.html', context=context)


def tags_list(request):

    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags':tags})


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



