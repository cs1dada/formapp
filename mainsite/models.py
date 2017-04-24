# _*_ encoding: utf-8 _*_
from django.db import models

class Mood(models.Model):
    status = models.CharField(max_length=10, null=False)

    def __unicode__(self):
        return self.status

class Post(models.Model):
    #ForeignKey: mood
    mood = models.ForeignKey('Mood', on_delete=models.CASCADE)
    #guest input infomation
    nickname = models.CharField(max_length=10, default='不願意透漏身份的人')
    message = models.TextField(null=False)
    del_pass = models.CharField(max_length=10)
    pub_time = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return self.message
