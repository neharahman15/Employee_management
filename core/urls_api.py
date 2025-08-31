from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views_api import DynamicFormViewSet, EmployeeViewSet

router = DefaultRouter()
router.register(r'forms', DynamicFormViewSet, basename='form')
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
