from typing import Dict, Set, List, Tuple, Type, Callable, Any, Awaitable
from unittest import TestCase
from typish._functions import get_type
from typish._types import NoneType, Unknown


class TestGetType(TestCase):
    def test_get_type_list(self):
        self.assertEqual(List[int], get_type([1, 2, 3]))
        self.assertEqual(List[object], get_type([1, 2, '3']))
        self.assertEqual(List[Unknown], get_type([]))

    def test_get_type_set(self):
        self.assertEqual(Set[int], get_type({1, 2, 3}))
        self.assertEqual(Set[object], get_type({1, 2, '3'}))
        self.assertEqual(Set[Unknown], get_type(set([])))

    def test_get_type_dict(self):
        self.assertEqual(Dict[str, int], get_type({'a': 1, 'b': 2}))
        self.assertEqual(Dict[int, object], get_type({1: 'a', 2: 2}))
        self.assertEqual(Dict[Unknown, Unknown], get_type({}))

    def test_get_type_tuple(self):
        self.assertEqual(Tuple[int, int, int], get_type((1, 2, 3)))
        self.assertEqual(Tuple[int, str, str], get_type((1, '2', '3')))

    def test_get_type_callable(self):

        def func1(x: int, y: str) -> object:
            pass

        def func2() -> int:
            pass

        def func3(x: int):
            pass

        def func4():
            pass

        def func5(x):
            pass

        def func6(l: List[List[List[int]]]):
            pass

        self.assertEqual(Callable[[int, str], object], get_type((func1)))
        self.assertEqual(Callable[[], int], get_type(func2))
        self.assertEqual(Callable[[int], NoneType], get_type(func3))
        self.assertEqual(Callable, get_type(func4))
        self.assertEqual(Callable[[Any], NoneType], get_type(func5))
        self.assertEqual(Callable[[List[List[List[int]]]], NoneType], get_type(func6))

    def test_get_type_async(self):

        async def func(x: int) -> str:
            return '42'

        self.assertEqual(Callable[[int], Awaitable[str]], get_type(func))

    def test_get_type_lambda(self):
        self.assertEqual(Callable[[Unknown, Unknown], Unknown], get_type(lambda x, y: 42))
        self.assertEqual(Callable[[], Unknown], get_type(lambda: 42))

    def test_get_type_deep(self):
        self.assertEqual(List[List[int]], get_type([[1, 2], [3]]))
        self.assertEqual(List[List[object]], get_type([[1, 2], ['3']]))

        deep = [[[1, 2]], [[3]], [[4], [5, '6']]]

        self.assertEqual(List[List[List[object]]], get_type(deep))
        self.assertEqual(Dict[str, List[List[List[object]]]], get_type({'a': deep}))

    def test_get_type_type(self):
        self.assertEqual(Type[int], get_type(int))

    def test_get_type_some_class(self):
        class SomeRandomClass:
            pass

        self.assertEqual(SomeRandomClass, get_type(SomeRandomClass()))
