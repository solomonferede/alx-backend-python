#!/usr/bin/env python3
"""Views for the messaging app using ViewSet."""

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, CustomUser, Message
from .serializers import ConversationSerializer, MessageSerializer


# -------------------------------
# Conversation ViewSet
# -------------------------------
class ConversationViewSet(viewsets.ViewSet):
    """
    List, retrieve, and create conversations.
    """
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['participants']
    search_fields = ['participants__first_name', 'participants__last_name']

    def list(self, request):
        qs = Conversation.objects.prefetch_related("participants", "messages__sender").all()
        participant_id = request.query_params.get("participant_id")
        if participant_id:
            qs = qs.filter(participants__user_id=participant_id)
        serializer = ConversationSerializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            conversation = Conversation.objects.prefetch_related("participants", "messages__sender").get(conversation_id=pk)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    def create(self, request):
        participant_ids = request.data.get("participant_ids", [])
        if not participant_ids:
            return Response({"error": "Participants are required"}, status=status.HTTP_400_BAD_REQUEST)
        conversation = Conversation.objects.create()
        participants = CustomUser.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(participants)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# -------------------------------
# Message ViewSet
# -------------------------------
class MessageViewSet(viewsets.ViewSet):
    """
    List, retrieve, and send messages.
    Supports nested routes under conversation.
    """
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation_id', 'sender_id']

    def list(self, request, conversation_pk=None):
        qs = Message.objects.select_related("sender", "conversation").all()
        # Use nested router conversation_pk if present
        if conversation_pk:
            qs = qs.filter(conversation_id=conversation_pk)
        else:
            conversation_id = request.query_params.get("conversation_id")
            if conversation_id:
                qs = qs.filter(conversation_id=conversation_id)
        serializer = MessageSerializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, conversation_pk=None):
        try:
            message = Message.objects.select_related("sender", "conversation").get(message_id=pk)
        except Message.DoesNotExist:
            return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def create(self, request, conversation_pk=None):
        conversation_id = conversation_pk or request.data.get("conversation_id")
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

        message = Message.objects.create(conversation_id=conversation, sender_id=sender, message_body=message_body)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
