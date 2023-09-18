# Effective Tax Rate Calculator
#### Video Demo:  <https://youtu.be/O6QPoLdZ0g8>
#### Description:
The effective tax rate calculator project calculates the effective tax rate.

### Assumptions
1. W-2 Employee (not self-employed)
2. Single (not married)
3. Standard Deductions
4. Maximum AGI of $1,000,000,000
5. 2023 Tax Brackets and Contribution Limits
6. Assumes person is younger than 50 (no catch-up contributions)

### User Inputs:
1. Gross Pre-Tax Income
2. Traditional 401k Contributions
3. HSA Contributions

### Program Outputs:
1. Calculates Effective Tax Rate Percentage (considering OASDI, Medicare, and Federal Income Tax)
2. Generates "Effective_Tax_Rate.pdf" of inputs and results

### Program Files:
1. README.md - This file. Explains this project.
2. project.py - Contains project code. See "project.py" section below for in-depth explaination of the code.
3. requirements.txt - Lists pip-installable libraries that project.py requires. "reportlab.pdfgen" is required to create the output pdf and "pytest" was used for testing.
4. Effective_Tax_Rate.pdf - Output of program. File will be overwritten each time project.py successfully runs unless this pdf file is manually renamed.
5. test_project.py - Contains tests for the following functions in project.py: calc_agi, calc_OASDI, calc_medicare, validate_cash_input, calc_federal, and calc_effective_tax_rate

## project.py
* Imports sys for sys.exit and reportlab.pdfgen in order to create pdfs later
* Lists Assumption in docstring
* Global constants are set (Input questions, 2023 limits and tax brackets)
* calc_agi calculates the Adjusted Gross Income from the inputs
* calc_OASDI calculates OASDI tax component
* calc_medicare calculates medicare tax component
* calc_federal calculates federal income tax component
* calc_effective_tax_rate_percent returns effective tax rate as a percent in a string
* request_input asks the questions and if the input is not valid, will continue to prompt the user
* validate_cash_input validates that inputs are integers without symbols
* calculate_tax_results formats the results to be printed
* print_pdf_inputs_result creates a pdf with the output results
### Design Decisions:
1. Initially I wanted to have this project also handle married filing jointly taxes. However I eventually realized that this increases the complexity of the project as I'd have to submit and track both individual's income/contributions and calculate OASDI limits for each. I decided to limit my project to a single filer as a "Minimum Viable Product".
2. I initially also wanted to include State and City taxes, since my local taxes were flat percentages. I soon learned that not every state or city has flat percentages, and also how large a problem it would be to store the information for every city and every state. I decided to cut this from the project scope.
3. The tax code is complex. In order to limit the number of inputs from the user (birthday/age, children, deductions, employee vs independent contractor), I limited the scope to the assumptions listed in the "Assumptions" at the top of the README file.
4. I had wanted to add a feature to calculate how many pounds of gold your taxes were worth, just for fun. However Gold APIs were behind paywalls or required web scraping, so I decided to cut that feature from the scope.

