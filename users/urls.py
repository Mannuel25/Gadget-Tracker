from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', login_user, name='login'),
    path('signup/', signup_user, name='signup'),
    path('users/add', add_user, name='add_user'),
    path('students/', all_students, name='all_students'),
    path('staff/', all_staff, name='all_staff'),
    path('vendors/', all_vendors, name='all_vendors'),
    path('users/edit/<int:id>', edit_user, name='edit_user'),
    path('users/delete/<int:id>', delete_user, name='delete_user'),
    path('logout/', logout_user, name='logout')
]
