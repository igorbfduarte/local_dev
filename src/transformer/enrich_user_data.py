from typing import Any, Dict, List, Tuple

import psycopg2.extras as p

from utils.data_generator import make_name
from utils.db import WarehouseConnection
from utils.sde_config import get_warehouse_creds


def get_user_data() -> List[Tuple[int, int]]:
    user_info = []
    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
        curr.execute("Select id, price from housing.user")
        user_info = curr.fetchall()
    return [(int(u[0]), int(u[1])) for u in user_info]


def enrich_user_data(user_info: List[Tuple[int, int]]) -> List[Dict[str, Any]]:
    enriched_data = []
    for id, price in user_info:
        data = {'id': id, 'price': price, 'name': make_name(id)}
        enriched_data.append(data)
    return enriched_data


def send_data_to_destination(data: List[Dict[str, Any]]):
    insert_query = '''
    INSERT INTO housing.user_enriched (
        id,
        price,
        name
    )
    VALUES (
        %(id)s,
        %(price)s,
        %(name)s
    )
    '''
    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
        p.execute_batch(curr, insert_query, data)


def run() -> None:
    send_data_to_destination(enrich_user_data(get_user_data()))


if __name__ == '__main__':
    run()
