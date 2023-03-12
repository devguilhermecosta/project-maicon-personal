import math

from django.http import HttpRequest
from django.core.paginator import Paginator


def make_pagination_range(range: list,
                          current_page: int,
                          range_per_page: int = 4) -> dict:

    middle_page: int = math.ceil(range_per_page / 2)
    start_range: int = current_page - middle_page
    stop_range: int = current_page + middle_page
    total_pages: int = len(range)

    start_range_offset: int = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(stop_range - total_pages)

    if len(range) <= range_per_page:
        start_range = 0
        stop_range = len(range)

    return {
        'pagination': range[start_range:stop_range],
        'total_pages': total_pages,
        'range_per_page': range_per_page,
        'current_page': current_page,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_page and len(range) > range_per_page,  # noqa: E501
        'last_page_out_of_range': stop_range < total_pages,
    }


def make_pagination(request: HttpRequest,
                    query_set: list[object],
                    objects_per_page: str | int,
                    range_per_page: int = 4,
                    ) -> Paginator:

    if not isinstance(objects_per_page, int):
        objects_per_page = int(objects_per_page)

    paginator: Paginator = Paginator(query_set,
                                     objects_per_page,
                                     )

    try:
        current_page: int = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    page_object: Paginator = paginator.get_page(current_page)
    paginator_range: dict = make_pagination_range(paginator.page_range,
                                                  current_page,
                                                  range_per_page
                                                  )
    return page_object, paginator_range
