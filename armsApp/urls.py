from django.contrib import admin
from django.urls import path,include
from . import views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.search_flight, name='public-page'),
    path('search_result',views.search_result, name="search-result"),
    path('search_result/<int:fromA>/<int:toA>/<str:departure>',views.search_result, name="search-result"),
    path('reserve_form/<int:pk>',views.reserve_form,name='reserve-form'),
    path('save_reservation',views.save_reservation,name='save-reservation'),
    path('home',views.home, name="home-page"),
    path('login',views.login_page,name='login-page'),
    path('register',views.userregister,name='register-page'),
    path('save_register',views.save_register,name='register-user'),
    path('user_login',views.login_user,name='login-user'),
    path('home',views.home,name='home-page'),
    path('logout',views.logout_user,name='logout'),
    path('profile',views.profile,name='profile-page'),
    path('update_password',views.update_password,name='update-password'),
    path('update_profile',views.update_profile,name='update-profile'),
    path('airline',views.list_airline,name='airline-page'),
    path('manage_airline',views.manage_airline,name='manage-airline'),
    path('manage_airline/<int:pk>',views.manage_airline,name='manage-airline-pk'),
    path('save_airline',views.save_airline,name='save-airline'),
    path('delete_airline/<int:pk>',views.delete_airline,name='delete-airline-pk'),
    path('airport',views.list_airport,name='airport-page'),
    path('manage_airport',views.manage_airport,name='manage-airport'),
    path('manage_airport/<int:pk>',views.manage_airport,name='manage-airport-pk'),
    path('save_airport',views.save_airport,name='save-airport'),
    path('delete_airport/<int:pk>',views.delete_airport,name='delete-airport-pk'),
    path('flight',views.list_flight,name='flight-page'),
    path('manage_flight',views.manage_flight,name='manage-flight'),
    path('manage_flight/<int:pk>',views.manage_flight,name='manage-flight-pk'),
    path('view_flight/<int:pk>',views.view_flight,name='view-flight-pk'),
    path('save_flight',views.save_flight,name='save-flight'),
    path('delete_flight/<int:pk>',views.delete_flight,name='delete-flight-pk'),
    path('reservation',views.list_reservation,name='reservation'),
    path('view_reservation/<int:pk>',views.view_reservation,name='view-reservation-pk'),
    path('delete_reservation/<int:pk>',views.delete_reservation,name='delete-reservation-pk'),
    path('update_reservation',views.update_reservation,name='update-reservation'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
