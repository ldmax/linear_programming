# encoding: utf-8
"""linear programming example to solve maximum profit deposit problem
using PuLP library
"""

from pulp import LpMaximize, LpProblem, LpVariable, getSolver, LpStatus, value


def get_deposit_for_banks(n_bank, deposit_bounds, rates, total_money):
    """Solve linear programming problem to get the deposit for each bank
    so that the total profit is maximized

    Args:
        n_bank: int, the number of banks
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

    # 存款列表
    deposits = [
        LpVariable(
            f"x{i}",
            lowBound=deposit_bounds[i][0],
            upBound=deposit_bounds[i][1],
            cat="continuous",
        )
        for i in range(n_bank)
    ]

    # 定义目标函数
    model += sum(rates[i] * deposits[i] for i in range(n_bank))

    # 定义约束条件
    model += sum(deposits[i] for i in range(n_bank)) == total_money

    # 求解
    results = model.solve(solver=solver)

    # 打印结果
    if LpStatus[results] == "Optimal":
        print("The solution is optimal.")

    print(f"Objective value: z = {value(model.objective)}")
    for i in range(n_bank):
        print(f"x{i+1} = {value(deposits[i])}")

    return [value(deposits[i]) for i in range(n_bank)]


def read_information_from_excel(path):
    """Read information from Excel file
    TODO: read Excel file from current path and retrieve information
    """
    pass 


def main():
    pass


if __name__ == "__main__":
    n_bank = 10  # 银行家数

    # 各家银行存款上下限
    deposit_bounds = [
        (1, 2),
        (3, 10),
        (5, 9),
        (2.4, 14),
        (1, 2),
        (1, 2),
        (1, 2),
        (1, 2),
        (1, 2),
        (1, 2),
    ]

    # 各家银行存款利率
    rates = [0.1, 0.07, 0.05, 0.03, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01]

    # 总存款
    total_money = 34

    deposits = get_deposit_for_banks(n_bank, deposit_bounds, rates, total_money)
