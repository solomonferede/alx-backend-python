#!/usr/bin/env python3
"""Models for the messaging app."""

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    """Enumeration for user roles."""
    Guest = 'guest', 'Guest'
    Host = 'host', 'Host'
    Admin = 'admin', 'Admin'


class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser."""
    user_id = models.UUIDField(
        primary_key = True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False, db_index=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.Guest,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    """Model representing a message sent by a user."""
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    conversation = models.ForeignKey(
        'Conversation',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    message_body = models.TextField(blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    """Model representing a conversation between users."""
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    participants = models.ManyToManyField(
        CustomUser,
        related_name='conversations',      
    )
    created_at = models.DateTimeField(auto_now_add=True)
