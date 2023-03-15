from django.test import SimpleTestCase
from ..pagination import make_pagination_range


class PaginationTest(SimpleTestCase):
    def setUp(self) -> None:
        self.range: list = list(range(1, 21))
        return super().setUp()

    def test_pagination_range_return_a_range(self) -> None:
        pagination = make_pagination_range(self.range,
                                           1,
                                           )

        self.assertEqual([1, 2, 3, 4], pagination.get('pagination'))

    def test_pagination_range_is_static_if_current_page_is_less_than_middle_page(self) -> None:  # noqa: E501
        pagintion_1: dict = make_pagination_range(self.range,
                                                  1,
                                                  4)
        self.assertEqual([1, 2, 3, 4], pagintion_1.get('pagination'))

        pagination_2: dict = make_pagination_range(self.range,
                                                   2,
                                                   4)
        self.assertEqual([1, 2, 3, 4], pagination_2.get('pagination'))

        pagination_3: dict = make_pagination_range(self.range,
                                                   3,
                                                   4)
        self.assertEqual([2, 3, 4, 5], pagination_3.get('pagination'))

        pagination_4: dict = make_pagination_range(self.range,
                                                   4,
                                                   4)

        self.assertEqual([3, 4, 5, 6], pagination_4.get('pagination'))

    def test_pagination_range_shoud_be_static_at_end_of_range(self) -> None:
        pagination_1: dict = make_pagination_range(self.range,
                                                   18)
        self.assertEqual([17, 18, 19, 20],
                         pagination_1.get('pagination')
                         )

        pagination_2: dict = make_pagination_range(self.range,
                                                   19)
        self.assertEqual([17, 18, 19, 20],
                         pagination_2.get('pagination')
                         )

        pagination_3: dict = make_pagination_range(self.range,
                                                   20)

        self.assertEqual([17, 18, 19, 20],
                         pagination_3.get('pagination')
                         )

    def test_pagination_is_correct_if_range_is_less_than_range_per_page(self) -> None:  # noqa: E501
        pagination_1: dict = make_pagination_range(list(range(1, 3)),
                                                   2,
                                                   )

        self.assertEqual([1, 2], pagination_1.get('pagination'))

        pagination_2: dict = make_pagination_range(list(range(1, 2)),
                                                   2)

        self.assertEqual([1], pagination_2.get('pagination'))
