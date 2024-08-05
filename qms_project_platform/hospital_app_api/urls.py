from django.urls import path
from hospital_app_api import views


urlpatterns = [
    path('api/authenticate_hospital/', views.authenticate_hospital, name='authenticate_hospital'), 
    path('api/secure_hospital_for_messaging/', views.secure_hospital_for_messaging, name='secure_hospital_for_messaging'),
    path('api/secure_hospital_for_storage/', views.secure_hospital_for_storage, name='secure_hospital_for_storage'),
    path('api/secure_hospital_for_telemedics/', views.secure_hospital_for_telemedics, name='secure_hospital_for_telemedics'),
    path('api/secure_hospital_for_reading_messages/', views.secure_hospital_for_reading_messages, name='secure_hospital_for_reading_messages'),
    path('api/secure_hospital_to_upload_to_storage/', views.secure_hospital_to_upload_to_storage, name='secure_hospital_to_upload_to_storage'),
    path('api/secure_hospital_for_downloading_assets/', views.secure_hospital_for_downloading_assets, name='secure_hospital_for_downloading_assets'),
    path('api/secure_hospital_for_deleting_assets/', views.secure_hospital_for_deleting_assets, name='secure_hospital_for_deleting_assets'),
    path('api/secure_hospital_for_subscription_claims/', views.secure_hospital_for_subscription_claims, name='secure_hospital_for_subscription_claims'),
    path('api/secure_hospital_for_phone_number_verification/', views.secure_hospital_for_phone_number_verification, name='secure_hospital_for_phone_number_verification'),
    path('api/hospital_password_reset/', views.hospital_password_reset, name='hospital_password_reset'),
    path('api/hospital_delete_file_from_firestore/', views.hospital_delete_file_from_firestore, name='hospital_delete_file_from_firestore'),
]