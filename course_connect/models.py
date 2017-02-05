from django.db import models
from django.utils import timezone


class Course(models.Model):
    course_code = models.CharField(max_length=12, primary_key=True)
    course_name = models.CharField(max_length=50)
    img_path = models.CharField(max_length=100)
    start_date = models.DateField()
