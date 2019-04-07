from django.contrib import admin
from .models import Profile,Review,Company_Post,Attendance,Company

admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Attendance)

admin.site.register(Company)
admin.site.register(Company_Post)



