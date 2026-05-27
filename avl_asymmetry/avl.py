"""Базова реалізація AVL-дерева.

AVL-дерево — самобалансоване BST з інваріантом ``|balance(node)| <= 1``,
де ``balance = height(left) - height(right)``.

Цей модуль містить мінімальну робочу реалізацію: вузол, обертання,
``insert`` і ``delete_node``. Жодна функція тут не рахує обертання — для
експериментів використовуй інструментовані варіанти з
:mod:`avl_asymmetry.tracked` і :mod:`avl_asymmetry.trace`.
"""

from __future__ import annotations

from typing import Optional


class AVLNode:
    """Вузол AVL-дерева."""

    __slots__ = ("key", "height", "left", "right")

    def __init__(self, key: int) -> None:
        self.key: int = key
        self.height: int = 1
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None


def get_height(node: Optional[AVLNode]) -> int:
    """Висота вузла; 0 для ``None``."""
    return node.height if node else 0


def get_balance(node: Optional[AVLNode]) -> int:
    """Фактор балансу: ``height(left) - height(right)``."""
    return get_height(node.left) - get_height(node.right) if node else 0


def left_rotate(z: AVLNode) -> AVLNode:
    """Ліве обертання навколо ``z``. Повертає новий корінь піддерева."""
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y


def right_rotate(y: AVLNode) -> AVLNode:
    """Праве обертання навколо ``y``. Повертає новий корінь піддерева."""
    x = y.left
    T3 = x.right
    x.right = y
    y.left = T3
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x


def min_value_node(node: AVLNode) -> AVLNode:
    """Найлівіший (мінімальний) вузол піддерева з коренем ``node``."""
    while node.left:
        node = node.left
    return node


def insert(root: Optional[AVLNode], key: int) -> AVLNode:
    """Вставка ключа з відновленням AVL-інваріанта. Дублікати ігноруються."""
    if not root:
        return AVLNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1:
        if key < root.left.key:
            return right_rotate(root)
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if balance < -1:
        if key > root.right.key:
            return left_rotate(root)
        root.right = right_rotate(root.right)
        return left_rotate(root)
    return root


def delete_node(root: Optional[AVLNode], key: int) -> Optional[AVLNode]:
    """Видалення ключа з відновленням AVL-інваріанта.

    Якщо ключа немає — дерево повертається без змін. Для вузла з двома
    дітьми використовується in-order successor (мінімум правого піддерева).
    """
    if not root:
        return root
    if key < root.key:
        root.left = delete_node(root.left, key)
    elif key > root.key:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        temp = min_value_node(root.right)
        root.key = temp.key
        root.right = delete_node(root.right, temp.key)

    if root is None:
        return root
    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1:
        if get_balance(root.left) >= 0:
            return right_rotate(root)
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if balance < -1:
        if get_balance(root.right) <= 0:
            return left_rotate(root)
        root.right = right_rotate(root.right)
        return left_rotate(root)
    return root
