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
    url(r'check/$', views.check_code, name='check')

]
