from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = "page_size"    # optional
    max_page_size = 100
