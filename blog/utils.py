from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.urls import reverse


class ObjectDetailMixin:

    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__exact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj, 'admin_obj':obj, 'detail':True})


class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, context={'form':form})

    def post(self,request):
        bound_form = self.form_model(request.POST or None,request.FILES or None)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        else:
            return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin:
    form_model=None
    template=None
    model=None

    def get(self,request,slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.form_model(instance=obj)
        return render(request, self.template, context={'form':bound_form, 'tag':obj})

    def post(self,request,slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.form_model(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        else:
            return render(request, self.template, context={'form':bound_form, self.__name__.lower(): obj})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower():obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))
