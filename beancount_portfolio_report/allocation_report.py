#!/usr/bin/env python3
__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

from tabulate import tabulate

import beancount_portfolio_report.loader as loader


def report_data(targets, allocations, total):
    result = dict()
    for asset_class in allocations.asset_classes():
        asset_class_result = list()
        sum_percentage_in_all = 0
        for subclass in allocations.asset_subclasses(asset_class):
            one_subclass_line, percentage_in_all = count_subclass(targets, allocations, total, asset_class, subclass)
            asset_class_result.append(one_subclass_line)
            sum_percentage_in_all = sum_percentage_in_all + percentage_in_all

        asset_class_summary_line = count_asset_class_summary(allocations, asset_class, sum_percentage_in_all)
        asset_class_result.append(asset_class_summary_line)

        result[asset_class] = asset_class_result
    total_summary_line = count_total_summary(allocations)
    result['TOTAL'] = [total_summary_line]
    return result


def count_subclass(targets, allocations, total, asset_class, subclass):
    book_value = allocations.cost_for_class_subclass(asset_class, subclass)
    market_value = allocations.value_for_class_subclass(asset_class, subclass)
    pnl = allocations.pnl_for_class_subclass(asset_class, subclass)
    pnl_percentage = allocations.pnl_percentage_for_class_subclass(asset_class,
                                                                   subclass)
    asset_market_value = allocations.value_for_class(asset_class)
    percentage_in_class = market_value / asset_market_value * 100
    percentage_in_all = allocations.percentage_for_class_subclass(asset_class,
                                                                  subclass)
    target = targets.get(subclass, 0)
    diff = cash_difference(target, percentage_in_all, total)
    line = [subclass, float(book_value), float(market_value), float(pnl), float(pnl_percentage),
            float(percentage_in_class), float(percentage_in_all), float(target), float(diff)]
    return line, percentage_in_all


def count_asset_class_summary(allocations, asset_class, sum_percentage_in_all):
    book_value = allocations.cost_for_class(asset_class)
    market_value = allocations.value_for_class(asset_class)
    pnl = allocations.pnl_for_class(asset_class)
    pnl_percentage = allocations.pnl_percentage_for_class(asset_class)
    # Note that sum of "% of asset_class" will always be equal to 100 such that we hard-coded here
    line = ['SUM', float(book_value), float(market_value), float(pnl), float(pnl_percentage), 100,
            float(sum_percentage_in_all)]
    return line


def count_total_summary(allocations):
    market_value = allocations.total_invested_for_portfolio()
    book_value = allocations.total_cost_for_portfolio()
    pnl = allocations.total_pnl()
    pnl_percentage = allocations.total_pnl_percentage()
    line = ['SUM', float(book_value), float(market_value), float(pnl), float(pnl_percentage)]
    return line


def report(bean, portfolio):
    targets, allocations, total = loader.load(bean, portfolio)
    data = report_data(targets, allocations, total)

    head = ["Subclass", "Book Value", "Market Value", "PnL", "PnL %", "% in asset_class", "% in All",
            "Target %", "Difference"]
    report = ""
    first = True

    for asset_class in data:
        head[5] = "% in " + asset_class
        if not first:
            report += "\n\n"
        else:
            first = False
        report += asset_class.upper()
        report += "\n"
        report += "=" * len(asset_class)
        report += "\n"

        report += tabulate(data[asset_class], head, floatfmt='.2f')
        report += "\n"

    return report


def percentage_difference(target, percentage):
    return float(target - percentage)


def cash_difference(target, percentage, total):
    return percentage_difference(target, percentage) / 100 * float(total)


def main():
    import argparse
    parser = argparse.ArgumentParser("Report on portfolio asset classes allocation vs targets.")
    parser.add_argument('bean', help='Path to the beancount file.')
    parser.add_argument('--portfolio',
                        type=str,
                        help='Name of portfolio to report on',
                        required=True)
    args = parser.parse_args()

    print(report(args.bean, args.portfolio))


if __name__ == "__main__":
    main()
