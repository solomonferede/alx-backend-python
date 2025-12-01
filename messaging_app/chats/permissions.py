from rest_framework import permissions, BasePermission


class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Users can access conversations and messages only if they are a participant.
    - Read-only requests are allowed only for participants.
    - Write (POST) is allowed only for participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # Safe methods: GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return self._is_participant(request, obj)

        # For writes (POST), ensure the user is a participant
        return self._is_participant(request, obj)

    def _is_participant(self, request, obj):
        """
        Returns True if the authenticated user is part of the conversation
        or sender of the message.
        """
        user = request.user

        # For Conversation objects
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        # For Message objects
        if hasattr(obj, "conversation"):
            return user in obj.conversation.participants.all() or obj.sender == user

        return False
