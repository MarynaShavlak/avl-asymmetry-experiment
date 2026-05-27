"""AVL-tree asymmetry: insert vs delete rotation counts.

Публічне API пакета — реекспорт основних функцій кожного підмодуля,
щоб користувачам не доводилось знати внутрішню організацію.
"""

from .avl import (
    AVLNode,
    delete_node,
    get_balance,
    get_height,
    insert,
    left_rotate,
    min_value_node,
    right_rotate,
)
from .tracked import delete_tracked, insert_count_rot, insert_tracked
from .trace import delete_with_trace
from .visualization import (
    count_nodes,
    extract_cascade_view,
    get_all_keys,
    visualize_avl_inorder,
)

__all__ = [
    # avl
    "AVLNode",
    "get_height",
    "get_balance",
    "left_rotate",
    "right_rotate",
    "min_value_node",
    "insert",
    "delete_node",
    # tracked
    "insert_tracked",
    "delete_tracked",
    "insert_count_rot",
    # trace
    "delete_with_trace",
    # visualization
    "visualize_avl_inorder",
    "extract_cascade_view",
    "count_nodes",
    "get_all_keys",
]

__version__ = "0.1.0"
