from django.urls import path
from . import views
urlpatterns = [
    path('',views.adminlogin,name='adminlogin'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('adminlogout',views.adminlogout,name="adminlogout"),
    path('user_management/', views.user_management_view, name='user_management_view'),
    path('edit_user/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('category_list/', views.category_list, name='category_list'),
    path('category_add/', views.add_category, name='add_category'),
    path('category/toggle_listing/<int:category_id>/', views.toggle_category_listing, name='toggle_category_listing'),

]
