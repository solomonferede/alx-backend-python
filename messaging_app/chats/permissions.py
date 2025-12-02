from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only authenticated users can access the API.
    Only participants can view or modify conversations/messages.
    """

    def has_permission(self, request, view):
        # Authenticated users only
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # For conversations
        if hasattr(obj, "participants"):
            is_participant = user in obj.participants.all()
        # For messages
        elif hasattr(obj, "conversation"):
            is_participant = user in obj.conversation.participants.all()
        else:
            is_participant = False

        # Allow read-only for participants
        if request.method in permissions.SAFE_METHODS:
            return is_participant

        # Allow write methods (POST, PUT, PATCH, DELETE) only for participants
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return is_participant

        # Deny everything else
        return False

    @staticmethod
    def filter_queryset_for_user(queryset, user):
        return queryset.filter(participants=user)
