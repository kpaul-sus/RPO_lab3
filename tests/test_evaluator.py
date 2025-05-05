import pytest

from calculator.parser import Number, BinaryOp, parse

from calculator.evaluator import evaluate

@pytest.mark.parametrize("expr, result", [
    (BinaryOp(Number(1), '+', Number(2)), 3),
    (BinaryOp(Number(4), '-', Number(2)), 2),
    (BinaryOp(Number(3), '*', Number(5)), 15),
    (BinaryOp(Number(10), '/', Number(2)), 5),
])
def test_simple_evaluations(expr, result):
    assert evaluate(expr) == result

def test_nested_expression():
    expr = BinaryOp(Number(2), '+', BinaryOp(Number(3), '*', Number(4)))  
    assert evaluate(expr) == 14

def test_division_by_zero():
    expr = BinaryOp(Number(1), '/', Number(0))
    with pytest.raises(ZeroDivisionError):
        evaluate(expr)

def test_large_division():
    expr = BinaryOp(Number(1e300), '/', Number(1e-300))
    with pytest.raises(OverflowError):
        evaluate(expr)

def test_unknown_operator():
    expr = BinaryOp(Number(1), '%', Number(2))  
    with pytest.raises(ValueError):
        evaluate(expr)

def test_basic_math():
    assert evaluate(parse("1 + 1")) == 2
    assert evaluate(parse("2 * 3")) == 6

def test_exponent():
    assert evaluate(parse("2^3")) == 8

def test_scientific():
    assert evaluate(parse("1.25e2")) == 125.0

def test_parentheses():
    result = evaluate(parse("1 + 2 / (3 + 4)"))
    assert abs(result - 1.2857142857142856) < 1e-10

def test_floating_point_sum():
    result = evaluate(parse("0.1 + 0.2"))
    assert abs(result - 0.3) < 1e-9  

def test_near_zero_division():
    expr = "1 / 1e-300"
    result = evaluate(parse(expr))
    assert result > 1e+299

def test_negative_exponent():
    assert evaluate(parse("4^-2")) == 0.0625

