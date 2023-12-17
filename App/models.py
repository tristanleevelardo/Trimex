# faculty/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Faculty(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_faculty = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_faculty = models.BooleanField(default=False)
    section = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class thirdYear (models.Model):
    student_firstName=models.CharField(max_length=255)
    student_lastName=models.CharField(max_length=255)
    student_fullName=models.CharField(max_length=255)
    
    subject =  models.CharField(max_length=255)
    course =  models.CharField(max_length=255)

    instructor_firstName =  models.CharField(max_length=255)
    instructor_lastName =  models.CharField(max_length=255)
    instructor_fullName =  models.CharField(max_length=255)
    
    totalSW = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    totalQuiz = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    writtenOutput = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    performanceTask = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    prelim = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    midterm = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    finals = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    grade = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"Student:{self.student_firstName},{self.student_lastName}__Course: {self.course}__Subject: {self.subject}__Instructor:{self.instructor_lastName}")
    
    def save(self, *args, **kwargs):
        # Update the modified_at field when the instance is saved
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)

class unit (models.Model):
    subject =  models.CharField(max_length=255)
    course =  models.CharField(max_length=255)
    instructor_fullName =  models.CharField(max_length=255)
    instructor_firstName =  models.CharField(max_length=255)
    instructor_lastName =  models.CharField(max_length=255)

    def __str__(self):
        return (f"{self.instructor_fullName}")
    
class Mail (models.Model):
    mail =  models.CharField(max_length=255)
    student_fullName =  models.CharField(max_length=255)
    instructor_fullName =  models.CharField(max_length=255)
    to_prof = models.BooleanField(default=False)
    to_student= models.BooleanField(default=False)
    datetime_sent = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return (f"{self.datetime_sent}")
    
    