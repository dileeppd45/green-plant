from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name="login"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('admin_home', views.admin_home, name='admin_home'),
    path('view_all_plant', views.view_all_plant, name='view_all_plant'),
    path('register_category_link', views.register_category_link, name='register_category_link'),
    path('register_category', views.register_category, name='register_category'),
    path('view_all_category', views.view_all_category, name='view_all_category'),
    path('edit_category_link/<int:id>', views.edit_category_link, name='edit_category_link'),
    path('update_category', views.update_category, name='update_category'),
    path('register_item/<int:id>', views.register_item, name='register_item'),
    path('register_item/plant_add', views.plant_add, name='plant_add'),
    path('delete_category/<int:id>', views.delete_category, name='delete_category'),
    path('admin_pending_feedback', views.admin_pending_feedback, name='admin_pending_feedback'),
    path('reply_fb/<int:id>', views.reply_fb, name='reply_fb'),
    path('reply_submit', views.reply_submit, name='reply_submit'),
    path('admin_replied_feedback', views.admin_replied_feedback, name='admin_replied_feedback'),
    path('edit_reply_fb/<int:id>', views.edit_reply_fb, name='edit_reply_fb'),
    path('edit_reply_submit', views.edit_reply_submit, name='edit_reply_submit'),
    path('admin_nltk_feedback', views.admin_nltk_feedback, name='admin_nltk_feedback'),

    path('view_orders/<int:id>', views.view_orders, name='view_orders'),
    path('view_approved_orders/<int:id>', views.view_approved_orders, name='view_approved_orders'),
    path('approve_order/<int:id>', views.approve_order, name='approve_order'),
    path('approved_carts', views.approved_carts, name='approved_carts'),
    path('all_carts', views.all_carts, name="all_carts"),
    path('signup', views.signup, name='signup'),
    path('user_register_link', views.user_register_link, name='user_register_link'),
    path('user_register', views.user_register, name='user_register'),
    path('user_home', views.user_home, name='user_home'),
    path('view_cat', views.view_cat, name='view_cat'),
    path('view_items/<int:id>', views.view_items, name='view_items'),
    path('add_cart/<int:itemid>', views.addcart, name='add_cart'),
    path('delete_cart_item/<int:id>', views.delete_cart_item, name='delete_cart_item'),
    path('edit_cart_item/<int:id>', views.edit_cart_item, name='edit_cart_item'),
    path('update_cart', views.update_cart_item, name="update_cart"),
    path('register_category_link', views.register_category_link, name='register_category_link'),
    path('register_category', views.register_category, name='register_category'),
    path('delete_plant/<int:id>', views.delete_plant, name='delete_plant'),
    path('update_plant', views.update_plant, name='update_plant'),
    path('edit_plant_link/<int:id>', views.edit_plant_link, name='edit_plant_link'),

    path('view_cart', views.view_cart, name='view_cart'),
    path('database', views.database, name='database'),
    path('pay_card_gateway/<int:id>', views.pay_card_gateway, name='pay_card_gateway'),
    path('card_verify', views.card_verify, name='card_verify'),
    path('feedback', views.feedback, name='feedback'),
    path('sendfb', views.sendfb, name='sendfb'),
    path('view_fb', views.view_fb, name='view_fb'),


    path('my_orders', views.my_orders, name='my_orders'),
    path('user_approved_orders/<int:id>', views.user_approved_orders, name='user_approved_orders'),
]
