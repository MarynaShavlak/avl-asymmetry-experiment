"""Експеримент 2 — візуальний доказ каскаду.

Будуємо те саме дерево, що в експерименті 1, шукаємо ключ із найбільшим
каскадом обертань при видаленні, виконуємо видалення з трасуванням і
малюємо «околицю каскаду» ДО і ПІСЛЯ.

Запуск з кореня репозиторію::

    python -m experiments.02_cascade_demo
"""

from __future__ import annotations

import copy
import random

import matplotlib.pyplot as plt
import numpy as np

from avl_asymmetry import (
    count_nodes,
    delete_tracked,
    delete_with_trace,
    extract_cascade_view,
    get_all_keys,
    get_height,
    insert_count_rot,
    visualize_avl_inorder,
)


def build_tree(n_keys: int = 5000):
    """Той самий протокол, що в експерименті 1: вставляємо, потім видаляємо половину."""
    keys = random.Random(0).sample(range(n_keys * 3), n_keys)
    root = None
    for k in keys:
        root, _ = insert_count_rot(root, k)
    del_keys = keys[: n_keys // 2]
    random.Random(99).shuffle(del_keys)
    for k in del_keys:
        counter = [0]
        root = delete_tracked(root, k, counter)
    return root


def count_rotations_for_delete(tree, key: int) -> int:
    """Лічить обертання для одного ``delete`` (на копії дерева)."""
    tmp = copy.deepcopy(tree)
    counter = [0]
    delete_tracked(tmp, key, counter)
    return counter[0]


def main() -> None:
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["font.size"] = 10
    random.seed(42)
    np.random.seed(42)

    root = build_tree()
    all_keys = get_all_keys(root)
    print(f"Дерево має {len(all_keys)} вершин, висота = {get_height(root)}")

    sample_keys = random.Random(123).sample(all_keys, min(500, len(all_keys)))
    print(f"Перевіряємо {len(sample_keys)} випадкових ключів на каскад...")

    candidates = [(k, count_rotations_for_delete(root, k)) for k in sample_keys]
    candidates.sort(key=lambda x: -x[1])

    print("\nТоп-10 ключів за каскадом:")
    for k, n in candidates[:10]:
        print(f"  ключ {k:>6}: {n} обертань")

    target_key, target_rot = candidates[0]
    print(
        f"\nОбираємо для демонстрації ключ {target_key} → "
        f"каскад {target_rot} обертань"
    )

    before = copy.deepcopy(root)
    print(f"\n=== Виконуємо delete({target_key}) ===\n")
    after, rotations = delete_with_trace(copy.deepcopy(root), target_key)

    print("\n=== Підсумок ===")
    print(f"Видалено ключ: {target_key}")
    print(f"Актів балансування: {len(rotations)}")
    print(f"Висота дерева ДО:    {get_height(before)}")
    print(f"Висота дерева ПІСЛЯ: {get_height(after)}")

    rotated_keys = [k for _, k, _ in rotations]
    focus_before = {target_key} | set(rotated_keys)
    focus_after = set(rotated_keys)

    before_view = extract_cascade_view(before, focus_before, off_path_depth=1)
    after_view = extract_cascade_view(after, focus_after, off_path_depth=1)

    print(f"\nПовне дерево:        {count_nodes(before)} вершин")
    print(f"Околиця ДО:          {count_nodes(before_view)} вершин")
    print(f"Околиця ПІСЛЯ:       {count_nodes(after_view)} вершин")

    visualize_avl_inorder(
        before_view,
        title=(
            f"Околиця каскаду ДО: видаляємо {target_key} (червоний); "
            f"обертання трапляться на {rotated_keys}"
        ),
        highlight_keys=[target_key] + rotated_keys,
        show_balance=True,
    )

    visualize_avl_inorder(
        after_view,
        title=(
            f"Та сама околиця ПІСЛЯ: виконано {len(rotations)} "
            "актів балансування"
        ),
        highlight_keys=rotated_keys,
        show_balance=True,
    )


if __name__ == "__main__":
    main()
