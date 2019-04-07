# -*- coding: utf-8 -*-

from django.shortcuts 			import render, HttpResponseRedirect, redirect, HttpResponse
from .models					import Profile, Company, Company_Post
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

def makeqrcode(id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(id)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("media/qrcodes/" + str(id) + ".png", "JPEG")

def plus(request):
    if request.GET.get("index") and request.GET.get("call") and request.GET.get("col"):
       profile = Profile.objects.get( id = request.GET["index"])
       profile.cholesterol += int(request.GET["call"])
       profile.calories += int(request.GET["col"])

       profile.save()

    return HttpResponseRedirect("/")

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
    context["company_posts"] = Company_Post.objects.all()

    request = render(request, 'main/index.html', context)

    return request

def profile(request, views_profile_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")

    context = {}

    user = User.objects.get(id = views_profile_id)


    if user.email == "company@m.ru":
        view_profile = Company.objects.get(user = user)
    else:
        view_profile = Profile.objects.get(user = user)

    context["view_profile"] = view_profile

    if request.user.email == "company@m.ru":
         context["profile"] = Company.objects.get(user = request.user)
    else:
        context["profile"] = Profile.objects.get(user = request.user)


    if request.method == "POST":
        if "com_btn" in request.POST:
            title = request.POST["title"]
            message = request.POST["message"]

            post = Company_Post.objects.create(company = Company.objects.get(user = request.user))
            post.title = title
            post.message = message

            post.save()

    request = render(request, 'main/profile.html', context)

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
                    context["error_message"] = "Такой аккаунт уже существует"
                    response = render(request, 'main/register.html', context)
                    return response

                if 'status' in request.POST and request.POST['status'] == "company":
                    user.email = "company@m.ru"
                    profile = Company(user = user)
                    profile.save()
                    user.save()
                else:
                    user.email = "profile@m.ru"
                    profile = Profile(user = user)
                    profile.save()
                   
                    makeqrcode(profile.id)
                    profile.qrcode = "qrcodes/" + str(profile.id) + ".png"
                    profile.user.save()
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
            if request.POST["password"] != "" and request.POST["password"] != None:
                new_password   = request.POST["password"]
                profile.user.password = new_password

            new_city       = request.POST["city"]
            if request.user.email == "company@m.ru":
                new_name = request.POST["name"]
                new_address = request.POST["address"]
                profile.name = new_name
                profile.address = new_address
            else:
                new_first_name = request.POST["first_name"]
                new_last_name  = request.POST["last_name"]
                new_about      = request.POST["about"]
                new_wishes     = request.POST["wishes"]

                profile.user.first_name = new_first_name
                profile.user.last_name  = new_last_name
                profile.wishes = new_wishes
                profile.about = new_about
            
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