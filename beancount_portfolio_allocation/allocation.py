__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"


class Allocations(list):
    def asset_classes(self):
        result = set()
        for p in self:
            result.add(p.asset_class)
        sorted_results = list(result)
        sorted_results.sort()
        return sorted_results

    def asset_subclasses(self, asset_class):
        result = set()
        for p in self:
            if p.asset_class == asset_class:
                result.add(p.asset_subclass)
        sorted_results = list(result)
        sorted_results.sort()
        return sorted_results

    def value_for_class_subclass(self, asset_class, asset_subclass):
        result = 0
        for p in self:
            if (p.asset_class == asset_class and
                    p.asset_subclass == asset_subclass):
                result += p.value
        return result

    def percentage_for_class_subclass(self, asset_class, asset_subclass):
        return (100 *
                (self.value_for_class_subclass(asset_class, asset_subclass) /
                 self.total_invested_for_portfolio()))

    def total_invested_for_portfolio(self):
        return sum([p.value for p in self])


class Position:
    def __init__(self, symbol, value, asset_class, asset_subclass, account):
        self.symbol = symbol
        self.value = value
        self.asset_class = asset_class
        self.asset_subclass = asset_subclass
        self.account = account