from django.urls import path
from e_consultant_app_api import views


urlpatterns = [
    path('api/authenticate_econsultant/', views.authenticate_econsultant, name='authenticate_econsultant'), 
    path('api/secure_econsultant_for_messaging/', views.secure_econsultant_for_messaging, name='secure_econsultant_for_messaging'),
    path('api/secure_econsultant_for_storage/', views.secure_econsultant_for_storage, name='secure_econsultant_for_storage'),
    path('api/secure_econsultant_for_telemedics/', views.secure_econsultant_for_telemedics, name='secure_econsultant_for_telemedics'),
    path('api/secure_econsultant_for_reading_messages/', views.secure_econsultant_for_reading_messages, name='secure_econsultant_for_reading_messages'),
    path('api/secure_econsultant_to_upload_to_storage/', views.secure_econsultant_to_upload_to_storage, name='secure_econsultant_to_upload_to_storage'),
    path('api/secure_econsultant_for_downloading_assets/', views.secure_econsultant_for_downloading_assets, name='secure_econsultant_for_downloading_assets'),
    path('api/secure_econsultant_for_deleting_assets/', views.secure_econsultant_for_deleting_assets, name='secure_econsultant_for_deleting_assets'),
    path('api/secure_econsultant_for_subscription_claims/', views.secure_econsultant_for_subscription_claims, name='secure_econsultant_for_subscription_claims'),
    path('api/secure_econsultant_for_phone_number_verification/', views.secure_econsultant_for_phone_number_verification, name='secure_econsultant_for_phone_number_verification'),
    path('api/econsultant_password_reset/', views.econsultant_password_reset, name='users_password_reset'),
    path('api/econsultant_delete_file_from_firestore/', views.econsultant_delete_file_from_firestore, name='econsultant_delete_file_from_firestore'),
    

]