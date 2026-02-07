from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5                     # items per page
    page_size_query_param = 'page_size'  # allow client override
    max_page_size = 50                # safety limit
    page_query_param = 'page'         # default is 'page'

class CustomResponsePagination(PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        return Response({
            'total_records': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next_page': self.get_next_link(),
            'prev_page': self.get_previous_link(),
            'data': data
        })

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'total_records': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data
        })

class AdvancedPageNumberPagination(PageNumberPagination):
    page_size = 10                       # default page size
    page_size_query_param = 'page_size'  # client can override
    max_page_size = 100                  # security limit
    page_query_param = 'page'

    def get_paginated_response(self, data):
        total_records = self.page.paginator.count
        page_size = self.get_page_size(self.request)
        current_page = self.page.number
        total_pages = math.ceil(total_records / page_size)

        return Response({
            "meta": {
                "total_records": total_records,
                "total_pages": total_pages,
                "current_page": current_page,
                "page_size": page_size,
                "next_page": current_page + 1 if self.page.has_next() else None,
                "previous_page": current_page - 1 if self.page.has_previous() else None,
                "first_page": 1,
                "last_page": total_pages,
            },
            "results": data
        })
