from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

# page_size = 10


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('page_count', self.page.paginator.num_pages)
        ]))
