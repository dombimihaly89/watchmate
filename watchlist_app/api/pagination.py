from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class ReviewPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 3
    last_page_strings = 'end'
    
class ReviewLOPagination(LimitOffsetPagination):
    default_limit = 1
    limit_query_param = 'limit'
    offset_query_param = 'skip'
    
class ReviewCursorPagination(CursorPagination):
    page_size = 2
    ordering = 'created'