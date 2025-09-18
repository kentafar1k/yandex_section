from main import A, Calculator
import pytest



class TestCalculator:
    @pytest.mark.parametrize('x, y', [(0, 1), (1, 0)])
    def test_1(self, x, y):
        assert Calculator().divide(x, y) == 0

    def test_main(self):
        assert 1 == 1

    def test_main2(self):
        a = A()

        assert a.x == 1
