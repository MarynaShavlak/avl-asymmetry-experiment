"""Інструментовані ``insert`` і ``delete``, що рахують обертання за один виклик.

Логіка ідентична функціям з :mod:`avl_asymmetry.avl` — додані лише
лічильники перед кожним обертанням. Виносити в окремий модуль зручно
тому, що базовий ``avl`` лишається чистим, а тут — усе про вимірювання.

Угода щодо одиниці виміру:

* для ``insert_tracked`` ми розрізняємо тип кожного обертання
  (LL/RR/LR/RL) і рахуємо по типах окремо у ``collections.Counter``;
* для ``delete_tracked`` нам важлива лише сумарна кількість обертань
  (саме каскад), тому всі типи лягають в один лічильник ``counter[0]``;
* **LR/RL рахуються як ОДИН акт балансування**, а не як два — попри те,
  що під капотом вони виконують два примітивні обертання. Так само як в
  оригінальній теоремі Adelson-Velsky & Landis.
"""

from __future__ import annotations

from collections import Counter
from typing import List, Optional

from .avl import (
    AVLNode,
    get_balance,
    get_height,
    left_rotate,
    min_value_node,
    right_rotate,
)


def insert_tracked(
    root: Optional[AVLNode], key: int, counter: Counter
) -> AVLNode:
    """``insert``, що інкрементує ``counter[case]`` за кожне обертання."""
    if not root:
        return AVLNode(key)
    if key < root.key:
        root.left = insert_tracked(root.left, key, counter)
    elif key > root.key:
        root.right = insert_tracked(root.right, key, counter)
    else:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1:
        if key < root.left.key:
            counter["LL"] += 1
            return right_rotate(root)
        counter["LR"] += 1
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if balance < -1:
        if key > root.right.key:
            counter["RR"] += 1
            return left_rotate(root)
        counter["RL"] += 1
        root.right = right_rotate(root.right)
        return left_rotate(root)
    return root


def delete_tracked(
    root: Optional[AVLNode], key: int, counter: List[int]
) -> Optional[AVLNode]:
    """``delete_node``, що інкрементує ``counter[0]`` за кожне обертання."""
    if not root:
        return root
    if key < root.key:
        root.left = delete_tracked(root.left, key, counter)
    elif key > root.key:
        root.right = delete_tracked(root.right, key, counter)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        temp = min_value_node(root.right)
        root.key = temp.key
        root.right = delete_tracked(root.right, temp.key, counter)

    if root is None:
        return root
    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1:
        if get_balance(root.left) >= 0:
            counter[0] += 1
            return right_rotate(root)
        counter[0] += 1
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if balance < -1:
        if get_balance(root.right) <= 0:
            counter[0] += 1
            return left_rotate(root)
        counter[0] += 1
        root.right = right_rotate(root.right)
        return left_rotate(root)
    return root


def insert_count_rot(root: Optional[AVLNode], key: int):
    """Обгортка: вставка з поверненням пари ``(новий_корінь, к-сть_обертань)``."""
    counter: Counter = Counter()
    root = insert_tracked(root, key, counter)
    return root, sum(counter.values())
