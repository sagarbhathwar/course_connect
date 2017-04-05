from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Course


class IndexView(generic.ListView):
    template_name = 'course_connect/index.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.order_by('-start_date')


class CoursesView(generic.ListView):
    template_name = 'course_connect/courses.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.all()

def check_code(request):
    code = request.POST['code']
    lang = request.POST['lang']

    if lang == "C":
        pass

    elif lang == "java":
        pass

    elif lang == "python":
        pass

    elif lang == "C++":
        pass

def lint(request):
    code = request.POST['code']
    lang = request.POST['lang']

    if lang == "C":
        pass

    elif lang == "java":
        pass

    elif lang == "python":
        
        """
        >>>TODO Use pylint on the code
                Echo the output of pylint
        """
        return HttpResponse("Good job!")

    elif lang == "C++":
        pass
