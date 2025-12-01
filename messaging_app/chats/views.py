#!/usr/bin/env python3
"""Simplified Views for the messaging app using ViewSet."""

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CustomUser, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOrReadOnly


class ConversationViewSet(viewsets.ViewSet):
    """
    List, retrieve, and create conversations.
    """

    permission_classes = [IsAuthenticated, IsParticipantOrReadOnly]
    # -----------------------
    # GET /conversations/
    # -----------------------
    def list(self, request):
        queryset = Conversation.objects.prefetch_related(
            "participants", "messages__sender"
        ).all()

        participant_id = request.query_params.get("participant_id")
        if participant_id:
            queryset = queryset.filter(participants__user_id=participant_id)

        serializer = ConversationSerializer(queryset, many=True)
        return Response(serializer.data)

    # -----------------------
    # GET /conversations/<id>/
    # -----------------------
    def retrieve(self, request, pk=None):
        try:
            conversation = Conversation.objects.prefetch_related(
                "participants", "messages__sender"
            ).get(conversation_id=pk)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    # -----------------------
    # POST /conversations/
    # -----------------------
    def create(self, request):
        participant_ids = request.data.get("participant_ids")

        if not participant_ids:
            return Response(
                {"error": "participant_ids is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the conversation
        conversation = Conversation.objects.create()

        # Assign participants
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
    Supports nested routes under conversations.
    """

    permission_classes = [IsAuthenticated, IsParticipantOrReadOnly]
    # --------------------------------------
    # GET /messages/  OR  GET /conversations/<pk>/messages/
    # --------------------------------------
    def list(self, request, conversation_pk=None):
        queryset = Message.objects.select_related(
            "sender", "conversation"
        ).all()

        # If using nested routes: /conversations/<id>/messages/
        if conversation_pk:
            queryset = queryset.filter(conversation_id=conversation_pk)
        else:
            # Normal route filter: /messages/?conversation_id=1
            conv_id = request.query_params.get("conversation_id")
            if conv_id:
                queryset = queryset.filter(conversation_id=conv_id)

        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    # --------------------------------------
    # GET /messages/<id>/
    # --------------------------------------
    def retrieve(self, request, pk=None, conversation_pk=None):
        try:
            message = Message.objects.select_related(
                "sender", "conversation"
            ).get(message_id=pk)
        except Message.DoesNotExist:
            return Response(
                {"error": "Message not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MessageSerializer(message)
        return Response(serializer.data)

    # --------------------------------------
    # POST /messages/  OR  POST /conversations/<pk>/messages/
    # --------------------------------------
    def create(self, request, conversation_pk=None):
        conversation_id = conversation_pk or request.data.get("conversation_id")
        sender_id = request.data.get("sender_id")
        message_body = (request.data.get("message_body") or "").strip()

        # Validate required fields
        if not all([conversation_id, sender_id, message_body]):
            return Response(
                {"error": "conversation_id, sender_id, and message_body are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check conversation + sender
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            sender = CustomUser.objects.get(user_id=sender_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Sender not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create and return message
        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
