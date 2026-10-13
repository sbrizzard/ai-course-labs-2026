"""消费统计与满额优惠：金额使用 Decimal，路径相对源码定位。"""
import json
from pathlib import Path
from decimal import Decimal


def load_expenses():
    path = Path(__file__).resolve().parent / "data" / "expenses.json"
    return json.loads(path.read_text(encoding="utf-8"))


def total_expenses(expenses):
    values = [Decimal(str(item["amount"])) for item in expenses]
    if any(not amount.is_finite() or amount < 0 for amount in values):
        raise ValueError("金额必须为有限非负数")
    return sum(values, Decimal("0")).quantize(Decimal("0.01"))


def discounted_total(total):
    total = Decimal(str(total))
    if not total.is_finite() or total < 0:
        raise ValueError("总金额必须为有限非负数")
    result = total * Decimal("0.9") if total >= Decimal("100") else total
    return result.quantize(Decimal("0.01"))
