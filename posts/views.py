from django.contrib.auth.hashers import check_password


from .models import *
from django.shortcuts import get_object_or_404, redirect, render
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as loginUser, update_session_auth_hash
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
import json
from time import time
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from edureka.settings import *
import razorpay
client = razorpay.Client(auth=('rzp_test_oE5GrnJfzSUqCP','xmxWct8JWngneVWqA3HtLCyZ'))
# Create your views here.

#for email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User


from django.http import HttpResponse
from django.shortcuts import render
import numpy as np

from collections import deque




def home(request):
    allposts = Post.objects.all().filter(maincourse=True)
    totalposts = Post.objects.all().order_by('-date')[:8]
    slider_post = Post.objects.all().filter(slider_post=True)
    top_three_catg = Category.objects.filter(top_three_cat=True)[:3]
    main_course = MainCourse.objects.all()
    allcat = Category.objects.all()
    categories = Category.objects.all().filter(top_three_cat=False).filter(more=False).order_by('-created_at')[:7]
    footcategories = Category.objects.filter(parent=None)[:2]
    catg = Category.objects.all().exclude(parent=None).order_by('-created_at')[:7]
    # catg_parent = Category.objects.all().exclude(parent=True).order_by('-hit')
    latest_catg = Category.objects.filter(parent=None)[:5]
    latest_catg_all = Category.objects.filter(parent=None)[5:]
    latest_post = Post.objects.order_by('-date')[:4]

    context = {'allposts':allposts, 'main_course':main_course, 'top_three_catg':top_three_catg, 'catg':catg, 'slider_post':slider_post, 'latest_catg':latest_catg, 'latest_post':latest_post, 'totalposts':totalposts, 
    
    # 'catg_parent':catg_parent,
     'allcat':allcat, 'categories':categories, 'footcategories':footcategories, 'latest_catg_all':latest_catg_all}
    return render(request, 'core/index.html', context)

def totalposts(request):
    total = Post.objects.all()
    context = {'total':total}
    return render(request, 'core/total.html', context)


def job_application(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            send_mail(
                'Job Application Received',
                'You have successfully applied for the job as a tutor. We will let you know if you are hired.',
                'minccedu@gmail.com',
                [form.cleaned_data['email']],
                fail_silently=False,
            )
            return render(request, 'core/thankyou.html')
    else:
        form = JobApplicationForm()

    return render(request, 'core/jobapplication.html', {'form': form})


class TutorLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

def tutorlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        tutor = authenticate(request, email=email, password=password)
        if tutor is not None and tutor.status == 'accepted':
            login(request, tutor)
            return redirect('tutor_dashboard')
        else:
            error_msg = 'Invalid email or password'
            return render(request, 'users/tutorlogin.html', {'error_msg': error_msg})
    else:
        return render(request, 'users/tutorlogin.html')


# def tutorlogin(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         tutor = Tutor.objects.filter(email=email, password=password).first()
#         if tutor is not None:
#             user = authenticate(request, email=email, password=password)
#             login(request,user)
#             return redirect('tutor_dashboard')
#         else:
#             error_msg = 'Invalid email or password'
#             return render(request, 'users/tutorlogin.html', {'error_msg': error_msg})
#     else:
#         return render(request, 'users/tutorlogin.html')
# @login_required
def tutor_dashboard(request):
    tutor = request.user
    # Use the tutor object to display information on the dashboard page
    return render(request, 'users/tutor_dashboard.html', {'tutor': tutor})


def all_tutors(request):
    accepted_applications = JobApplication.objects.filter(status='accepted')
    return render(request, 'webadmin/alltutors.html', {'tutors': accepted_applications})

def schedule_view(request):
    tutor = request.user.tutor # get the tutor object from the logged in user
    schedule = Schedule.objects.filter(tutor=tutor)
    context = {'schedule': schedule}
    return render(request, 'webadmin/schedule.html', context)





def post_by_category(request, catslug):
    posts = Post.objects.all()
    cat_post = Post.objects.filter(category__slug=catslug)
    allposts = Post.objects.all().filter(maincourse=True)
    slider_post = Post.objects.all().filter(slider_post=True)
    top_three_catg = Category.objects.filter(top_three_cat=True)[:3]
    main_course = MainCourse.objects.all()
    allcat = Category.objects.all()
    categories = Category.objects.filter(parent=None).order_by('-created_at')[:7]
    footcategories = Category.objects.filter(parent=None)[:2]
    catg = Category.objects.all().exclude(parent=None).order_by('-created_at')[:7]
    catg_parent = Category.objects.all().exclude(parent=True)
    latest_catg = Category.objects.filter(parent=None)[:5]
    latest_post = Post.objects.order_by('-date')[:4]
    latest_catg_all = Category.objects.filter(parent=None)[5:]
    # rev = Reviews.objects.all().order_by('-created')[:6]
    context = {'latest_catg_all':latest_catg_all, 'rev':rev, 'posts':posts, 'cat_post':cat_post,'allposts':allposts, 'main_course':main_course, 'top_three_catg':top_three_catg, 'catg':catg, 'slider_post':slider_post, 'latest_catg':latest_catg, 'latest_post':latest_post}
    return render(request, 'core/index.html', context)

def allpost_by_category(request, postslug):
    posts = Post.objects.all()
    cat_post = Post.objects.filter(category__slug=postslug)
    subcat_post = Post.objects.filter(subcategory__slug=postslug)
    allposts = Post.objects.all().filter(maincourse=True)
    allcat = Category.objects.all()
    context = {'posts':posts,'subcat_post':subcat_post, 'cat_post':cat_post,'allposts':allposts,'allcat':allcat,}
    return render(request, 'core/allposts.html', context)

def subcat_by_category(request, subcatslug):
    allcats = get_object_or_404(Category, slug=subcatslug)
    category = subcat.objects.filter(slug=subcatslug)
    # allsubcatg = allcats.subcat.filter(parent__slug=slug)
    cat_subcat = subcat.objects.filter(parent__slug=subcatslug)
    context = {'cat_subcat':cat_subcat, 'category':category, 'allcats':allcats}
    return render(request, 'core/catg_subcat.html', context)
  
def post_details(request, category_slug, slug):
    posts = Post.objects.filter(slug=slug).first()
    category = Post.objects.filter(slug=category_slug)
    catg_parent = Category.objects.all().exclude(parent=True)    
    allcat = Category.objects.all()
    allpost = get_object_or_404(Post, slug=slug)
    #for add curriculam 
    curriculam = Curriculam.objects.filter(Post=allpost)
    #for class features
    feature = features.objects.filter(Post=allpost)
    #for Timing
    time = timing.objects.filter(Post=allpost)    
    #for Videos
    vid = video.objects.filter(post=allpost)

    context = {'posts':posts, 'category':category, 'allcat':allcat, 'catg_parent':catg_parent, 'curriculam':curriculam, 'allpost':allpost,'features':feature, 'time':time, 'videos':vid}
    return render(request, 'core/details.html', context)

def search(request):
    search = request.GET['search']
    totalposts = Post.objects.filter(title__icontains=search)
    context = {'totalposts':totalposts, 'search':search}
    return render(request, 'core/search.html', context)

def videos(request):
    return render(request, 'core/videos.html')

def vr_mode(request):
    return render(request, 'core/vr_mode.html')

def courses(request):
    main_course = MainCourse.objects.all()
    context = {'main_course':main_course}
    return render(request, 'core/courses.html', context)




@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = request.POST
        context = {}
        print(data)
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            order = Order.objects.get(order_id=razorpay_order_id)
            order.payment_id = razorpay_payment_id
            order.ordered = True
            order.save()
            cart_items = Cart.objects.filter(user=request.user, purchase=False)
            for item in cart_items:
                item.purchase = True
                item.save()
            return redirect('userhome')
        except:
            return HttpResponse("Invalid Payment Details")    

# UserSignup Form
def signup(request):
    next_page = request.GET.get('next')
    form=CustomerCreationForm()
    customerForm=CustomerForm()
    mydict={'form':form,'customerForm':customerForm}
    if request.method=='POST':
        form = CustomerCreationForm(request.POST)
        customerForm=CustomerForm(request.POST,request.FILES)
        if form.is_valid() and customerForm.is_valid():
            user = form.save()
            user.email = user.username
            user.save()
            email=user.email
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                messages.success(request, 'Thank you for registering with us.')
                messages.success(request, 'Please verify your email for login!')

                current_site = get_current_site(request)
                message = render_to_string('core/account_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })

                send_mail(
                    'Please activate your account',
                    message,
                    'minccedu@gmail.com',
                    [email],
                    fail_silently=False,
                )
                # to_email = form.cleaned_data.get('email')
                # send_mail(mail_subject, message, 'youremail', [to_email])

                return redirect('/login/?command=verification&email=' + email)
                # return redirect('userlogin')
    context = {'form':form, 'customerForm':customerForm}
    return render(request, 'users/signup.html', context)



# def signup(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
#         address = request.POST.get('address')
#         mobile = request.POST.get('mobile')
#         profile_pic = request.FILES.get('profile_pic')
#
#         # Perform validation on form data
#         errors = {}
#         if not username:
#             errors['username'] = 'Email is required.'
#         elif User.objects.filter(username=username).exists():
#             errors['username'] = 'Email is already taken.'
#         if not first_name:
#             errors['first_name'] = 'First name is required.'
#         if not last_name:
#             errors['last_name'] = 'Last name is required.'
#         if not password1:
#             errors['password1'] = 'Password is required.'
#         elif len(password1) < 8:
#             errors['password1'] = 'Password must be at least 8 characters long.'
#         if password1 != password2:
#             errors['password2'] = 'Passwords do not match.'
#         if not address:
#             errors['address'] = 'Address is required.'
#         if not mobile:
#             errors['mobile'] = 'Mobile number is required.'
#         elif len(mobile) != 10:
#             errors['mobile'] = 'Mobile number must be 10 digits long.'
#
#         if errors:
#             context = {'errors': errors, 'form_data': request.POST}
#             return render(request, 'users/signup.html', context)
#
#         # Create the new User and enrolledstudents objects
#         user = User.objects.create_user(username=username, password=password1, first_name=first_name,
#                                         last_name=last_name)
#         user.email = username
#         user.save()
#         customer = enrolledstudents.objects.create(user=user, address=address, mobile=mobile, profile_pic=profile_pic)
#
#         # Add the user to the CUSTOMER group
#         my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
#         my_customer_group[0].user_set.add(user)
#
#         # Send account verification email
#         email = user.email
#         messages.success(request, 'Thank you for registering with us.')
#         messages.success(request, 'Please verify your email for login!')
#
#         current_site = get_current_site(request)
#         message = render_to_string('core/account_verification_email.html', {
#             'user': user,
#             'domain': current_site,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': default_token_generator.make_token(user),
#         })
#
#         send_mail(
#             'Please activate your account',
#             message,
#             'minccedu@gmail.com',
#             [email],
#             fail_silently=False,
#         )
#
#         return redirect('/login/?command=verification&email=' + email)
#
#     return render(request, 'users/signup.html')


# UserSignup Form
# def login(request):
#     if request.method == 'GET':
#         form = Customerloginform() #This comes from forms.py
#         next_page = request.GET.get('next') #If url has next value so this function will redirect the user on next page url
#         context = {'form':form}
#         return render(request, 'users/login.html', context)
#     else:
#         form = Customerloginform(data=request.POST) #This comes from forms.py
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user:
#                 loginUser(request, user) #We use loginUser here because yaha 2 login ho gye hai to alag se import kiya hai isko humne
#             # messages.success(request, "Welcome Sir")
#             #If url has next value so this function will redirect the user on next page url
#             if 'next' in request.POST:
#                 return redirect(request.POST.get('next'))
#             else:
#                 return redirect('userhome')
#         else:
#             context = {'form':form}
#             return render(request, 'users/login.html', context)


def login(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'users/login.html', context)
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            loginUser(request, user)
            return redirect('home')
        else:
            context = {}
            return render(request, 'users/login.html', context)



def logout(request):
    request.session.clear()
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user =User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('userlogin')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('usersignup')

def userdashboard(request):
    customer = enrolledstudents.objects.all()
    carts = Cart.objects.filter(user=request.user, purchase=True)
    orders = Order.objects.filter(user=request.user, ordered=True)
    if orders.exists() and carts.exists():
        order = orders[0]
        return render(request, 'users/index.html', context={'carts':carts,'orders':orders})
    context = {'carts':carts,'customer':customer, 'orders':orders}
    return render(request, 'users/index.html', context)
def enter_course(request, slug):
    allpost = get_object_or_404(Post, slug=slug)
    context = {'allpost': allpost}
    # You can add your custom logic here to enter the user into the course
    return render(request, 'webadmin/enter_course.html', context)

def paid_video(request, slug):
    allpost = get_object_or_404(Post, slug=slug)
    vid = video.objects.filter(post=allpost)
    context = {'allpost':allpost, 'vid':vid}
    return render(request, 'users/video.html', context)

def live_class(request, slug):
    allpost = get_object_or_404(Post, slug=slug)
    live_classes = LiveClass.objects.filter(post=allpost)
    context = {'allpost': allpost, 'live_classes': live_classes}
    return render(request, 'webadmin/live_class.html', context)

def study_material(request, slug):
    allpost = get_object_or_404(Post, slug=slug)
    study_materials = StudyMaterial.objects.filter(post=allpost)
    context = {'allpost': allpost, 'study_materials': study_materials}
    return render(request, 'webadmin/study_material.html', context)

# def course_details(request, slug):
#     allpost = get_object_or_404(Post, slug=slug)
#     vid = video.objects.filter(post=allpost)
#     context = {'allpost': allpost, 'vid': vid}
#
#     if request.method == 'POST':
#         # Custom logic to enter user into course goes here
#         pass
#
#     return render(request, 'webadmin/enter_course.html', context)


def userprofile(request):
    profile = enrolledstudents.objects.get(user_id=request.user.id)
    context = {'profile':profile}
    return render(request, 'users/profile.html', context)

def edit_profile(request):
    if request.method == 'POST':
        user_form = CustomerCreationEditForm(request.POST or None, request.FILES or None, instance=request.user)
        profile_form = CustomerEditForm(request.POST or None, request.FILES or None, instance=request.user.enrolledstudents)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            # print(user_form)
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = CustomerCreationEditForm(instance=request.user)
        profile_form = CustomerEditForm(instance=request.user.enrolledstudents)
    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('userhome')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/edit_password.html', {
        'form': form
    })


# @login_required(login_url='/login/')
# def add_to_cart(request, slug):
#     course = get_object_or_404(Post, slug=slug)
#     order_item = Cart.objects.get_or_create(item=course, user=request.user, purchase=False)
#     order_object = Order.objects.filter(user=request.user, ordered=False)
#     if order_object.exists():
#         order = order_object[0]
#         if order.orderitems.filter(item=course).exists():
#             messages.success(request, "You already enrolled this course")
#             return redirect('cart')
#         else:
#             order.orderitems.add(order_item[0])
#             messages.success(request, "You have Enrolled for this course,Complete Payment to continue to course!")
#             return redirect('cart')
#     else:
#         order = Order(user= request.user)
#         order.save()
#         order.orderitems.add(order_item[0])
#         messages.success(request, "You have Enrolled for this course,Complete Payment to continue to course!")
#         return redirect('cart')

@login_required
def add_to_cart(request, slug):
    course = get_object_or_404(Post, slug=slug)
    order_object = Order.objects.filter(user=request.user, ordered=True)
    if order_object.exists():
        messages.error(request, "You have already purchased a course and cannot purchase another.")
        return redirect('cart')
    order_item, created = Cart.objects.get_or_create(item=course, user=request.user, purchase=False)
    order_object = Order.objects.filter(user=request.user, ordered=False)
    if order_object.exists():
        order = order_object[0]
        if order.orderitems.filter(item=course).exists():
            messages.error(request, "You have already enrolled in this course. Please complete the payment to continue.")
            return redirect('cart')
        else:
            order.orderitems.add(order_item)
            order.save()
            messages.success(request, "You have successfully enrolled in this course. Please complete the payment to continue.")
            return redirect('cart')
    else:
        order = Order.objects.create(user=request.user)
        order.orderitems.add(order_item)
        order.save()
        messages.success(request, "You have successfully enrolled in this course. Please complete the payment to continue.")
        return redirect('cart')

def checkout(request):
    user = None

    if request.method == 'get':
        try:
            orders = Order.objects.get(user=request.user, ordered=False)
            context = {'orders':orders}
            return render(request, 'core/checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(request, 'You do not have an active order')
            return redirect('checkout')
    
    orders = Order.objects.filter(user=request.user, ordered=False)           
    user = request.user        
    if orders.exists():
        order = orders[0]
    orderss = None    
    order_payment = None
    action = request.GET.get('action')    
    if action == 'create_payment':
        amount = int(order.get_totals() * 100)
        currency = "INR"
        receipt = f"MINCC-{int(time())}"
        notes = {
                "email": user.email,
                "name": f'{user.first_name} {user.last_name}'
        }
        orderss = client.order.create({
        'amount':amount,
        'currency':currency,
        'receipt':receipt,
        'notes':notes
        })

        orders = Order.objects.filter(user=request.user, ordered=False)    
        order_payment = orders[0]
        order_payment.user = user
        order_payment.emailAddress = user.email

        order_payment.order_id = orderss.get('id')
        order_payment.total = orderss.get('amount')
        order_payment.save()
    context = {'orderss':orderss, 'order_payment':order_payment, 'orders':orders, 'order':order}
    return render(request, 'core/checkout.html', context)





@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchase=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'core/cart.html', context={'carts':carts,'order':order,'orders':orders})
    else:
        messages.warning(request, "")
        return redirect('userhome')

# @login_required
# def order_view(request):
#     orders = Order.objects.filter(user=request.user, ordered=True)
#     context = {'orders':orders}
#     return render(request, "users/index.html", context)


def remove_from_cart(request, id):
    item = get_object_or_404(Post, id=id)
    order_obj = Order.objects.filter(user=request.user, ordered=False)
    if order_obj.exists():
        order = order_obj[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchase=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "you unenrolled this course")
            return redirect("cart")
        else:
            messages.info(request, "you have not enrolled this course")
            return redirect("cart")
    else:
        messages.info(request,"You are not enrolled in any courses")
        return redirect("home")



def webadmin(request):
    postcount = Post.objects.all().count()
    catcount = Category.objects.all().count()
    usercount = User.objects.all().count()
    orders = Order.objects.all()
    context = {'postcount':postcount, 'cat':catcount, 'user':usercount,"orders":orders}
    return render(request, 'webadmin/index.html', context)  




def add_post(request):
    posts= PostForm()
    if request.method=='POST':
        posts=PostForm(request.POST, request.FILES)
        if posts.is_valid():
            posts.save()
        messages.success(request, "Posts Added Sucessfully !!")    
        return redirect('allposts')
    return render(request, "webadmin/addpost.html", {'post':posts})


def add_course(request):
    course= Maincourse()
    if request.method=='POST':
        course=Maincourse(request.POST, request.FILES)
        if course.is_valid():
            course.save()
        messages.success(request, "Course Added Sucessfully !!")    
        return redirect('allcourses')
    return render(request, "webadmin/addcourse.html", {'course':course})


def add_cat(request):
    category= CatForm()
    if request.method=='POST':
        category=CatForm(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addcat.html", {'category':category})

def add_curriculam(request):
    category= CatForm()
    if request.method=='POST':
        category=CatForm(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('webadmin')
    return render(request, "webadmin/addcat.html", {'category':category})

#This is for show all Posts in Custom Admin Panel
def allposts(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'webadmin/allposts.html', context)

#This is for show all Users in Custom Admin Panel
def allusers(request):
    # users = User.objects.all()
    customer = enrolledstudents.objects.all()
    context = {
        # 'users':users
    'customer':customer
    }
    return render(request, 'webadmin/allusers.html', context)

def userdetails(request, id):
    customer = enrolledstudents.objects.filter(id=id).first()
    context = {'customer':customer}
    return render(request, 'webadmin/user_detail.html', context)

def allorders(request):
    orders = Order.objects.filter(ordered=True)
    carts = Cart.objects.all()
    context = {
    'orders':orders, 'carts':carts,
    }
    return render(request, 'webadmin/allorders.html', context)


    
#This is for show all Categories in Custom Admin Panel
def allcat(request):
    cat = Category.objects.filter(parent=None).order_by('hit')
    context = {'cat':cat}
    return render(request, 'webadmin/allcat.html', context)

def allcourse(request):
    course = MainCourse.objects.all()
    context = {'course':course}
    return render(request, 'webadmin/allcourse.html', context)

def edit_post(request, id):
    if request.method == 'POST':
        posts = Post.objects.get(id=id)
        editpostForm= EditPostForm(request.POST or None, request.FILES or None, instance=posts)
        if editpostForm.is_valid():
            editpostForm.save()
        messages.success(request, "Post Update Sucessfully !!")
        return redirect('allposts')
    else:
        posts = Post.objects.get(id=id)
        editpostForm= EditPostForm(instance=posts)

    return render(request, "webadmin/editposts.html", {'editpost':editpostForm})
    
def delete_post(request, id):
    delete = Post.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Post Deleted Successfully.")
    return redirect('allposts')


#For edit the categories
def edit_cat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= CatForm(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= CatForm(instance=cat)

    return render(request, "webadmin/editcat.html", {'editcat':editcatForm})

#For delete the categories    
def delete_cat(request, id):
    delete = Category.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Category Deleted Successfully.")
    return redirect('allcat')


#For edit the course
def edit_course(request, id):
    if request.method == 'POST':
        course = MainCourse.objects.get(id=id)
        editcourse= EditMaincourse(request.POST or None, request.FILES or None, instance=course)
        if editcourse.is_valid():
            editcourse.save()
        messages.success(request, "Course Update Sucessfully !!")
        return redirect('allcat')
    else:
        cat = MainCourse.objects.get(id=id)
        editcourse= EditMaincourse(instance=cat)

    return render(request, "webadmin/editcourse.html", {'editcourse':editcourse})

#For delete the course
def delete_course(request, id):
    delete = MainCourse.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "MainCourse Deleted Successfully.")
    return redirect('allcourses')    


    

def add_videos(request):
    video= videoform()
    if request.method=='POST':
        video=videoform(request.POST, request.FILES)
        if video.is_valid():
            video.save()
        messages.success(request, "video Added Sucessfully !!")    
        return redirect('home')
    return render(request, "webadmin/addvideo.html", {'video':video})

def edit_videos(request, id):
    if request.method == 'POST':
        vid = video.objects.get(id=id)
        editvideoForm= videoform(request.POST or None, request.FILES or None, instance=vid)
        if editvideoForm.is_valid():
            editvideoForm.save()
        messages.success(request, "Video Update Sucessfully !!")
        return redirect('allcat')
    else:
        vid = video.objects.get(id=id)
        editvideoForm= videoform(instance=vid)

    return render(request, "webadmin/editvideo.html", {'editvideo':editvideoForm})

def delete_video(request, id):
    delete = video.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "video Deleted Successfully.")
    return redirect('allcourses')   

# def allvideos(request):
#     vid = video.objects.all()
#     context = {'video':vid}
#     return render(request, 'webadmin/allvideo.html', context)






def alltime(request):
    f = timing.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/alltime.html', context)

def add_time(request):
    time= timingform()
    if request.method=='POST':
        time= timingform(request.POST, request.FILES)
        if time.is_valid():
            time.save()
        messages.success(request, "Timings Added Sucessfully !!")    
        return redirect('alltime')
    return render(request, "webadmin/add_time.html", {'time':time})

def edit_time(request, id):
    if request.method == 'POST':
        time = timing.objects.get(id=id)
        Edittimingform= timingform(request.POST, instance=time)
        if Edittimingform.is_valid():
            Edittimingform.save()
        messages.success(request, "Timings Update Sucessfully !!")
        return redirect('alltime')
    else:
        time = timing.objects.get(id=id)
        Edittimingform= timingform(instance=time)   

    return render(request, "webadmin/edit_time.html", {'time':Edittimingform})

def delete_time(request, id):
    delete = timing.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Timing Deleted Successfully.")
    return redirect('alltime') 

def allfeatures(request):
    f = features.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allfeatures.html', context)

def add_features(request):
    features= featuresform()
    if request.method=='POST':
        features= featuresform(request.POST, request.FILES)
        if features.is_valid():
            features.save()
        messages.success(request, "Timings Added Sucessfully !!")    
        return redirect('allfeatures')
    return render(request, "webadmin/add_features.html", {'features':features})

def edit_features(request, id):
    if request.method == 'POST':
        feat = features.objects.get(id=id)
        editfeatures = featuresform(request.POST, instance=feat)
        if editfeatures .is_valid():
            editfeatures .save()
        messages.success(request, "featuress Update Sucessfully !!")
        return redirect('allfeatures')
    else:
        feat = features.objects.get(id=id)
        editfeatures = featuresform(instance=feat)   

    return render(request, "webadmin/edit_features.html", {'features':editfeatures })

def delete_features(request, id):
    delete = features.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Features Deleted Successfully.")
    return redirect('allfeatures') 

def allcurriculam(request):
    f = Curriculam.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allcurriculam.html', context)

def add_curriculam(request):
    curr= Curriculamform()
    if request.method=='POST':
        curr= Curriculamform(request.POST, request.FILES)
        if curr.is_valid():
            curr.save()
        messages.success(request, "Curriculam Added Sucessfully !!")    
        return redirect('allcurriculam')
    return render(request, "webadmin/add_curr.html", {'curr':curr})

def edit_curriculam(request, id):
    if request.method == 'POST':
        curr = Curriculam.objects.get(id=id)
        editcurr = Curriculamform(request.POST, instance=curr)
        if editcurr.is_valid():
            editcurr.save()
        messages.success(request, "Curriculam Update Sucessfully !!")
        return redirect('allcurriculam')
    else:
        curr = Curriculam.objects.get(id=id)
        editcurr = Curriculamform(instance=curr)   

    return render(request, "webadmin/edit_curriculam.html", {'editcurr':editcurr })

def delete_curriculam(request, id):
    delete = Curriculam.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Curriculam Deleted Successfully.")
    return redirect('allcurriculam') 

def allsubcatg(request):
    f = subcat.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allsubcat.html', context)

def add_subcatg(request):
    sub= subcatg()
    if request.method=='POST':
        sub= subcatg(request.POST, request.FILES)
        if sub.is_valid():
            sub.save()
        messages.success(request, "Subcat Added Sucessfully !!")    
        return redirect('allsubcatg')
    return render(request, "webadmin/add_subcat.html", {'sub':sub})

def edit_subcatg(request, id):
    if request.method == 'POST':
        sub = subcat.objects.get(id=id)
        editsub = subcatg(request.POST, instance=sub)
        if editsub.is_valid():
            editsub.save()
        messages.success(request, "Subcat Update Sucessfully !!")
        return redirect('allsubcatg')
    else:
        sub = subcat.objects.get(id=id)
        editsub = subcatg(instance=sub)   

    return render(request, "webadmin/edit_subcat.html", {'subcat':editsub })

def delete_subcatg(request, id):
    delete = subcat.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Subcat Deleted Successfully.")
    return redirect('allsubcatg') 

def add_leftcat(request):
    category= leftmenu()
    if request.method=='POST':
        category=leftmenu(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addleftcat.html", {'category':category})

#For edit the categories
def edit_leftcat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= leftmenu(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= leftmenu(instance=cat)

    return render(request, "webadmin/editleftcat.html", {'editcat':editcatForm})

def add_middlecat(request):
    category= middlemenu()
    if request.method=='POST':
        category=middlemenu(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addmiddlecat.html", {'category':category})

#For edit the categories
def edit_middlecat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= middlemenu(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= middlemenu(instance=cat)

    return render(request, "webadmin/editmiddlecat.html", {'editcat':editcatForm})

def add_rightcat(request):
    category= rightmenu()
    if request.method=='POST':
        category=rightmenu(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addrightcat.html", {'category':category})

#For edit the categories
def edit_rightcat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= rightmenu(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= rightmenu(instance=cat)

    return render(request, "webadmin/editrightcat.html", {'editcat':editcatForm})

def allvideos(request):
    videos = [
        {
            'title': 'Video 1',
            'url': 'https://example.com/video1.mp4',
            'description': 'This is the first video'
        },
        {
            'title': 'Video 2',
            'url': 'https://example.com/video2.mp4',
            'description': 'This is the second video'
        },
        {
            'title': 'Video 3',
            'url': 'https://example.com/video3.mp4',
            'description': 'This is the third video'
        }
    ]
    return render(request, 'videos.html', {'videos': videos})

