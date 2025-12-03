from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from .auth import JWTLoginView
from .views import ConversationViewSet, MessageViewSet, StatusViewSet
from rest_framework_simplejwt.views import TokenRefreshView

# Main router
router = routers.DefaultRouter()
router.register('conversations', ConversationViewSet, basename='conversation')
router.register('messages', MessageViewSet, basename='message')
router.register(r'status', StatusViewSet, basename='status')

# Nested routes
nested = NestedDefaultRouter(router, 'conversations', lookup='conversation')
nested.register('messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested.urls)),

    # JWT Authentication
    path('auth/login/', JWTLoginView.as_view(), name='jwt_login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


