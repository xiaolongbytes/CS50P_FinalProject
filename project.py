import sys
from reportlab.pdfgen import canvas

"""
Assumptions:
Assumed employee and not self-employed
Assumed single
Assumed standard deductions
Assumed max AGI of 1,000,000,000
2023 Tax Brackets and Contribution Limits
Assumed younger than 50 (for HSA and 401k limits, no catch-up contributions)

LIST OF ACRONYMS:
AGI = Adjusted Gross Income
HSA = Health Savings Account
"""
INPUT_QUESTIONS = [
    "Gross Income: ",
    "Traditional 401k Contribution: ",
    "HSA contribution: "
]

AGI_UPPER_LIMIT = 1000000000

STANDARD_DEDUCTION_2023_SINGLE = 13850

MAX_TRAD_401k_2023 = 22500

MAX_HSA_2023 = 3650

OASDI_2023_SINGLE = {
    "lower_limit" : 0,
    "upper_limit" : 160200,
    "OASDI_rate" : 0.062,
}

MEDICARE_2023_SINGLE = {
    "normal_rate" : 0.029,
    "additional_lower_limit" : 200000,
    "additional_rate" : 0.009,
}

TAX_BRACKETS_2023_SINGLE = [
        {
            "lower_limit" : 0,
            "upper_limit" : 11000,
            "marginal_tax_rate": 0.10,
        },
        {
            "lower_limit" : 11000,
            "upper_limit" : 44725,
            "marginal_tax_rate": 0.12,
        },
        {
            "lower_limit" : 44725,
            "upper_limit" : 95375,
            "marginal_tax_rate": 0.22,
        },
        {
            "lower_limit" : 95375,
            "upper_limit" : 182100,
            "marginal_tax_rate": 0.24,
        },
        {
            "lower_limit" : 182100,
            "upper_limit" : 231250,
            "marginal_tax_rate": 0.32,
        },
        {
            "lower_limit" : 231250,
            "upper_limit" : 578125,
            "marginal_tax_rate": 0.35,
        },
        {
            "lower_limit" : 578125,
            "upper_limit" : AGI_UPPER_LIMIT,
            "marginal_tax_rate": 0.37,
        },
]

def main():
    user_inputs = request_input(INPUT_QUESTIONS)
    agi = calc_agi(user_inputs["Gross Income: "], user_inputs["Traditional 401k Contribution: "], user_inputs["HSA contribution: "], STANDARD_DEDUCTION_2023_SINGLE)
    if agi > AGI_UPPER_LIMIT:
        sys.exit(f"AGI is greater than {AGI_UPPER_LIMIT} and is not handled by this program.")
    if user_inputs["Traditional 401k Contribution: "] > MAX_TRAD_401k_2023:
        sys.exit(f"Traditional 401k contribution is greater than {MAX_TRAD_401k_2023} and is not handled by this program.")
    if (user_inputs["Traditional 401k Contribution: "]+user_inputs["HSA contribution: "]) > user_inputs["Gross Income: "]:
        sys.exit("Invalid input. Traditional 401k and/or HSA contribution is greater than gross income.")
    if user_inputs["HSA contribution: "] > MAX_HSA_2023:
        sys.exit(f"HSA contribution is greater than {MAX_HSA_2023} and is not handled by this program.")

    user_tax_results = calculate_tax_results(agi, OASDI_2023_SINGLE, MEDICARE_2023_SINGLE, TAX_BRACKETS_2023_SINGLE, user_inputs["Gross Income: "])

    print(f'Effective Tax Rate: {user_tax_results["Effective Tax Rate: "]}')
    print_pdf_inputs_result("Effective_Tax_Rate.pdf", user_inputs, user_tax_results)
    print('See "Effective_Tax_Rate.pdf", printed in this folder, for more details.')

def calc_agi(gross_income, trad_401k, hsa, standard_deduction) -> int:
    agi = gross_income - trad_401k - hsa - standard_deduction
    return agi

def calc_OASDI(agi, OASDI_dict) -> int:
    if agi >= OASDI_dict["upper_limit"]:
        return int(OASDI_dict["upper_limit"] * OASDI_dict["OASDI_rate"])
    if agi < OASDI_dict["upper_limit"]:
        return int(agi * OASDI_dict["OASDI_rate"])

def calc_medicare(agi, medicare_dict) -> int:
    if agi >= medicare_dict["additional_lower_limit"]:
        return int(agi * medicare_dict["normal_rate"] + (agi - medicare_dict["additional_lower_limit"]) * medicare_dict["additional_rate"])
    if agi < medicare_dict["additional_lower_limit"]:
        return int(agi * medicare_dict["normal_rate"])

def calc_federal(agi, tax_brackets)-> int:
    federal_taxes = 0
    for bracket in tax_brackets:
        if agi <= bracket["lower_limit"]:
            income_in_range = 0
        elif agi > bracket["upper_limit"]:
            income_in_range = (bracket["upper_limit"] - bracket["lower_limit"])
        elif agi <= bracket["upper_limit"]:
            income_in_range = (agi - bracket["lower_limit"])
        federal_taxes += income_in_range * bracket["marginal_tax_rate"]
    return int(federal_taxes)


def calc_effective_tax_rate_percent(gross_income, oasdi, medicare, federal) -> str:
    return f"{int(round((100*(oasdi + medicare + federal)/gross_income),0))}%"

def request_input(input_list) -> dict:
    inputs = {}
    for label in input_list:
        validator, answer = validate_cash_input(input(f"{label}"))
        while validator == False:
            validator, answer = validate_cash_input(input(f"{label}"))
        inputs[(label)] = answer
    return inputs

def validate_cash_input(s) -> tuple:
    try:
        cash = int(s)
    except ValueError:
        print('Invalid input, input should be an integer and not include "$" or ","')
        return (False, 0)
    if cash < 0:
        print("Invalid input, input should be positive integer")
        return (False, 0)
    return (True, cash)

def calculate_tax_results(agi, oasdi_table, medicare_table, tax_bracket_table, gross_income):
    tax_results = {}
    tax_results["OASDI Tax: "] = calc_OASDI(agi, oasdi_table)
    tax_results["Medicare Tax: "] = calc_medicare(agi, medicare_table)
    tax_results["Federal Income Tax: "] = calc_federal(agi, tax_bracket_table)
    tax_results["Total OASDI/Medicare/Federal Taxes: "] = tax_results["OASDI Tax: "] + tax_results["Medicare Tax: "] + tax_results["Federal Income Tax: "]
    tax_results["Effective Tax Rate: "] = calc_effective_tax_rate_percent(gross_income, tax_results["OASDI Tax: "], tax_results["Medicare Tax: "], tax_results["Federal Income Tax: "])
    return tax_results


def print_pdf_inputs_result(pdf_filename, inputs_dict, tax_results_dict):
    my_canvas = canvas.Canvas(pdf_filename)
    my_canvas.setFont("Helvetica", 12)
    left_margin = 30
    line_spacing = 15
    cursor_location_from_bottom = 750
    my_canvas.drawString(left_margin, cursor_location_from_bottom, "USER INPUTS:")
    cursor_location_from_bottom -= line_spacing
    for key, val in inputs_dict.items():
        my_canvas.drawString(left_margin,cursor_location_from_bottom, f"{key}${val:,}")
        cursor_location_from_bottom -= line_spacing
    cursor_location_from_bottom -= line_spacing
    my_canvas.drawString(left_margin, cursor_location_from_bottom, "RESULTS:")
    cursor_location_from_bottom -= line_spacing
    for key, val in tax_results_dict.items():
        if type(val) == int:
            my_canvas.drawString(left_margin,cursor_location_from_bottom, f"{key}${int(val):,}")
        else:
            my_canvas.drawString(left_margin,cursor_location_from_bottom, f"{key}{val}")
        cursor_location_from_bottom -= line_spacing
    my_canvas.save()

if __name__ == "__main__":
    main()