from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

class Course(models.Model):
    course_code = models.CharField(max_length=12, primary_key=True)
    course_name = models.CharField(max_length=50)
    img_path = models.CharField(max_length=100)
    start_date = models.DateField()


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    announcement_text = models.TextField()
    author = models.CharField(max_length=100)
    publish_time = models.DateTimeField(default=timezone.now)

    @staticmethod
    def get_latest_announcements():
        return Announcement.objects.order_by('-publish_time')[:5]


class Question(models.Model):
    question_title = models.CharField(max_length=100)
    question_statement = models.CharField(max_length=1000)
    author = models.CharField(max_length=100)
    semester = models.IntegerField(default=3)
    testcases = ArrayField(models.TextField())
    solutions = ArrayField(models.TextField())
    publish_time = models.DateTimeField(default=timezone.now)
