from django.contrib import admin
from .models import *
from django.core.mail import send_mail
from django.utils.html import format_html

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta


# Register your models here.

class CuricullamAdmin(admin.StackedInline):
    model = Curriculam
 
class featuresAdmin(admin.StackedInline):
    model = features


class timeAdmin(admin.StackedInline):
    model = timing


class videoAdmin(admin.StackedInline):
    model = video

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CuricullamAdmin,timeAdmin, videoAdmin]

    class Meta:
       model = Post



@admin.register(Curriculam)
class CuricullamAdmin(admin.ModelAdmin):
    pass

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


# class JobApplicationAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'phone_number', 'status', 'date_applied')
#     list_filter = ('status',)
#     search_fields = ('name', 'email', 'phone_number', 'status')
#
#     def save_model(self, request, obj, form, change):
#         old_obj = JobApplication.objects.get(pk=obj.pk) if obj.pk else None
#         super().save_model(request, obj, form, change)
#         if old_obj and old_obj.status != obj.status:
#             print(obj.status)
#             if obj.status == 'accepted':
#                 # Generate random password for new user account
#                 password = get_random_string(length=10)
#                 send_mail(
#                     f"Job Application Status: {obj.status}",
#                     f"Congratulations, your job application has been accepted!\n\nYour login credentials are:\nUsername: {obj.email}\nPassword: {password}\n\nYou can log in to the tutor dashboard at http://http://127.0.0.1:8000/tutor_login/",
#                     'minccedu@gmail.com',
#                     [obj.email],
#                     fail_silently=False,
#                 )
#


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'resume', 'status', 'date_applied')
    list_filter = ('status',)
    search_fields = ('name', 'email', 'phone_number', 'resume','status')

    def save_model(self, request, obj, form, change):
        old_obj = JobApplication.objects.get(pk=obj.pk) if obj.pk else None
        super().save_model(request, obj, form, change)
        if old_obj and old_obj.status != obj.status:
            if obj.status == 'interviewscheduled':
                interview_date = datetime.now() + timedelta(days=2)
                # interview_link = request.build_absolute_uri(reverse('interview'))
                send_mail(
                    f"Job Application Status: {obj.status}",
                    f"Interview scheduled for your job application.\n\nYou are invited to an online interview on {interview_date.strftime('%Y-%m-%d')} at {interview_date.strftime('%H:%M')}.\n\nPlease click on the following link to join the interview:\n https://us04web.zoom.us/j/74092072725?pwd=hqA9aCH4qSxJDqcoATYjExpbMq9O6V.1",
                    'minccedu@gmail.com',
                    [obj.email],
                    fail_silently=False,
                )
                if obj.status == 'accepted':
                    # Generate random password for new user account
                    password = get_random_string(length=3)
                    # Send login credentials to the applicant
                    send_mail(
                        f"Job Application Status: {obj.status}",
                        f"Congratulations, your job application has been accepted!\n\nYour login credentials are:\nUsername: {obj.email}\nPassword: {password}\n\nYou can log in to the tutor dashboard at http://http://127.0.0.1:8000/tutor_login/",
                        'minccedu@gmail.com',
                        [obj.email],
                        fail_silently=False,
                    )
                    if obj.status == 'rejected' or obj.status == 'pending':
                        send_mail(
                            f"Job Application Status: {obj.status}",
                            f"Your job application has been updated to {obj.status}.",
                            'minccedu@gmail.com',
                            [obj.email],
                            fail_silently=False,
                        )



                # Create a new Tutor object
                tutor = Tutor.objects.create(
                    job_application=obj,
                    name=obj.name,
                    email=obj.email,


                )
class TutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'job_application')
    search_fields = ('name', 'email', 'job_application__name')
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('status', 'created_at')

    def save_model(self, request, obj, form, change):
        old_obj = Vacancy.objects.get(pk=obj.pk) if obj.pk else None
        super().save_model(request, obj, form, change)
        if old_obj and old_obj.status != obj.status and obj.status == 'available':
            # Find all rejected job applications and send them a notification email
            rejected_applications = JobApplication.objects.filter(status='rejected')
            for application in rejected_applications:
                send_mail(
                    "Vacancy for Tutors Role Available",
                    "A vacancy for the Tutors role you applied for is now available. Please consider applying again if you are still interested.",
                    'minccedu@gmail.com',
                    [application.email],
                    fail_silently=False,
                )
admin.site.register(Vacancy, VacancyAdmin)

admin.site.register(Tutor, TutorAdmin)


admin.site.register(JobApplication, JobApplicationAdmin)



admin.site.register(Category)

admin.site.register(MainCourse)
admin.site.register(enrolledstudents)


admin.site.register(Order, OrderAdmin)
admin.site.register(passedstudents)
admin.site.register(subcat)



