from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ProductPagination(PageNumberPagination):
    """Класс пагинации для страницы с товарами"""

    page_size = 8
    page_query_param = "currentPage"
    max_page_size = 16

    def get_paginated_response(self, data) -> Response:
        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": self.page.paginator.num_pages,
            }
        )
