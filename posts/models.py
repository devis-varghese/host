from django.db import models
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import time
import os
from edureka import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils import timezone
from embed_video.fields import EmbedVideoField

@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance._state.adding is True:
        print("Creating Inactive User")
        instance.is_active = False
    else:
        print("Updating User Record")

class enrolledstudents(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='media/profile_pic',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    Country = models.CharField(max_length=20,null=False, blank=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name

class JobApplication(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    resume = models.FileField(upload_to='media/resumes/')
    cover_letter = models.TextField()
    date_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('interviewscheduled', 'Interviewscheduled'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ))

    def __str__(self):
        return f"{self.name} - {self.date_applied}"


class Vacancy(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unavailable')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Vacancies'

    def __str__(self):
        return f'Vacancy {self.pk} - {self.status}'

class Tutor(models.Model):
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    assigned_courses = models.ManyToManyField('Post', blank=True, related_name='assigned_tutors')


    def __str__(self):
        return self.name



class Schedule(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    date_created = models.DateTimeField(default=timezone.now)


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank = True, null=True)
    title = models.CharField(max_length=100) 
    slug = AutoSlugField(populate_from='title', unique=True, null=False, editable=True)
    logo = models.ImageField(upload_to='media/catlogo', blank=True, null=True, help_text='Optional')
    logo1 = models.ImageField(upload_to='media/catlogo', blank=True, null=True, help_text='Optional')
    logo2 = models.ImageField(upload_to='media/catlogo', blank=True, null=True, help_text='Optional')
    top_three_cat = models.BooleanField(default=False)
    more = models.BooleanField(default=False, blank=True, verbose_name="For Add In Right Menu")
    created_at = models.DateTimeField(auto_now_add=True)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')
    hit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def post_count(self):
        return self.posts.all().count()    

    class Meta:

        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def __str__(self):                           
        full_path = [self.title]                  
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])    

class subcat(models.Model):
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcat', blank = True, null=True, help_text='Select Only Sub Category')
    title = models.CharField(max_length=100) 
    slug = AutoSlugField(populate_from='title', unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')

    def __str__(self):
        return self.title

    class Meta:
        #enforcing that there can not be two categories under a parent with same slug
        
        # __str__ method elaborated later in post.  use __unicode__ in place of

        unique_together = ('slug', 'parent',)
        #This is for outside or main which shows outside panel.    
        verbose_name_plural = "Sub Categories"     

    def __str__(self):                           
        full_path = [self.title]                  
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])    

class MainCourse(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, null=False, editable=True)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=500)

    slug = AutoSlugField(populate_from='title', max_length=500, unique=True, null=False)
    image = models.ImageField(upload_to='media/post')

    # logo = models.ImageField(upload_to='media/post') #If user want to add university logo(Slider and Post)
    desc = RichTextField(blank=True, null=True)
    #for live classes or offline classes

    youtube = models.URLField(max_length=500, default='' )
    # author = models.CharField(max_length=20, default="admin" )
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name="posts")
    subcategory = models.ForeignKey(subcat, on_delete=models.CASCADE, default=1, related_name="subcat", blank=True, null=True)

    button_text = models.CharField(max_length=20, default="Enroll Now") #Apply Now and enroll button text
    slider_post = models.BooleanField(default=False, blank=True)
    maincourse = models.ManyToManyField(MainCourse, blank=True, related_name='posts')
    price = models.IntegerField(default=0)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')
    assigned_tutor = models.ForeignKey('Tutor', on_delete=models.CASCADE, blank=True, null=True,related_name='assigned_posts')
    
    def __str__(self):
        return self.title    
        

class Curriculam(models.Model):
    title = models.CharField(max_length=500)
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='acc_posts')
    content = RichTextField(blank=True, null=True)

class timing(models.Model):
    date = models.CharField(max_length=100, blank=True, null=True)
    day_duration = models.CharField(max_length=100, blank=True, null=True)
    time_duration1 = models.CharField(max_length=100, blank=True, null=True)

    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='time_posts')

class features(models.Model):
    title = models.CharField(max_length=500)
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='feature_posts')
    content = RichTextField(blank=True, null=True)

class boxes_three(models.Model):
    title = models.CharField(max_length=70)
    slug = AutoSlugField(populate_from='title', unique=True, null=False, editable=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title    

class Cart(models.Model):
    cart_id = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='item')
    purchase = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.item}'

    def get_total(self):
        total = self.item.price
        float_total = format(total, '0.2f')
        return float_total    

class Order(models.Model):
    method = (
        ('EMI', "EMI"),
        ('ONLINE', "Online"),
    )
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, null = False, default='0')
    total = models.DecimalField(max_digits=10, default=0, decimal_places=2, verbose_name='INR ORDER TOTAL')
    emailAddress = models.EmailField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, null=True)
    order_id =  models.CharField(max_length=100, null=True)

    # objects = models.Manager()
    # client=order_id.client
    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        # if self.coupon:
        #     total -= self.coupon.amount
        return total


class passedstudents(models.Model):
    image= models.ImageField(upload_to='media/clients',null=True,blank=True)

class video(models.Model):
    title = models.CharField(max_length=100, null=False)
    post = post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='videos')
    serial_number = models.IntegerField(null=False)
    is_preview = models.BooleanField(default=False)
    desc = RichTextField(blank=True, null=True)
    # video_id = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class LiveClass(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='live_classes')
    url = models.URLField(max_length=200)
    def __str__(self):
        return self.url

class StudyMaterial(models.Model):
    title = models.CharField(max_length=100, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='study_materials')
    file = models.FileField(upload_to='study_materials/')
    desc = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.title

