from django.contrib.auth import views as auth_views
from django.urls import path

from currency.views import CustomPasswordResetView
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', auth_views.LoginView.as_view(), {'redirect_authenticated_user': True }, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('user/', views.UserListView.as_view(), name='users_list'),
    path('user/<pk>/edit/', views.PasswordUpdateView.as_view(), name='edit_user'),
    path('user/edit/', views.edit_profile, name='edit_user_profile'),
    path('user/edit/password/', views.profile_password, name='profile_password'),

    path('register/<pk>/', views.preregister, name='preregister'),
    path('register/success/', views.preregister_success, name='preregister_success'),

    path('map/', views.entity_map, name='map'),
    path('entity/', views.user_entity, name='user_entity'),
    path('entity/add', views.add_entity, name='add_entity'),
    path('qr/<pk>/', views.entity_detail, name='entity_qr_detail'),
    path('entity/<pk>/', views.entity_detail, name='entity_detail'),
    path('entity/<pk>/edit/', views.entity_edit, name='entity_edit'),
    #path('entities/', views.entity_list, name='entity_list'),
    path('entities/', views.EntityListView.as_view(), name='entity_list'),

    path('profile/', views.user_profile, name='user_profile'),
    path('member/card/', views.member_card, name='member_card'),
    path('member/card_pdf/', views.member_card_pdf, name='member_card_pdf'),
    path('socia/', views.member_check, name='memeber_check'),
    path('profile/admin/', views.ProfileListView.as_view(), name='profile_list'),

    path('profile/<pk>/', views.profile_detail, name='profile_detail'),
    path('profile/<pk>/edit/', views.profile_edit, name='profile_edit'),
    path('users/search/', views.search_users, name='search_users'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/add', views.add_category, name='add_category'),
    path('categories/<pk>/edit/', views.category_edit, name='category_edit'),

    path('dashboard/', views.profile, name='dashboard'),
]