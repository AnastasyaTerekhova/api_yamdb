from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import SignupView, TokenView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/', include(router.urls)),
]
