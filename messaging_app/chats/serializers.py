#!/usr/bin/env python3
"""
Serializers for the messaging app.
"""
from rest_framework import serializers
from .models import CustomUser, Conversation, Message


class UserSerializer(serializers.Serializer):
    """Serializer for CustomUser model."""
    user_id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    role = serializers.CharField()


class ConversationSerializer(serializers.Serializer):
    """Serializer for Conversation model."""
    conversation_id = serializers.UUIDField(read_only=True)
    participants = UserSerializer(many=True)
    messages = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)

    # Include messages nested manually
    def get_messages(self, obj):
        qs = obj.messages.all()  # Related name from Message model
        return MessageSerializer(qs, many=True).data


class MessageSerializer(serializers.Serializer):
    """Serializer for Message model. """
    message_id = serializers.UUIDField(read_only=True)
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()
    sent_at = serializers.DateTimeField(read_only=True)

    # Validation
    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        return value
