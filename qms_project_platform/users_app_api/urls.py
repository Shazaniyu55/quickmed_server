from django.urls import path
from users_app_api import views


urlpatterns = [
    path('api/authenticate_users/', views.authenticate_users, name='authenticate_users'), 
    path('api/secure_users_for_messaging/', views.secure_users_for_messaging, name='secure_users_for_messaging'),
    path('api/secure_users_for_storage/', views.secure_users_for_storage, name='secure_users_for_storage'),
    path('api/secure_users_for_telemedics/', views.secure_users_for_telemedics, name='secure_users_for_telemedics'),
    path('api/secure_users_for_reading_messages/', views.secure_users_for_reading_messages, name='secure_users_for_reading_messages'),
    path('api/secure_users_to_upload_to_storage/', views.secure_users_to_upload_to_storage, name='secure_users_to_upload_to_storage'),
    path('api/secure_users_for_downloading_assets/', views.secure_users_for_downloading_assets, name='secure_users_for_downloading_assets'),
    path('api/secure_users_for_deleting_assets/', views.secure_users_for_deleting_assets, name='secure_users_for_deleting_assets'),
    path('api/secure_users_for_subscription_claims/', views.secure_users_for_subscription_claims, name='secure_users_for_subscription_claims'),
    path('api/secure_users_for_phone_number_verification/', views.secure_users_for_phone_number_verification, name='secure_users_for_phone_number_verification'),
    path('api/users_password_reset/', views.users_password_reset, name='users_password_reset'),
    path('api/users_delete_file_from_firestore/', views.users_delete_file_from_firestore, name='users_delete_file_from_firestore'),
    path('api/secure_users_for_logout/', views.secure_users_for_logout, name='secure_users_for_logout'), 
]

