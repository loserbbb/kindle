from django.db import models

# Create your models here.


class Book(models.Model):
    bookpath = models.TextField()
    bookname = models.CharField(max_length=50)
    

class Fans(models.Model):
    fansid = models.CharField(max_length=35, unique=True)
    email = models.CharField(max_length=30)
    downloademail = models.CharField(max_length=30)
    lastpush = models.DateField(null=True)
    lastdownload = models.DateField(null=True)
    times = models.IntegerField(default=0)
    downloadtimes = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    deadline = models.DateField(null=True)


class Activationcode(models.Model):
    code = models.CharField(max_length=32, unique=True)
    rank = models.IntegerField()


class Count(models.Model):
    rank = models.IntegerField()
    price = models.FloatField()
    time = models.DateTimeField(null=True, auto_now_add=True)

class Accesskey(models.Model):
    key = models.TextField()
    gettime = models.IntegerField()

class Pushlist(models.Model):
    bookname = models.TextField()
    usermail = models.CharField(max_length=30)
    bookpath = models.TextField()
