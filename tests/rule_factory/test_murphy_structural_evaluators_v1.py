from src.rule_factory.murphy_structural_evaluators_v1 import *


def test_0013_symmetrical_triangle():
    assert evaluate_0013({"slope":-1,"intercept":10},{"slope":1,"intercept":0})["status"] == "CONFIRMED"


def test_0014_ascending_triangle():
    assert evaluate_0014({"slope":0,"intercept":10},{"slope":1,"intercept":0})["status"] == "CONFIRMED"


def test_0018_falling_wedge():
    assert evaluate_0018({"slope":-2,"intercept":10},{"slope":-1,"intercept":0})["status"] == "CONFIRMED"


def test_0019_rising_wedge():
    assert evaluate_0019({"slope":2,"intercept":0},{"slope":1,"intercept":10})["status"] == "CONFIRMED"


def test_0020_rectangle():
    assert evaluate_0020({"slope":0,"intercept":10},{"slope":0,"intercept":5})["status"] == "CONFIRMED"


def test_missing_geometry_is_not_evaluable():
    assert evaluate_0013({}, {"slope":1,"intercept":0})["status"] == "NOT_EVALUABLE"
