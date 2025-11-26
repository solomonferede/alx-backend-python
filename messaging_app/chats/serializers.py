#!/usr/bin/env python3
"""Serializers for the messaging app."""


from rest_framework import serializers
from .models import CustomUser, Message, Conversation


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model."""

    class Meta:
        model = CustomUser
        fields = [
            'user_id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model."""
    sender = CustomUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']

class conversationSerializer(serializers.ModelSerializer):
    """Serializer for the Conversation model."""

    participants = CustomUserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'created_at',
        ]
        read_only_fields = ['conversation_id', 'created_at']