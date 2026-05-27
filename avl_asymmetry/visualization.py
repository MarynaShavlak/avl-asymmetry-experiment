"""Утиліти візуалізації дерева через matplotlib.

Дві функції:

* :func:`visualize_avl_inorder` — малює дерево in-order розкладкою
  (координата X = ранг у in-order обході, Y = глибина); опційно показує
  висоту і баланс у вузлі та підсвічує задані ключі.
* :func:`extract_cascade_view` — для дерев у тисячі вершин повертає
  «вирізку»: повний шлях від кореня до фокусних ключів плюс невелику
  околицю навколо нього. Решта дерева обрізається — інакше картинка
  стане нечитабельною смугою точок.
"""

from __future__ import annotations

from typing import Iterable, Optional

import matplotlib.pyplot as plt

from .avl import AVLNode, get_balance


def visualize_avl_inorder(
    root: Optional[AVLNode],
    title: str = "AVL",
    highlight_keys: Optional[Iterable[int]] = None,
    figsize: Optional[tuple] = None,
    show_balance: bool = False,
    ax: Optional["plt.Axes"] = None,
    max_width: int = 20,
) -> None:
    """Малює дерево in-order розкладкою.

    :param root: корінь дерева (``None`` → друкуємо повідомлення і виходимо).
    :param highlight_keys: ключі, які треба підсвітити червоним.
    :param show_balance: чи виводити в підписі вузла висоту і баланс.
    :param ax: якщо переданий, малюємо в нього (без ``show``); інакше
        створюємо власну фігуру.
    :param max_width: верхня межа ширини фігури в дюймах — на гігантських
        деревах matplotlib без обмеження зависає.
    """
    if root is None:
        print("Порожнє дерево")
        return

    positions: dict = {}
    labels: dict = {}
    keys_by_id: dict = {}
    edges: list = []
    rank = [0]

    def walk(node: Optional[AVLNode], depth: int) -> None:
        if node is None:
            return
        walk(node.left, depth + 1)
        rank[0] += 1
        nid = id(node)
        positions[nid] = (rank[0], -depth)
        keys_by_id[nid] = node.key
        labels[nid] = (
            f"{node.key}\nh={node.height} b={get_balance(node):+d}"
            if show_balance
            else str(node.key)
        )
        if node.left:
            edges.append((nid, id(node.left)))
        if node.right:
            edges.append((nid, id(node.right)))
        walk(node.right, depth + 1)

    walk(root, 0)
    n = rank[0]
    if ax is None:
        if figsize is None:
            figsize = (min(max_width, max(8, n * 0.4)), 6)
        _, ax = plt.subplots(figsize=figsize)
        own = True
    else:
        own = False

    for p, c in edges:
        px, py = positions[p]
        cx, cy = positions[c]
        ax.plot([px, cx], [py, cy], color="gray", alpha=0.6, linewidth=1.2, zorder=1)

    highlight = set(highlight_keys or [])
    for nid, (x, y) in positions.items():
        color = "lightcoral" if keys_by_id[nid] in highlight else "lightblue"
        ax.scatter(x, y, s=500, c=color, edgecolors="black", linewidths=1, zorder=2)
        ax.text(x, y, labels[nid], ha="center", va="center", fontsize=7, zorder=3)

    ax.set_title(title, fontsize=11)
    ax.set_xlim(0, n + 1)
    y_min = min(p[1] for p in positions.values())
    ax.set_ylim(y_min - 0.7, 0.7)
    ax.axis("off")
    if own:
        plt.tight_layout()
        plt.show()


def extract_cascade_view(
    root: Optional[AVLNode],
    focus_keys: Iterable[int],
    off_path_depth: int = 1,
) -> Optional[AVLNode]:
    """Повертає копію дерева з обрізаним до «околиці» вмістом.

    Залишає:

    * усі ancestor-вузли на шляху від кореня до кожного з ``focus_keys``
      (так званий *спайн*);
    * для кожного такого вузла — його піддерево, обмежене глибиною
      ``off_path_depth``.

    Решта обрізається. Корисно, щоб показати ділянку, де відбувається
    каскад, а не намагатись намалювати все дерево з тисяч вершин.
    """
    focus = set(focus_keys)
    interesting: set = set()

    def mark(node: Optional[AVLNode]) -> bool:
        if node is None:
            return False
        left_has = mark(node.left)
        right_has = mark(node.right)
        self_is = node.key in focus
        if left_has or right_has or self_is:
            interesting.add(id(node))
            return True
        return False

    mark(root)

    def copy_node(
        node: Optional[AVLNode], depth_remaining: int
    ) -> Optional[AVLNode]:
        if node is None:
            return None
        new = AVLNode(node.key)
        new.height = node.height
        if id(node) in interesting:
            new.left = copy_node(node.left, off_path_depth)
            new.right = copy_node(node.right, off_path_depth)
        elif depth_remaining > 0:
            new.left = copy_node(node.left, depth_remaining - 1)
            new.right = copy_node(node.right, depth_remaining - 1)
        return new

    return copy_node(root, 0)


def count_nodes(node: Optional[AVLNode]) -> int:
    """Кількість вершин у піддереві."""
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)


def get_all_keys(node: Optional[AVLNode]) -> list:
    """Усі ключі дерева в in-order порядку."""
    if not node:
        return []
    return get_all_keys(node.left) + [node.key] + get_all_keys(node.right)
