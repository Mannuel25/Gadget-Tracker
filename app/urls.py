from django.urls import path
from .views import *

# app_name = "app"

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('upload_users/', upload, name='upload_users'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('signup/', signup_user, name='signup'),
    path('students/', all_students, name='all_students'),
    path('staff/', all_staff, name='all_staff'),
    path('vendors/', all_vendors, name='all_vendors'),
    path('users/delete/<int:id>', delete_user, name='delete_user'),
    path('create_user/', UserGadgetsCreate.as_view(), name='create_user'),
    path('update/<int:pk>/', UserGadgetsUpdate.as_view(), name='update_user'),
    path('gadgets/delete/<int:id>/', delete_gadget, name='delete_gadget'),
    path('download_template/', download_template, name='download_template'),
    path('missing_gadgets/', missing_gadgets, name='missing_gadgets'),
    path('gadget_found/<int:id>', mark_gadget_as_found, name='mark_gadget_as_found'),
]
