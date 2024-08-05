from django.urls import path
from ambulance_app_api import views


urlpatterns = [
    path('api/authenticate_ambulance/', views.authenticate_ambulance, name='authenticate_ambulance'), 
    path('api/secure_ambulance_for_messaging/', views.secure_ambulance_for_messaging, name='secure_ambulance_for_messaging'),
    path('api/secure_ambulance_for_storage/', views.secure_ambulance_for_storage, name='secure_ambulance_for_storage'),
    path('api/secure_ambulance_for_telemedics/', views.secure_ambulance_for_telemedics, name='secure_ambulance_for_telemedics'),
    path('api/secure_ambulance_for_reading_messages/', views.secure_ambulance_for_reading_messages, name='secure_ambulance_for_reading_messages'),
    path('api/secure_ambulance_to_upload_to_storage/', views.secure_ambulance_to_upload_to_storage, name='secure_ambulance_to_upload_to_storage'),
    path('api/secure_ambulance_for_downloading_assets/', views.secure_ambulance_for_downloading_assets, name='secure_ambulance_for_downloading_assets'),
    path('api/secure_ambulance_for_deleting_assets/', views.secure_ambulance_for_deleting_assets, name='secure_ambulance_for_deleting_assets'),
    path('api/secure_ambulance_for_subscription_claims/', views.secure_ambulance_for_subscription_claims, name='secure_ambulance_for_subscription_claims'),
    path('api/secure_ambulance_for_phone_number_verification/', views.secure_ambulance_for_phone_number_verification, name='secure_ambulance_for_phone_number_verification'),
    path('api/ambulance_password_reset/', views.ambulance_password_reset, name='ambulance_password_reset'),
    path('api/ambulance_delete_file_from_firestore/', views.ambulance_delete_file_from_firestore, name='ambulance_delete_file_from_firestore'),
    

]