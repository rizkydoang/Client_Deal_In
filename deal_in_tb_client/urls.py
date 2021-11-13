from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # App
    path('', views.Index, name='home'),
    path('store/index/<slug:id_store>/', views.IndexStore, name='home_store'),
    path('store/add_item/', views.AddItem, name='add_item_store'),
    path('store/search/', views.Search, name='search_item_store'),


    # Authentification App
    path('login/', views.LoginUser, name='login_user'),
    path('logout/', views.Logout, name='logout_user'),
    path('signup/', views.SignUpUser, name='signup_user'),
    path('signup_store/', views.SignUpStore, name='signup_store'),
    path('pin_store/', views.SignUpStoreAuth, name='pin_store_auth'),

    path('checkout/', views.CheckOut, name='check_out'),

]
