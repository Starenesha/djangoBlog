from django.http import HttpResponse
from django.shortcuts import redirect, render


# def redirect_blog(request):
#     return redirect('post_list_url', permanent=True)


def home(request):
    return render(request, "home.html")