from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView

from .forms import ComposeForm
from .models import Thread, ChatMessage

from Auth.models import SocialPerson
from friend.models import FriendList


class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chatsystem/white_chat.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        friend = FriendList.objects.get(user=self.request.user)
        results = []
        for i in friend.friends.all():
            results.append(SocialPerson.objects.get(slug=i.username))
        context['friends'] = results
        
        return context


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chatsystem/chat.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("slug")
        
        if self.kwargs.get("slug") == self.request.user.username:
            raise Http404

        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['person'] = SocialPerson.objects.get(slug = self.kwargs['slug'])
        context['me'] = SocialPerson.objects.get(slug=self.request.user.username)
        context['allMessages'] = ChatMessage.objects.filter(thread=self.get_object())

        friend = FriendList.objects.get(user=self.request.user)
        results = []
        for i in friend.friends.all():
            results.append(SocialPerson.objects.get(slug=i.username))
        context['friends'] = results

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)