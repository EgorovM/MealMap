# -*- coding: utf-8 -*-

from django.shortcuts 			import render, HttpResponseRedirect, redirect, HttpResponse
from .models					import Profile, Company
from django.db 					import IntegrityError
from django.core.paginator 		import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth 		import authenticate
from django.contrib.auth 		import logout
from django.contrib 			import auth
from PIL      					import Image
from pytz 						import timezone
from datetime 					import datetime, timedelta
from django.http 				import JsonResponse
from io import StringIO
import pandas as pd
import mimetypes
import threading
import operator
import sqlite3
import json
import pytz
import os
import qrcode

value = {"school_enter":"present","school_exit":"leave"}

secret_word = "axaxloleslivslomaesh"

ykt_utc = timezone('Asia/Yakutsk')

def login(request):
    context = {}
    
    if request.method == "POST":

        if "ok_button" in request.POST:
            login    = request.POST["login"]
            password = request.POST["password"]
    
            if login != "" and password != "":
                user = authenticate(username = login, password = password)

                if user is not None and user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    context["error_message"] = "Неправильно введены данные"
            else:
                context["error_message"] = "Заполните все поля, пожалуйста"
        else:
            return HttpResponseRedirect('/register')

    response = render(request, 'main/login.html',context)

    return response

def index(request):
    context = {}

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    if request.user.email == "company@m.ru":
        profile = Company.objects.get(user = request.user)
    else:
        profile = Profile.objects.get(user = request.user)

    context["profile"] = profile

    request = render(request, 'main/index.html', context)

    return request

def profile(request, views_profile_id):
    context = {}

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    if request.user.email == "company@m.ru":
        profile = Company.objects.get(user = request.user)
    else:
        profile = Profile.objects.get(user = request.user)

    context['profile'] = profile
    request = render(request, 'main/index.html', context)

    return request

def register(request):
    context = {}

    if request.method == "POST":
        if "ok_button" in request.POST:
            username     = request.POST["login"]
            password     = request.POST["password"]
            
            if username !='' and password !='':
                try:
                    user = User.objects.create_user(username = username, password = password)
                    user.save()

                except IntegrityError:
                    context["break"] = True
                    response = render(request, 'main/register.html', context)
                    return response

                if request.POST["status"] == "company":
                    user.email = "company@m.ru"
                    profile = Company(user = user)
                else:
                    user.email = "profile@m.ru"
                    profile = Profile(user = user)

                profile.save()      

                user = authenticate(username = username, password = password)

                if user is not None and user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect("/settings")
            else:
                context['error_message'] = 'Заполните все поля, пожалуйста'

    request = render(request, 'main/register.html', context)

    return request

def settings(request):
    context = {}

    if request.user.email == "company@m.ru":
        profile = Company.objects.get(user = request.user)
    else:
        profile = Profile.objects.get(user = request.user)

    context["profile"] = profile

    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")


    if request.method == "POST":
        if "ok_button" in request.POST:            
            new_password   = request.POST["password"]
            new_city       = request.POST["city"]
            new_first_name = request.POST["first_name"]
            new_last_name  = request.POST["last_name"]

            profile.user.first_name = new_first_name
            profile.user.last_name  = new_last_name
            profile.city            = new_city

            profile.save()
            profile.user.save()

    response = render(request, 'main/settings.html',context)

    return response


def picture(request):
    context = {}

    if not request.user.is_authenticated():
        return redirect('/login')

    if request.user.email == "company@m.ru":
        profile = Company.objects.get(user = request.user)
    else:
        profile = Profile.objects.get(user = request.user)

    if request.method == "POST":
        if "ok_button" in request.POST:

            new_image = ""

            if "image" in request.FILES:
                new_image = request.FILES["image"]
                profile.avatar = new_image
                profile.save()

                return HttpResponseRedirect(".")
            else:
                error_message = "Нет"
                context["error_message"] = error_message


    context['profile'] = profile
    response = render(request, 'main/picture.html',context)

    return response

def logout_view(request):

    logout(request)

    return HttpResponseRedirect('/login')