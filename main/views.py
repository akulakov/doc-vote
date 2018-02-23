# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from django.views.generic import (DetailView, UpdateView, DeleteView, FormView, View, ListView,
                                  CreateView)
from django.views.generic.detail import SingleObjectMixin

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Page, Vote, Node, Comment
from .forms import CommentForm

vote_links = """
<a href='{minus_url}' class='{minus_class}'>-</a>
<a href='{plus_url}' class='{plus_class}'>+</a>
"""

class PageView(DetailView):
    model = Page
    template_name = 'page.html'

    def get_context_data(self, **kwargs):
        nodes = []
        for node in self.object.nodes.all():
            user_vote = Vote.objects.filter(
                                         user=self.request.user,
                                         node=node,
                                         ).first()
            minus_url = reverse('vote', kwargs=dict(pk=node.pk,
                                                    page_pk=self.object.pk,
                                                    plus=0))
            plus_url = reverse('vote', kwargs=dict(pk=node.pk,
                                                   page_pk=self.object.pk,
                                                   plus=1))

            if not user_vote:
                node.vote_links = vote_links.format(minus_class='', plus_class='', minus_url=minus_url, plus_url=plus_url)
            elif user_vote.plus:
                node.vote_links = vote_links.format(minus_class='', plus_class='selected', minus_url=minus_url, plus_url=plus_url)
            elif not user_vote.plus:
                node.vote_links = vote_links.format(minus_class='selected', plus_class='', minus_url=minus_url, plus_url=plus_url)

            nodes.append(node)
        kwargs['nodes'] = nodes
        return super().get_context_data(**kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class AjaxNodeView(SingleObjectMixin, View):
    model = Node

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return JsonResponse(dict(success=True))

    def get(self, request, *args, **kwargs):
        return JsonResponse(dict(body=self.get_object().body))

    def post(self, request, *args, **kwargs):
        node = self.get_object()
        node.body = self.request.POST.get('body')
        node.save()
        return JsonResponse(dict(body=node.body_rendered, success=True))


# class NodeView(DetailView):
#     model = Node
#     context_object_name = 'node'
#     template_name = 'node.html'

#     def get_context_data(self, **kwargs):
#         kwargs.update(form=CommentForm(), view=self, comments=self.object.comments.all())
#         return super().get_context_data(**kwargs)


class CreateUpdateCommentView(UpdateView):
    model = Comment
    template_name = 'create-update-comment.html'
    fields = ('body',)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if pk:
            return self.model.objects.get(pk=pk)

    def form_valid(self, form):
        node = get_object_or_404(Node, pk=self.kwargs.get('node_pk'))
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.node = node
        comment.save()
        return redirect(node.get_absolute_url())


class CreateUpdateNodeAjaxView(UpdateView):
    model = Node
    fields = ('body',)
    def get_object(self, queryset=None):
        if self.after:
            return None
        pk = self.kwargs.get('node_pk')
        if pk:
            return self.model.objects.get(pk=pk)

    def form_valid(self, form):
        node = form.save(commit=False)
        node.creator = self.request.user
        page = get_object_or_404(Page, pk=self.kwargs.get('pk'))

        pk = self.kwargs.get('node_pk')
        last = self.model.objects.get(pk=pk)

        order = None
        next = Node.objects.filter(order__gt=last.order).first()
        if next:
            if (next.order - last.order) <= 1:
                Node.reorder_after(last)
                order = last.order + 10
            else:
                order = last.order + int((next.order - last.order)/2)

        if not order:
            order = Node.objects.filter(page=page).last().order + 20
        node.order = order
        node.page = page
        node.save()
        return redirect(page.get_absolute_url())


class CreateUpdateNodeView(UpdateView):
    model = Node
    template_name = 'create-update-node.html'
    fields = ('body',)
    after = False

    def get_object(self, queryset=None):
        if self.after:
            return None
        pk = self.kwargs.get('node_pk')
        if pk:
            return self.model.objects.get(pk=pk)

    def form_valid(self, form):
        node = form.save(commit=False)
        node.creator = self.request.user
        page = get_object_or_404(Page, pk=self.kwargs.get('pk'))

        pk = self.kwargs.get('node_pk')
        last = self.model.objects.get(pk=pk)

        order = None
        next = Node.objects.filter(order__gt=last.order).first()
        if next:
            if (next.order - last.order) <= 1:
                Node.reorder_after(last)
                order = last.order + 10
            else:
                order = last.order + int((next.order - last.order)/2)

        if not order:
            order = Node.objects.filter(page=page).last().order + 20
        node.order = order
        node.page = page
        node.save()
        return redirect(page.get_absolute_url())

# class DeleteNodeView(DeleteView):
#     model = Node
#     page_pk = None

#     def get_success_url(self):
#         return reverse('page', kwargs=dict(pk=self.kwargs.get('page_pk')))

@method_decorator(csrf_exempt, name='dispatch')
class VoteView(DetailView):
    model = Node
    template_name = 'none'

    def post(self, request, *args, **kwargs):
        node = self.get_object()
        plus = int(self.kwargs.get('plus'))
        page_pk = self.kwargs.get('page_pk')
        vote = Vote.objects.filter(node=node, user=self.request.user).first() \
                or Vote(node=node, user=self.request.user)
        vote.plus = bool(plus)
        vote.save()
        return JsonResponse(dict(score=vote.node.score))
        # return redirect(reverse('page', kwargs=dict(pk=page_pk)))

class MoveNodeView(DetailView):
    model = Node
    template_name = 'none'

    def get(self, request, *args, **kwargs):
        node = self.get_object()

        dir = self.kwargs.get('dir')
        other = None
        if dir == 'down':
            other = Node.objects.filter(order__gt=node.order).first()
        elif dir == 'up':
            other = Node.objects.filter(order__lt=node.order).last()
        if other:
            node.order, other.order = other.order, node.order
            node.save(); other.save()

        page_pk = self.kwargs.get('page_pk')
        return redirect(reverse('page', kwargs=dict(pk=page_pk)))
