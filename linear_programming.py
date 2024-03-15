# encoding: utf-8
"""linear programming example to solve maximum profit deposit problem
using PuLP library
"""

from pulp import LpMaximize, LpProblem, LpVariable, getSolver, LpStatus, value
import pandas as pd


def get_deposit_for_banks(n_bank, bank_names, deposit_bounds, rates, total_money):
    """Solve linear programming problem to get the deposit for each bank
    so that the total profit is maximized

    Args:
        n_bank: int, the number of banks
        bank_names: bank names
        deposit_bounds: list of tuples, each tuple contains the lower and upper
                        limit of the deposit for each bank
        rates: list of float, the interest rate for each bank
        total_money: float, the total money to be deposited

    Returns:
        list of float, the deposit for each bank

    Raises:
    """
    model = LpProblem("Maximize_profit", LpMaximize)

    solver = getSolver("PULP_CBC_CMD")

    # deposit list
    deposits = [
        LpVariable(
            f"x{i}",
            lowBound=deposit_bounds[i][0],
            upBound=deposit_bounds[i][1],
            cat="continuous",
        )
        for i in range(n_bank)
    ]

    # define target function
    model += sum(rates[i] * deposits[i] for i in range(n_bank))

    # constraints
    model += sum(deposits[i] for i in range(n_bank)) == total_money

    # solve
    results = model.solve(solver=solver)

    # print result to file
    with open("output.txt", "w+", encoding="utf-8") as f:
        if LpStatus[results] == "Optimal":
            f.write("The solution is optimal.\n")

        f.write(f"Objective value: z = {value(model.objective)}\n")
        for i in range(n_bank):
            f.write(f"{bank_names[i]} = {value(deposits[i])}\n")


def main():
    # Read Excel file in current path
    wb = pd.ExcelFile("Parameters.xlsx")
    sheet_names = wb.sheet_names
    df_dict = {}

    for sheet_name in sheet_names:
        df_dict[sheet_name] = wb.parse(sheet_name=sheet_name)

    info = df_dict[sheet_names[0]]

    tt_money = df_dict[sheet_names[1]]

    n_bank = info.shape[0]
    deposit_bounds = list(
        info[["Lower Bound", "Upper Bound"]].itertuples(index=False, name=None)
    )
    rates = info["Rate"].tolist()
    total_money = tt_money["Total Money"].tolist()[0]

    bank_names = info["Bank"].tolist()
    get_deposit_for_banks(n_bank, bank_names, deposit_bounds, rates, total_money)


if __name__ == "__main__":
    main()
