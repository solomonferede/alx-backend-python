from rest_framework import serializers
from .models import CustomUser, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ["user_id", "first_name", "last_name", "email", "role"]

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        return value

    class Meta:
        model = Message
        fields = ["message_id", "sender", "message_body", "sent_at"]

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all(), many=True).data

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "messages", "created_at"]
