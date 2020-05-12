from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', post_list, name='post_list_url'),
    path('post/create/',login_required(PostCreate.as_view()), name='post_create_url'),
    path('post/<str:slug>/update/', login_required(PostUpdate.as_view()), name='post_update_url'),
    path('post/<str:slug>/delete', login_required(PostDelete.as_view()), name='post_delete_url'),
    path('post/<str:slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('tags/', tags_list, name='tags_list_url'),
    path('tag/create/', login_required(TagCreate.as_view()), name='TagCreate_url'),
    path('tag/<str:slug>/update/', login_required(TagUpdate.as_view()), name='tag_update_url'),
    path('tag/<str:slug>/delete/', login_required(TagDelete.as_view()), name='tag_delete_url'),
    path('tag/<str:slug>/', TagDetail.as_view(), name='tag_detail_url'),
]