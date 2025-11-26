#!/usr/bin/env python3
"""Views for the messaging app."""

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, CustomUser, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ViewSet):
    """
    API endpoint for listing conversations and creating new ones.
    """

    # GET /conversations/
    def list(self, request):
        conversations = Conversation.objects.prefetch_related("participants", "messages__sender").all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    # GET /conversations/{id}/
    def retrieve(self, request, pk=None):
        try:
            conversation = Conversation.objects.prefetch_related("participants", "messages__sender").get(conversation_id=pk)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    # POST /conversations/
    def create(self, request):
        participant_ids = request.data.get("participant_ids", [])
        if not participant_ids:
            return Response({"error": "Participants are required"}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        participants = CustomUser.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(participants)
        conversation.save()

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ViewSet):
    """
    API endpoint for listing messages and sending a new message.
    """

    # GET /messages/?conversation_id=...
    def list(self, request):
        conversation_id = request.query_params.get("conversation_id")
        if not conversation_id:
            return Response({"error": "conversation_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        messages = Message.objects.filter(conversation_id=conversation_id).select_related("sender").all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            message = Message.objects.select_related("sender_id", "conversation_id").get(message_id=pk)
        except Message.DoesNotExist:
            return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(message)
        return Response(serializer.data)


    # POST /messages/
    def create(self, request):
        conversation_id = request.data.get("conversation_id")
        sender_id = request.data.get("sender_id")
        message_body = request.data.get("message_body", "").strip()

        if not all([conversation_id, sender_id, message_body]):
            return Response({"error": "conversation_id, sender_id, and message_body are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            sender = CustomUser.objects.get(user_id=sender_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({"error": "Sender not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create Message
        message = Message.objects.create(
            conversation_id=conversation,
            sender_id=sender,
            message_body=message_body
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

