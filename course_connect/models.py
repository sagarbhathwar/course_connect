from django.db import models
from django.utils import timezone


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

