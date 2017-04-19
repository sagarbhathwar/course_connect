import json
import os
import time
from datetime import datetime
from subprocess import Popen, PIPE
from random import randint

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.urls import reverse
from django.utils import timezone

from .models import Course, Announcement, Question
from .forms import UploadFileForm


class IndexView(generic.ListView):
    template_name = 'course_connect/index.html'
    context_object_name = 'announcements'

    def get_queryset(self):
        return Announcement.get_latest_announcements()


class CoursesView(generic.ListView):
    template_name = 'course_connect/courses.html'

    def get_queryset(self):
        return Course.objects.all()

    def get_context_data(self, **kwargs):
        questions_list = Question.objects.all()
        context = super(CoursesView, self).get_context_data(**kwargs)
        context['question'] = questions_list[randint(
            0, len(questions_list) - 1)]

        return context


def lint(request):
    code = request.POST['code']
    lang = request.POST['lang']

    if lang == "C":
        pass

    elif lang == "java":
        pass

    elif lang == "python":
        f = open("simple.py", "w+")
        f.write(code)
        f.close()
        cmd1 = "pylint --reports=n --disable=deprecated-module --const-rgx='[a-z_][a-z0-9_]{2,30}$'  simple.py > results.txt "
        os.system(cmd1)
        f = open("results.txt", "r")
        data = f.read()
        f.close()
        os.remove("results.txt")
        return HttpResponse(data)


def get_announcements(request):
    timestamp = request.GET.get('timestamp')
    if not timestamp:
        announcements = Announcement.get_latest_announcements()
        context = {'msgs': [anc.title for anc in announcements],
                   'msgid': [anc.id for anc in announcements],
                   'timestamp': timezone.now().isoformat()}
        return HttpResponse(json.dumps(context))

    else:
        timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f+00:00")
        unseen_announcements = Announcement.objects.filter(
            publish_time__gt=timestamp)

        while not unseen_announcements:
            time.sleep(1)
            unseen_announcements = Announcement.objects.filter(
                publish_time__gt=timestamp)

        context = {'msgs': [anc.title for anc in unseen_announcements],
                   'msgid': [anc.id for anc in unseen_announcements],
                   'timestamp': timezone.now().isoformat()}
        return HttpResponse(json.dumps(context))


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


def question(request):
    author = request.POST['author']
    text = request.POST['text']
    title = request.POST['title']
    semester = request.POST['semester']
    form = UploadFileForm(request.POST, request.FILES)
    tests = str(request.FILES['test'].read(), 'utf-8').split("\n\n")
    test_solutions = str(
        request.FILES['testSolution'].read(), 'utf-8').split("\n\n")
    q = Question(question_title=title,
                 question_statement=text,
                 author=author,
                 semester=semester,
                 testcases=tests,
                 solutions=test_solutions)
    q.save()
    return HttpResponseRedirect(reverse('course_connect:question_upload'))


def stream_http(num_testcases, filename, tinput, toutput):
    yield "cases:"+str(num_testcases)
    time.sleep(2)

    for i in range(num_testcases):
        proc = Popen(["python", filename], stdout=PIPE, stdin=PIPE)
        output = proc.communicate(input=str.encode(tinput[i]))[0].decode('utf-8')
        yield str(i+1) + ":" + str(int(output.strip() == toutput[i].strip()))
        time.sleep(2)

def submit(request, question_id):
    code = request.POST['code']
    lang = request.POST['lang']
    question = Question.objects.get(pk=question_id)
    test_cases = question.testcases[0].split("\r\n\r\n")
    solutions = question.solutions[0].split("\r\n\r\n")
    test_cases_int = []
    solutions_int = []
    for test in test_cases:
        test_cases_int.append(test.split("\r\n"))

    for sol in solutions:
        solutions_int.append(sol.split("\r\n"))

    if lang == "C":
        pass

    elif lang == "python":
        f = open("code.py", "w")
        f.write(code)
        f.close()

        return StreamingHttpResponse(stream_http(len(test_cases_int), "code.py",
                                                     test_cases, solutions))


def question_upload(request):
    return render(request, 'course_connect/question_upload.html')
