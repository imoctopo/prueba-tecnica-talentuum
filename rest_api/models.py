from django.db import models


class Actor(models.Model):
    login = models.CharField(max_length=50)
    avatar_url = models.URLField()

    def __str__(self):
        return self.login


class Repo(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name


class Event(models.Model):
    type = models.CharField(max_length=50)
    actor = models.ForeignKey(Actor, on_delete=models.PROTECT, related_name='events')
    repo = models.ForeignKey(Repo, on_delete=models.PROTECT, related_name='events')
    created_at = models.DateTimeField()

    def __str__(self):
        return self.type
