"""Експеримент 1 — емпірична перевірка теорії.

Будуємо AVL з ``N=5000`` випадкових ключів, рахуємо обертання за кожен
виклик ``insert``. Потім видаляємо половину у випадковому порядку,
рахуємо обертання за кожен ``delete``. Друкуємо описову статистику і
малюємо дві гістограми.

Запуск з кореня репозиторію::

    python -m experiments.01_empirical_distribution
"""

from __future__ import annotations

import random
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

from avl_asymmetry import delete_tracked, insert_count_rot


def main() -> None:
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["font.size"] = 10
    random.seed(42)
    np.random.seed(42)

    n_keys = 5000
    keys = random.Random(0).sample(range(n_keys * 3), n_keys)

    root = None
    insert_rot_per_call = []
    for k in keys:
        root, rot = insert_count_rot(root, k)
        insert_rot_per_call.append(rot)

    del_keys = keys[: n_keys // 2]
    random.Random(99).shuffle(del_keys)
    delete_rot_per_call = []
    for k in del_keys:
        counter = [0]
        root = delete_tracked(root, k, counter)
        delete_rot_per_call.append(counter[0])

    ins_dist = Counter(insert_rot_per_call)
    del_dist = Counter(delete_rot_per_call)

    print(f"INSERT (N={len(insert_rot_per_call)} викликів):")
    print(f"  макс. обертань за виклик: {max(insert_rot_per_call)}")
    print(
        f"  середнє:                 "
        f"{sum(insert_rot_per_call) / len(insert_rot_per_call):.3f}"
    )
    print(f"  розподіл: {dict(sorted(ins_dist.items()))}")

    print(f"\nDELETE (N={len(delete_rot_per_call)} викликів):")
    print(f"  макс. обертань за виклик: {max(delete_rot_per_call)}")
    print(
        f"  середнє:                 "
        f"{sum(delete_rot_per_call) / len(delete_rot_per_call):.3f}"
    )
    print(f"  розподіл: {dict(sorted(del_dist.items()))}")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    max_k = max(max(ins_dist.keys()), max(del_dist.keys()))
    xs = list(range(max_k + 1))

    ins_pcts = [100 * ins_dist.get(k, 0) / len(insert_rot_per_call) for k in xs]
    del_pcts = [100 * del_dist.get(k, 0) / len(delete_rot_per_call) for k in xs]

    axes[0].bar(xs, ins_pcts, color="#27ae60", alpha=0.8)
    axes[0].set_title("INSERT: розподіл обертань за виклик")
    axes[0].set_xlabel("обертань за виклик")
    axes[0].set_ylabel("% викликів")
    axes[0].set_xticks(xs)
    axes[0].grid(alpha=0.3, axis="y")
    for k, p in zip(xs, ins_pcts):
        if p > 0:
            axes[0].text(k, p + 1, f"{p:.1f}%", ha="center", fontsize=9)

    axes[1].bar(xs, del_pcts, color="#c0392b", alpha=0.8)
    axes[1].set_title("DELETE: розподіл обертань за виклик")
    axes[1].set_xlabel("обертань за виклик")
    axes[1].set_ylabel("% викликів")
    axes[1].set_xticks(xs)
    axes[1].grid(alpha=0.3, axis="y")
    for k, p in zip(xs, del_pcts):
        if p > 0:
            axes[1].text(k, p + 1, f"{p:.1f}%", ha="center", fontsize=9)

    plt.suptitle("E2. Асиметрія insert vs delete за кількістю обертань", y=1.02)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
