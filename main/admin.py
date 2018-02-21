# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Page, Node, Comment

class PageAdmin(admin.ModelAdmin):
    pass
class NodeAdmin(admin.ModelAdmin):
    list_display = ('to_str', 'order')

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Page,PageAdmin)
admin.site.register(Node,NodeAdmin)
admin.site.register(Comment,CommentAdmin)
