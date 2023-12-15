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
    path('product/toggle_listing/<int:category_id>/', views.toggle_product_listing, name='toggle_product_listing'),
    path('product_list/', views.product_list, name='product_list'),
    path('add_product/', views.add_product, name='add_product'),

    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),

]
