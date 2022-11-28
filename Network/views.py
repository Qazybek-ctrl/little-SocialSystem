from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.urls import reverse

from django.contrib.auth.models import User
from Auth.models import SocialPerson
from .forms import EditProfileForm, EditImage
from friend.models import FriendList, FriendRequest
from .utils import check_condition

# Create your views here.

def friendsPage(request, *args, **kwargs):
    context = {}
    context['isOwner'] = True
    try:
        context['user'] = SocialPerson.objects.get(slug=request.user.username)
    except:
        return redirect('home')
         
    if 'pageOwner' in request.GET:
        pageOwner = SocialPerson.objects.get(slug=request.GET['pageOwner'])
        if request.user.username != pageOwner:
            context['isOwner'] = False
    else:
        pageOwner = SocialPerson.objects.get(slug=request.user.username)

    context['friend_request_list'] = []

    if context['isOwner'] == True:
        friend_request_list = FriendRequest.objects.filter(receiver=request.user, is_active=True)
        friendRequestResult = []
        for i in friend_request_list:
            friendRequestResult.append(SocialPerson.objects.get(slug=i.sender.username))
        context['friend_request_list'] = friendRequestResult
        print(type(friendRequestResult))

    friend = FriendList.objects.get(user=pageOwner.user)
    friends = friend.friends.all()
    results = []
    for i in friends:
        results.append(SocialPerson.objects.get(slug=i.username))
    context['friends'] = results
    context['pageOwner'] = pageOwner
    return render(request, 'Network/friends.html', context)

def homePage(request):
    context = {

    }
    if request.user.is_authenticated and request.user.is_superuser != True:
        context['user'] = SocialPerson.objects.get(slug=request.user.username)
    return render(request, 'Network/index.html', context)


def profilePage(request, *args, **kwargs):
    context = {}

    context['isFriend'] = False

    if request.user.is_authenticated == False:
        return redirect('home')

    # profile_user = kwargs.get('profile_slug')
    try:
        page_owner = SocialPerson.objects.get(slug = kwargs.get('profile_slug'))
    except:
        return HttpResponse("Oops, Something went wrong :(")

    try:
        friend_list = FriendList.objects.get(user=page_owner.user)
    except FriendList.DoesNotExist:
        friend_list = FriendList(user = page_owner.user)
        friend_list.save()
    
    friend = friend_list.friends.all()

    context['isOwner'] = True
    context['isFriend'] = False
    context['condition'] = 1
    context['friend_request_list'] = False

    if request.user.is_authenticated == True and request.user != page_owner.user:
        context['isOwner'] = False
        if friend.filter(pk=request.user.id).exists():
            context['isFriend'] = True
        else:
            context['isFriend'] = False
            if check_condition(sender=page_owner.user, receiver=request.user) != False:
                context['condition'] = 1
            elif check_condition(sender=request.user, receiver=page_owner.user):
                context['condition'] = 2
            else:
                context['condition'] = 0
    else:
        friend_request_list = FriendRequest.objects.filter(receiver=request.user, is_active=True)
        context['friend_request_list'] = friend_request_list
        print(friend_request_list)

    context['person'] = page_owner
    context['friend'] = friend

    return render(request, 'Network/profile.html', context)

def editPage(request, profile_slug):
    if request.user.is_authenticated == False or profile_slug != request.user.username:
        return redirect('home')

    costumer = request.user.socialperson
    form = EditImage(instance=costumer)
    form1 = EditProfileForm(instance=request.user)

    if request.method == 'POST' and 'Update Information' in request.POST:
        form = EditImage(request.POST, request.FILES,instance=costumer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes successfully saved', extra_tags='forms')

    if request.method == 'POST' and 'additional' in request.POST:
        form1 = EditProfileForm(request.POST, instance=request.user)
        if form1.is_valid():
            form1.save()
            messages.success(request, 'Changes successfully saved <=3', extra_tags='form-additional')

    context = {
        'person': request.user.socialperson,
        'form':form,
        'form1':form1,
        'profile':request.user.username
    }
    return render(request, 'Network/edit.html', context)

def friend_action(request, *args, **kwargs):
    action = kwargs.get('operation')
    person = SocialPerson.objects.get(slug=kwargs.get('slug'))
    if action == 'send_friend_request':
        if FriendRequest.objects.filter(sender=request.user, receiver=person.user).count() == 0:
            friend_request = FriendRequest(sender=request.user, receiver=person.user)
            friend_request.save()
            return redirect('profile', person.slug)
        friend_request = FriendRequest.objects.get(sender=request.user, receiver=person.user, is_active=False)
        friend_request.is_active = True
        friend_request.save()
        return redirect('profile', person.slug)
    elif action == 'accept':
        friend_request = FriendRequest.objects.get(sender=person.user, receiver=request.user)
        friend_request.accept()
        friend_request.save()
        return redirect('profile', person.slug)
    elif action == 'decline':
        friend_request = FriendRequest.objects.get(sender=person.user, receiver=request.user)
        friend_request.decline()
        friend_request.save()
        return redirect('profile', person.slug)
    elif action == 'cancel':
        friend_request = FriendRequest.objects.get(sender=request.user, receiver=person.user, is_active=True)
        friend_request.cancel()
        return redirect('profile', person.slug)
    elif action == 'delete_friend':
        friend_request = FriendList.objects.get(user=request.user)
        friend_request.unfriend(account=person.user)
        friend_request.save()
        return redirect('profile', person.slug)
    else:
        return redirect('profile', person.slug)
