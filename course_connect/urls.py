from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'course_connect'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^about/$', TemplateView.as_view(template_name='course_connect/about.html'),
        name='about'),
    url(r'^contact/$', TemplateView.as_view(template_name='course_connect/contact.html'),
        name='contact'),
    url(r'^courses/$', views.CoursesView.as_view(), name='courses'),
    url(r'^lint/$', views.lint, name='lint'),
    url(r'^check/$', views.check_code, name='check'),
    url(r'^announcements/$', views.get_announcements, name='get_announcements'),
    url(r'^submissions/$', views.get_submissions, name='get_submissions'),
    url(r'^announce/$', views.announce ,name="announce"),
    url(r'^announce_something/$', views.announce_something, name="announce_something"),
    url(r'^announcement/(?P<announcement_id>[0-9]+)/$', views.announcement, name="announcement")
]
