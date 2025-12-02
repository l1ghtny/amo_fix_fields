import re
from typing import Tuple, Any, Iterable

DELIVERY_PREFIXES = (
    "CDEK",
    "Доставка курьером",
    "Самовывоз",
)

async def parse_the_cart_field(data: str):
    items = re.findall(r'^\s*\d+\.\s*(.+)$', data, flags=re.MULTILINE)

    products = []
    deliveries = []

    for item in items:
        line = item.strip()

        # 2. Classify based on the delivery prefixes
        if line.startswith(DELIVERY_PREFIXES):
            deliveries.append(line)
        else:
            products.append(line)

    # 3. Turn lists into strings (you can change the joiner if you want)
    products_str = "\n".join(products)
    deliveries_str = "\n".join(deliveries)

    return products_str, deliveries_str


_MISSING = object()

def get_nested(data: Any, path: Iterable[str], default: Any = None) -> Any:
    """
    Safely get nested values from dicts/lists using a path of keys/indexes.
    Example:
        get_nested(nested, ["leads", "update", "0", "id"])
    """
    current = data

    for key in path:
        if isinstance(current, dict):
            current = current.get(key, _MISSING)
        elif isinstance(current, list):
            # support numeric keys for lists like ["0", "1"]
            try:
                idx = int(key)
                current = current[idx]
            except (ValueError, IndexError):
                current = _MISSING
        else:
            current = _MISSING

        if current is _MISSING:
            return default

    return current