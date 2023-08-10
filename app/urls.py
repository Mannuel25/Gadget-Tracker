from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('login/', login_user, name='login'),
    path('signup/', signup_user, name='signup'),
    path('students/', all_students, name='all_students'),
    path('staff/', all_staff, name='all_staff'),
    path('vendors/', all_vendors, name='all_vendors'),
    # path('users/edit/<int:id>', edit_user, name='edit_user'),
    # path('users/add', AddUsers.as_view(), name='add_user'),
    # path('users/edit/<int:id>', UpdateUsers.as_view(), name='edit_user'),
    path('users/delete/<int:id>', delete_user, name='delete_user'),
    path('gadgets/delete/<int:id>/', delete_gadget, name='delete_gadget'),
    path('logout/', logout_user, name='logout'),

    path('products/', all_users_gadgets, name='all_users_gadgets'),
    path('create/', UserGadgetsCreate.as_view(), name='create_product'),
    path('update/<int:pk>/', UserGadgetsUpdate.as_view(), name='update_product'),
    path('delete-variant/<int:pk>/', delete_variant, name='delete_variant'),
]
