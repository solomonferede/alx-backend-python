#!/usr/bin/env python3
"""Messaging app ViewSets with full CRUD and permissions."""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


# ===========================================================
# Conversation ViewSet
# ===========================================================
class ConversationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Apply IsParticipantOfConversation for object-level access.
        """
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsParticipantOfConversation()]
        return [IsAuthenticated()]

    # -----------------------
    # GET /conversations/
    # -----------------------
    def list(self, request):
        user = request.user
        queryset = Conversation.objects.prefetch_related(
            "participants", "messages__sender"
        ).filter(participants=user)  # only conversations where user is a participant

        participant_id = request.query_params.get("participant_id")
        if participant_id:
            queryset = queryset.filter(participants__user_id=participant_id)

        serializer = ConversationSerializer(queryset, many=True)
        return Response(serializer.data)


    # -----------------------
    # GET /conversations/<id>/
    # -----------------------
    def retrieve(self, request, pk=None):
        conversation = self.get_object(pk)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    # -----------------------
    # POST /conversations/
    # -----------------------
    def create(self, request):
        participant_ids = request.data.get("participant_ids")
        if not participant_ids:
            raise ValidationError({"participant_ids": "This field is required."})

        conversation = Conversation.objects.create()
        participants = CustomUser.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(participants)

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # -----------------------
    # PUT / PATCH /conversations/<id>/
    # -----------------------
    def update(self, request, pk=None):
        conversation = self.get_object(pk)
        participant_ids = request.data.get("participant_ids")

        if participant_ids:
            participants = CustomUser.objects.filter(user_id__in=participant_ids)
            conversation.participants.set(participants)

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    # -----------------------
    # DELETE /conversations/<id>/
    # -----------------------
    def destroy(self, request, pk=None):
        conversation = self.get_object(pk)
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # -----------------------
    # Helper
    # -----------------------
    def get_object(self, pk):
        try:
            conversation = Conversation.objects.prefetch_related(
                "participants", "messages__sender"
            ).get(conversation_id=pk)
        except Conversation.DoesNotExist:
            raise NotFound("Conversation not found.")

        # Trigger object-level permission check
        for perm in self.get_permissions():
            if hasattr(perm, "has_object_permission"):
                if not perm.has_object_permission(self.request, self, conversation):
                    raise ValidationError("You do not have permission to access this conversation.")

        return conversation


# ===========================================================
# Message ViewSet
# ===========================================================
class MessageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "retrieve", "update", "partial_update", "destroy", "create"]:
            return [IsAuthenticated(), IsParticipantOfConversation()]
        return [IsAuthenticated()]

    # -----------------------
    # GET /messages/ OR /conversations/<pk>/messages/
    # -----------------------
    def list(self, request, conversation_pk=None):
        user = request.user

        # Filter messages only for conversations where user is a participant
        queryset = Message.objects.filter(conversation__participants=user)

        if conversation_pk:
            queryset = queryset.filter(conversation_id=conversation_pk)

        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)


    # -----------------------
    # GET /messages/<id>/
    # -----------------------
    def retrieve(self, request, pk=None, conversation_pk=None):
        message = self.get_object(pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    # -----------------------
    # POST /messages/ OR /conversations/<pk>/messages/
    # -----------------------
    def create(self, request, conversation_pk=None):
        conversation_id = conversation_pk or request.data.get("conversation_id")
        sender_id = request.data.get("sender_id")
        message_body = (request.data.get("message_body") or "").strip()

        if not all([conversation_id, sender_id, message_body]):
            raise ValidationError("conversation_id, sender_id, and message_body are required.")

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise NotFound("Conversation not found.")

        try:
            sender = CustomUser.objects.get(user_id=sender_id)
        except CustomUser.DoesNotExist:
            raise NotFound("Sender not found.")

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # -----------------------
    # PUT / PATCH /messages/<id>/
    # -----------------------
    def update(self, request, pk=None, conversation_pk=None):
        message = self.get_object(pk)
        message_body = (request.data.get("message_body") or "").strip()
        if message_body:
            message.message_body = message_body
            message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def partial_update(self, request, pk=None, conversation_pk=None):
        return self.update(request, pk, conversation_pk)

    # -----------------------
    # DELETE /messages/<id>/
    # -----------------------
    def destroy(self, request, pk=None, conversation_pk=None):
        message = self.get_object(pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # -----------------------
    # Helper
    # -----------------------
    def get_object(self, pk):
        try:
            message = Message.objects.select_related("sender", "conversation").get(message_id=pk)
        except Message.DoesNotExist:
            raise NotFound("Message not found.")

        # Object-level permission
        for perm in self.get_permissions():
            if hasattr(perm, "has_object_permission"):
                if not perm.has_object_permission(self.request, self, message):
                    return Response(
                    {"detail": "You do not have permission to access this message."},
                    status=status.HTTP_403_FORBIDDEN
                )

        return message
