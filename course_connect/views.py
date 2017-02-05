from django.shortcuts import render
from django.views import generic

from .models import Course


class IndexView(generic.ListView):
    template_name = 'course_connect/index.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.order_by('-start_date')
