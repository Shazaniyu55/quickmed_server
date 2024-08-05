from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users_app_api/', include('users_app_api.urls')),
    path('ambulance/', include('ambulance_app_api.urls')),
    path('e-consultant/', include('e_consultant_app_api.urls')),
    path('hospital/', include('hospital_app_api.urls')),
    path('flutterwave/', include('flutterwave_payment_app_api.urls')),
    path('api/schema', SpectacularAPIView.as_view(), name="schema"),
    path('api/schema/quickmeddocs', SpectacularSwaggerView.as_view(url_name="schema")),
    
]
