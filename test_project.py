from project import calc_agi, calc_OASDI, calc_medicare, validate_cash_input, calc_federal, calc_effective_tax_rate_percent
from project import STANDARD_DEDUCTION_2023_SINGLE, OASDI_2023_SINGLE,MEDICARE_2023_SINGLE,TAX_BRACKETS_2023_SINGLE

def test_calc_agi():
    assert calc_agi(100000,20000,3000,STANDARD_DEDUCTION_2023_SINGLE) == 63150

def test_calc_OASDI():
    assert calc_OASDI(100000, OASDI_2023_SINGLE) == 6200
# def test_calc_OASDI_max():
    assert calc_OASDI(200000,OASDI_2023_SINGLE) == 9932


def test_calc_medicare():
    assert calc_medicare(100000, MEDICARE_2023_SINGLE) == 2900
# def test_calc_medicare_additional():
    assert calc_medicare(300000, MEDICARE_2023_SINGLE) == 9600

def test_validate_cash_input():
    assert validate_cash_input("1") == (True, 1)
# def test_validate_cash_input_typeerror():
    assert validate_cash_input("cat") == (False, 0)
    assert validate_cash_input("$100") == (False, 0)
# def test_validate_cash_input_negative():
    assert validate_cash_input("-100") == (False, 0)

def test_calc_federal():
# def test_calc_federal_bracket1():
    assert calc_federal(10000,TAX_BRACKETS_2023_SINGLE) == 1000
# def test_calc_federal_bracket2():
    assert calc_federal(40000,TAX_BRACKETS_2023_SINGLE) == 4580
# def test_calc_federal_bracket3():
    assert calc_federal(90000,TAX_BRACKETS_2023_SINGLE) == 15107
# def test_calc_federal_bracket4():
    assert calc_federal(180000,TAX_BRACKETS_2023_SINGLE) == 36600
# def test_calc_federal_bracket5():
    assert calc_federal(220000,TAX_BRACKETS_2023_SINGLE) == 49232
# def test_calc_federal_bracket6():
    assert calc_federal(570000,TAX_BRACKETS_2023_SINGLE) == 171394
# def test_calc_federal_bracket7():
    assert calc_federal(700000,TAX_BRACKETS_2023_SINGLE) == 219332

def test_calc_effective_tax_rate():
    assert calc_effective_tax_rate_percent(10,1,2,3) == "60%"