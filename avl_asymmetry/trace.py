"""Версія ``delete``, що друкує тип і центр кожного акта балансування.

Призначено для покрокових демонстрацій каскаду на одному конкретному
видаленні: коли треба не просто отримати кількість обертань, а буквально
побачити, *де* кожне з них спрацювало.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from .avl import (
    AVLNode,
    get_balance,
    get_height,
    left_rotate,
    min_value_node,
    right_rotate,
)

# (тип_обертання, ключ_центру_обертання, баланс_до_обертання)
RotationRecord = Tuple[str, int, int]


def delete_with_trace(
    root: Optional[AVLNode],
    key: int,
    _rotations: Optional[List[RotationRecord]] = None,
) -> Tuple[Optional[AVLNode], List[RotationRecord]]:
    """Видаляє ``key`` і друкує кожен акт балансування під час підйому рекурсії.

    Повертає пару ``(новий_корінь, список_записів_про_обертання)``.
    LR/RL рахуються як один запис (один акт), аналогічно до
    :func:`avl_asymmetry.tracked.delete_tracked`.
    """
    if _rotations is None:
        _rotations = []

    if not root:
        return root, _rotations
    if key < root.key:
        root.left, _ = delete_with_trace(root.left, key, _rotations)
    elif key > root.key:
        root.right, _ = delete_with_trace(root.right, key, _rotations)
    else:
        if root.left is None:
            return root.right, _rotations
        elif root.right is None:
            return root.left, _rotations
        temp = min_value_node(root.right)
        root.key = temp.key
        root.right, _ = delete_with_trace(root.right, temp.key, _rotations)

    if root is None:
        return root, _rotations
    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1:
        if get_balance(root.left) >= 0:
            _rotations.append(("LL", root.key, balance))
            print(
                f"  ↻ #{len(_rotations)}: LL навколо вузла {root.key} "
                f"(balance тут був {balance:+d})"
            )
            return right_rotate(root), _rotations
        _rotations.append(("LR", root.key, balance))
        print(
            f"  ↻ #{len(_rotations)}: LR (подвійне) навколо вузла {root.key} "
            f"(balance тут був {balance:+d})"
        )
        root.left = left_rotate(root.left)
        return right_rotate(root), _rotations

    if balance < -1:
        if get_balance(root.right) <= 0:
            _rotations.append(("RR", root.key, balance))
            print(
                f"  ↻ #{len(_rotations)}: RR навколо вузла {root.key} "
                f"(balance тут був {balance:+d})"
            )
            return left_rotate(root), _rotations
        _rotations.append(("RL", root.key, balance))
        print(
            f"  ↻ #{len(_rotations)}: RL (подвійне) навколо вузла {root.key} "
            f"(balance тут був {balance:+d})"
        )
        root.right = right_rotate(root.right)
        return left_rotate(root), _rotations

    return root, _rotations
