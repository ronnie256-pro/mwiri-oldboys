
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('my-account/', views.MyAccountView.as_view(), name='my_account'),
    path('admin-page/', views.AdminView.as_view(), name='admin_page'),
    path('admin/', views.admin_redirect_view, name='admin_redirect'),
]
