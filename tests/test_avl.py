"""Smoke-тести базової реалізації AVL.

Перевіряємо AVL-інваріант і теоретичну межу insert ≤ 1 обертання на
будь-якому розмірі дерева. Запуск::

    pytest tests/
"""

from __future__ import annotations

import random

import pytest

from avl_asymmetry import (
    AVLNode,
    delete_node,
    get_balance,
    get_height,
    insert,
    insert_count_rot,
)


def is_avl(node):
    """True, якщо у будь-якій вершині піддерева ``|balance| <= 1``."""
    if node is None:
        return True
    if abs(get_balance(node)) > 1:
        return False
    return is_avl(node.left) and is_avl(node.right)


def heights_consistent(node):
    """True, якщо поле ``height`` коректно у будь-якій вершині."""
    if node is None:
        return True
    expected = 1 + max(get_height(node.left), get_height(node.right))
    if node.height != expected:
        return False
    return heights_consistent(node.left) and heights_consistent(node.right)


def inorder(node):
    return [] if node is None else inorder(node.left) + [node.key] + inorder(node.right)


@pytest.mark.parametrize("seed", [0, 1, 42, 100])
def test_avl_invariant_after_random_inserts(seed):
    rng = random.Random(seed)
    keys = rng.sample(range(2000), 500)
    root = None
    for k in keys:
        root = insert(root, k)
    assert is_avl(root)
    assert heights_consistent(root)
    assert inorder(root) == sorted(keys)


@pytest.mark.parametrize("seed", [0, 1, 42])
def test_avl_invariant_after_random_deletes(seed):
    rng = random.Random(seed)
    keys = rng.sample(range(2000), 500)
    root = None
    for k in keys:
        root = insert(root, k)

    to_delete = rng.sample(keys, 250)
    for k in to_delete:
        root = delete_node(root, k)
    assert is_avl(root)
    assert heights_consistent(root)
    assert inorder(root) == sorted(set(keys) - set(to_delete))


def test_insert_never_exceeds_one_rotation_per_call():
    """Теоретична гарантія Adelson-Velsky & Landis: insert <= 1 обертання."""
    rng = random.Random(7)
    keys = rng.sample(range(20000), 5000)
    root = None
    for k in keys:
        root, rot = insert_count_rot(root, k)
        assert rot <= 1, f"insert зробив {rot} обертань — порушення теореми"


def test_duplicate_insert_is_noop():
    root = None
    root = insert(root, 5)
    h_before = root.height
    root = insert(root, 5)
    assert root.height == h_before
    assert inorder(root) == [5]


def test_delete_missing_key_is_noop():
    root = None
    for k in [10, 5, 15, 3, 7]:
        root = insert(root, k)
    before = inorder(root)
    root = delete_node(root, 999)
    assert inorder(root) == before


def test_empty_tree():
    assert get_height(None) == 0
    assert get_balance(None) == 0
    assert delete_node(None, 5) is None
