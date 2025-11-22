from abc import ABC, abstractmethod
from typing import ClassVar, Optional


class RuleRegistry:
    _rules = {}

    @classmethod
    def register(cls, name, rule_class):
        cls._rules[name] = rule_class

    @classmethod
    def get_rule(cls, name):
        return cls._rules.get(name)

    @classmethod
    def get_all_rules(cls):
        return cls._rules


class BaseRule(ABC):
    name: ClassVar[Optional[str]] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if getattr(cls, "name", None):
            RuleRegistry.register(cls.name, cls)

    @abstractmethod
    def check(self, order):
        pass


class MinTotal100Rule(BaseRule):
    name = "min_total_100"

    def check(self, order):
        return order.total > 100


class MinItems2Rule(BaseRule):
    name = "min_items_2"

    def check(self, order):
        return order.items_count >= 2


class DivisibleBy5Rule(BaseRule):
    name = "divisible_by_5"

    def check(self, order):
        return order.total % 5 == 0


# TEST NEW RULES
# class MaxTotal500Rule(BaseRule):
#     """
#     Checks if the order total is less than 500
#     """
#     name = "max_total_500"

#     def check(self, order):
#         return order.total < 100
