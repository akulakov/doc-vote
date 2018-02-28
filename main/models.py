# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, transaction
from django.contrib.auth.models import User
from django.urls import reverse

from markdown2 import markdown

class Page(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('page', kwargs=dict(pk=self.pk))

class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Node(TimeStamp, models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='nodes')
    body = models.TextField(max_length=5000)
    body_rendered = models.TextField(max_length=15000, blank=True, default='')
    order = models.IntegerField(default=1, blank=True)
    score = models.IntegerField(default=0, blank=True)

    def get_absolute_url(self):
        return reverse('node', kwargs=dict(pk=self.pk))

    def save(self, *args, **kwargs):
        self.body_rendered = markdown(self.body)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.body[:25] + '...'

    def to_str(self):
        return str(self)

    def calc_score(self):
        return self.votes.filter(plus=True).count() - \
                self.votes.filter(plus=False).count()

    @staticmethod
    def reorder_after(last):
        nodes = Node.objects.filter(order__gt=last.order)
        order = last.order
        for node in nodes:
            order += 20
            node.order = order
            node.save()

    class Meta:
        ordering = ('order',)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, related_name='votes', on_delete=models.CASCADE)
    plus = models.BooleanField()

    def __str__(self):
        return '+' if self.plus else '-'

    @transaction.atomic
    def save(self, **kwargs):
        mod = 0
        delete = False
        if not self.pk:
            mod = 1 if self.plus else -1
        else:
            orig_sign = Vote.objects.get(pk=self.pk).plus
            if orig_sign is True and self.plus is False:
                mod = -2
            elif orig_sign is False and self.plus is True:
                mod = 2
            elif orig_sign is True and self.plus is True:
                mod = -1
                delete = True
            elif orig_sign is False and self.plus is False:
                mod = 1
                delete = True
        self.node.score += mod
        self.node.save()
        if delete:
            self.delete()
        else:
            super().save(**kwargs)

    class Meta:
        pass
        # unique_together = ('user', 'node')

class Comment(TimeStamp, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=5000)
    body_rendered = models.TextField(max_length=15000, blank=True, default='')
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.body[:25] + '...'

    def save(self, *args, **kwargs):
        self.body_rendered = markdown(self.body)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('created',)

