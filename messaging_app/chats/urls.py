#!/usr/bin/env python3
""" URLs for the messaging app chats."""
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet
from rest_framework import routers

# Create a router and register the  viewsets
router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")

# Include the router URLs
urlpatterns = [
    path("", include(router.urls)),
]
