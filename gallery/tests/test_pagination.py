import math

from django.test import SimpleTestCase


def make_pagination_range(range: list,
                          current_page: int,
                          range_per_page: int = 4) -> dict:

    middle_page: int = math.ceil(range_per_page / 2)
    start_range: int = current_page - middle_page
    stop_range: int = current_page + middle_page
    total_pages: int = len(range)  # 2

    start_range_offset: int = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(stop_range - total_pages)

    return {
        'pagination_range': range[start_range:stop_range],
        'total_pages': total_pages,
        'range_per_page': range_per_page,
        'current_page': current_page,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_page,
        'last_page_out_of_range': stop_range < total_pages,
    }


class PaginationTest(SimpleTestCase):
    def setUp(self) -> None:
        self.range: list = list(range(1, 21))
        return super().setUp()

    def test_pagination_range_return_a_range(self) -> None:
        pagination = make_pagination_range(self.range,
                                           1,
                                           )

        self.assertEqual([1, 2, 3, 4], pagination.get('pagination_range'))

    def test_pagination_range_is_static_if_current_page_is_less_than_middle_page(self) -> None:  # noqa: E501
        pagintion_1: dict = make_pagination_range(self.range,
                                                  1,
                                                  4)
        self.assertEqual([1, 2, 3, 4], pagintion_1.get('pagination_range'))

        pagination_2: dict = make_pagination_range(self.range,
                                                   2,
                                                   4)
        self.assertEqual([1, 2, 3, 4], pagination_2.get('pagination_range'))

        pagination_3: dict = make_pagination_range(self.range,
                                                   3,
                                                   4)
        self.assertEqual([2, 3, 4, 5], pagination_3.get('pagination_range'))

        pagination_4: dict = make_pagination_range(self.range,
                                                   4,
                                                   4)

        self.assertEqual([3, 4, 5, 6], pagination_4.get('pagination_range'))

    def test_pagination_range_shoud_be_static_at_end_of_range(self) -> None:
        pagination_1: dict = make_pagination_range(self.range,
                                                   18)
        self.assertEqual([17, 18, 19, 20],
                         pagination_1.get('pagination_range')
                         )

        pagination_2: dict = make_pagination_range(self.range,
                                                   19)
        self.assertEqual([17, 18, 19, 20],
                         pagination_2.get('pagination_range')
                         )

        pagination_3: dict = make_pagination_range(self.range,
                                                   20)

        self.assertEqual([17, 18, 19, 20],
                         pagination_3.get('pagination_range')
                         )

    def test_pagination_is_correct_if_range_is_less_than_range_per_page(self) -> None:  # noqa: E501
        pagination_1: dict = make_pagination_range(list(range(1, 3)),
                                                   2)

        self.assertEqual([1, 2], pagination_1.get('pagination_range'))

        pagination_2: dict = make_pagination_range(list(range(1, 2)),
                                                   2)

        self.assertEqual([1], pagination_2.get('pagination_range'))
