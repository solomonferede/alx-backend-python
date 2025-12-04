import django_filters
from django.utils import timezone
from .models import Message, Conversation


# -------------------------------------
# Filter Messages
# -------------------------------------
class MessageFilter(django_filters.FilterSet):
    # filter messages sent by a specific user
    sender_id = django_filters.CharFilter(field_name="sender__user_id", lookup_expr="exact")

    # filter messages in a specific conversation
    conversation_id = django_filters.CharFilter(field_name="conversation__conversation_id", lookup_expr="exact")

    # date range filters
    start_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["sender_id", "conversation_id", "start_date", "end_date"]


# -------------------------------------
# Filter Conversations
# -------------------------------------
class ConversationFilter(django_filters.FilterSet):
    # get conversations that include a specific user
    participant_id = django_filters.CharFilter(field_name="participants__user_id", lookup_expr="exact")

    class Meta:
        model = Conversation
        fields = ["participant_id"]
