from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API.
    - Only participants of a conversation can view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - Conversations: user must be a participant
        - Messages: user must belong to the message's conversation
        """
        user = request.user

        # Case 1: Conversation object
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        # Case 2: Message object
        if hasattr(obj, "conversation"):
            conversation = obj.conversation
            return user in conversation.participants.all()

        return False

    @staticmethod
    def filter_queryset_for_user(queryset, user):
        """
        Filter a queryset to only include objects where the user is a participant.
        """
        return queryset.filter(participants=user)


