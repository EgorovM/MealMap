# -*- coding: utf-8 -*-

from __future__                     import unicode_literals
from django.utils.encoding          import python_2_unicode_compatible
from django.db                      import models
from django.contrib.auth.models     import User
from datetime 					    import datetime
from django 						import forms
from django.utils import timezone

STATUS = (
	('company', 'Предприниматель'),
	('profile', 'Потребитель'),
)

class Review(models.Model):
	company = models.ForeignKey('Profile')
	title   = models.CharField(max_length = 50)
	message = models.CharField(max_length = 50)
	date    = models.DateField(max_length = 50)

	def __str__(self):
		return str(self.profile.user.first_name) + ' ' + str(self.company)

class Company_Post(models.Model):
	company = models.ForeignKey('Company')
	photo   = models.ImageField(upload_to = "images/", default = "images/post_default.png")
	title   = models.CharField(max_length = 50)
	message = models.CharField(max_length = 50)
	date    = models.DateField(max_length = 50, default = timezone.now())

	def __str__(self):
		return str(self.date) + ' ' + str(self.company)

class Attendance(models.Model):
	profile = models.ForeignKey('Profile')
	time    = models.TimeField('Attendance time')

	def __str__(self):
		return str(self.profile) + str(self.time)

class Profile(models.Model):
	status = models.CharField(max_length = 10, default = "profile")
	index  = models.CharField(max_length = 60)
	qrcode = models.CharField(max_length = 60)
	user   = models.OneToOneField(User)
	city   = models.CharField(max_length = 50)

	cholesterol = models.IntegerField(default = 0)
	calories    = models.IntegerField(default = 0)

	avatar = models.ImageField(upload_to = "images/", default = "images/user_default.jpg")

	about  = models.CharField(max_length = 160)
	wishes = models.CharField(max_length = 160)

	def __str__(self):
		return str(self.user.first_name) + ' ' + str(self.user.last_name)

class Company(models.Model):
	status  = models.CharField(max_length = 10, default = "company")
	user    = models.OneToOneField(User)
	name    = models.CharField(max_length = 50)
	city    = models.CharField(max_length = 50)
	address = models.CharField(max_length = 100)

	avatar = models.ImageField(upload_to = "images/", default = "images/company_default.jpg")

	def __str__(self):
		return str(self.name) + ' ' + str(self.city)

# class Event(models.Model):
# 	profile = models.ForeignKey('Pupil', on_delete = models.CASCADE, null = True, blank =True)
# 	text    = models.CharField(max_length = 50)
# 	color   = models.CharField(max_length = 20, choices = COLOR, blank = True)
# 	time    = models.TimeField('event time')

# 	def __str__(self):
# 		return str(self.time) + " " + str(self.text)


# class Pupil(models.Model):
#     index       = models.CharField(max_length = 50)
#     qrcode      = models.CharField(max_length = 50)
#     name        = models.CharField(max_length = 50)
#     grade       = models.CharField(max_length = 50, choices = GRADE)
#     location    = models.CharField(max_length = 50, choices = LOCATION)
#     eating      = models.BooleanField(default = False)
#     inboard     = models.BooleanField(default = True)
#     status      = models.CharField(max_length = 50, default = "absent", choices = STATUS)

#     arrive_time	   = models.TimeField('time arrive', null = True, blank = True)
#     photo     	   = 
#     non_attendance = models.IntegerField(default = 0);

#     def __str__(self):
#     	return str(self.qrcode)

# class Order(models.Model):
# 	email       = models.CharField(max_length = 70)
# 	school_name = models.CharField(max_length = 100)
# 	message     = models.CharField(max_length = 300)
# 	date        = models.DateField('order date')

# 	def __str__(self):
# 		return str(self.school_name)
