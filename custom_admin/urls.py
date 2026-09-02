from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_home, name="admin_dashboard_home"),
    path("login/", views.admin_login, name="admin_dashboard_login"),
    path("logout/", views.admin_logout, name="admin_dashboard_logout"),
    path("members/", views.manage_members, name="admin_members"),
    path("members/verify/<int:user_id>/", views.toggle_user_verification, name="admin_verify_user"),
    path("products/", views.manage_products, name="admin_products"),
    path("products/delete/<int:product_id>/", views.delete_product, name="admin_delete_product"),
    path("content/", views.manage_content, name="admin_content"),
    path("elections/", views.manage_elections, name="admin_elections"),
    path("elections/candidate/<int:candidate_id>/<str:action>/", views.toggle_candidate_status, name="admin_candidate_action"),
    path("payments/", views.manage_payments, name="admin_payments"),
    path("settings/", views.manage_settings, name="admin_settings"),
]
