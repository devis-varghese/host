from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
# from django.conf.urls import url


urlpatterns = [
    path('', views.home, name='home'),
    #Custom admin panel urls
    path('webadmin/', views.webadmin, name='webadmin'),
    path('addpost/', views.add_post, name='addpost'),
    path('addcat/', views.add_cat, name='addcat'),
    path('webadmin/addleftcat/', views.add_leftcat, name='addleftcat'),
    path('webadmin/addmiddlecat/', views.add_middlecat, name='addmiddlecat'),
    path('webadmin/addrightcat/', views.add_rightcat, name='addrightcat'),
    path('addvideo/', views.add_videos, name='addvideo'),
    path('add_course/', views.add_course, name='addcourse'),
    path('allposts/', views.allposts, name='allposts'),
    path('allcat/', views.allcat, name='allcat'),
    path('allusers/', views.allusers, name='allusers'),
    path('allcourse/', views.allcourse, name='allcourses'),

    path('allorders/', views.allorders, name='allorders'),

    path('allvideos/', views.allvideos, name='allvideos'),
    # path('orderdetail/<int:id>', views.order_details, name='orderdetail'),
    path('webadmin/editpost/<int:id>', views.edit_post, name='editpost'),
    path('webadmin/deletepost/<int:id>', views.delete_post, name='deletepost'),
    path('webadmin/editcat/<int:id>', views.edit_cat, name='editcat'),
    path('webadmin/editvideo/<int:id>', views.edit_videos, name='editvideo'),
    path('webadmin/deletecat/<int:id>', views.delete_cat, name='deletecat'),
    path('webadmin/deletevideo/<int:id>', views.delete_video, name='deletevideo'),
    path('webadmin/editcourse/<int:id>', views.edit_course, name='editcourse'),
    path('webadmin/deletecourse/<int:id>', views.delete_course, name='deletecourse'),
    path('webadmin/add_time/', views.add_time, name='add_time'),
    path('webadmin/edit_time/', views.edit_time, name='edit_time'),
    path('webadmin/delete_time/', views.delete_time, name='delete_time'),
    path('webadmin/alltime/', views.alltime, name='alltime'),
    path('webadmin/add_features/', views.add_features, name='add_features'),
    path('webadmin/edit_features/<int:id>', views.edit_features, name='edit_features'),
    path('webadmin/delete_features/<int:id>', views.delete_features, name='delete_features'),
    path('webadmin/allfeatures/', views.allfeatures, name='allfeatures'),
    path('webadmin/add_curriculam/', views.add_curriculam, name='add_curriculam'),
    path('webadmin/edit_curriculam/', views.edit_curriculam, name='edit_curriculam'),
    path('webadmin/delete_curriculam/', views.delete_curriculam, name='delete_curriculam'),
    path('webadmin/allcurriculam/', views.allcurriculam, name='allcurriculam'),
    path('webadmin/add_subcatg/', views.add_subcatg, name='add_subcatg'),
    path('webadmin/edit_subcatg/<int:id>', views.edit_subcatg, name='edit_subcatg'),
    path('webadmin/delete_subcatg/<int:id>', views.delete_subcatg, name='delete_subcatg'),
    path('webadmin/allsubcatg/', views.allsubcatg, name='allsubcatg'),


    #User panel urls
    path('login/', views.login, name='userlogin'),
    path('usersignup/', views.signup, name='usersignup'),
    path('userlogout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('userdashboard/', views.userdashboard, name='userhome'),
    path('userprofile/', views.userprofile, name='profile'),
    path('userdetail/<int:id>', views.userdetails, name='userdetails'),
    path('edituserprofile/', views.edit_profile, name='editprofile'),
    path('changepassword/', views.change_password, name='changepassword'),



    #Public urls

    path('add/<str:slug>', views.add_to_cart, name='add'),

    path('cart/', views.cart_view, name='cart'),
    path('removecart/<int:id>', views.remove_from_cart, name='removecart'),
    path('search/', views.search, name='search'),

    path('filter/<str:catslug>', views.post_by_category, name='catpost'),

    path('subcat/<str:subcatslug>', views.subcat_by_category, name='subcat'),

    path('<str:postslug>', views.allpost_by_category, name='allcatpost'),
    path('<str:category_slug>/<str:slug>', views.post_details, name='details'),
    path('videos/', views.videos, name='videos'),
    path('users/yourcoursesvideo/<str:slug>/', views.paid_video, name='paid_video'),
    path('course/<slug:slug>/', views.enter_course, name='enter_course'),
    path('post/<slug:slug>/live-class/', views.live_class, name='live_class'),
    path('vr_mode/', views.vr_mode, name='vr_mode'),
    path('post/<slug:slug>/study-material/', views.study_material, name='study_material'),

    path('courses/', views.courses, name='courses'),            

    path('checkout/', views.checkout, name='checkout'), 

    path('verify_payment/', views.verify_payment, name='verify_payment'), 
    path('allcourses/', views.totalposts, name='all-courses'),
    path('alltutors/', views.all_tutors, name='alltutors'),
    path('tutorlogin/', views.tutorlogin, name='tutor_login'),
    path('tutordashboard/', views.tutor_dashboard, name='tutor_dashboard'),
    path('schedule/', views.schedule_view, name='schedule'),
    
    path('apply/', views.job_application, name='job_application'),





] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
