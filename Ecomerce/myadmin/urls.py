from django.urls import path
from . import views
urlpatterns = [
    path('',views.adminlogin,name='adminlogin'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('adminlogout',views.adminlogout,name="adminlogout"),
    path('user_management/', views.user_management_view, name='user_management_view'),
    path('edit_user/<int:user_id>/', views.edit_user_view, name='edit_user'),

]
