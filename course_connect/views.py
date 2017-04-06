import json
import os
import time
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone

from .models import Course, Announcement


class IndexView(generic.ListView):
    template_name = 'course_connect/index.html'
    context_object_name = 'announcements'

    def get_queryset(self):
        return Announcement.get_latest_announcements()

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
        f= open("simple.py","w+")
        f.write(code)
        f.close()
        cmd1 = "pylint --reports=n --disable=deprecated-module --const-rgx='[a-z_][a-z0-9_]{2,30}$'  simple.py > results.txt "
        os.system(cmd1)
        f=open("results.txt","r")
        data = f.read()
        f.close()
        return HttpResponse(data)

    elif lang == "C++":
        pass

def get_announcements(request):
    timestamp = request.GET.get('timestamp')
    if not timestamp:
        announcements = Announcement.get_latest_announcements()
        context = {'msgs': [anc.title for anc in announcements],
                   'msgid': [anc.id for anc in announcements],
                   'timestamp' : timezone.now().isoformat()}
        return HttpResponse(json.dumps(context))

    else:
        timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f+00:00")
        unseen_announcements = Announcement.objects.filter(publish_time__gt=timestamp)

        while not unseen_announcements:
            time.sleep(1)
            unseen_announcements = Announcement.objects.filter(publish_time__gt=timestamp)
        

        context = {'msgs': [anc.title for anc in unseen_announcements],
                   'msgid': [anc.id for anc in unseen_announcements],
                   'timestamp' : timezone.now().isoformat()}
        return HttpResponse(json.dumps(context))


def get_submissions(request):
    pass

def announce(request):
    author = request.GET['author']
    text = request.GET['text']
    title = request.GET['title']
    announcement = Announcement(author=author,
                                title=title,
                                announcement_text=text)
    announcement.save()

    return HttpResponseRedirect(reverse('course_connect:announce_something'))

def announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    context = {'announcement': announcement}
    return render(request, 'course_connect/announcement.html', context=context)

def announce_something(request):
    return render(request, 'course_connect/announce.html')