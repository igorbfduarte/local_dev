import psycopg2.extras as p

from src.transformer.enrich_user_data import run
from utils.data_generator import make_name
from utils.db import WarehouseConnection
from utils.sde_config import get_warehouse_creds


class TestDataPipeline:
    def setup_method(self, test_data_pipeline):
        insert_query = '''
            INSERT INTO housing.user (
                id,
                price
            )
            VALUES (
                %(id)s,
                %(price)s
            )
        '''
        user_fixture = [
            {'id': 1, 'price': 1},
            {'id': 2, 'price': 2},
            {'id': 3, 'price': 3},
            {'id': 4, 'price': 4},
        ]
        with WarehouseConnection(
            get_warehouse_creds()
        ).managed_cursor() as curr:
            p.execute_batch(curr, insert_query, user_fixture)

    def teardown_method(self, test_data_pipeline):
        with WarehouseConnection(
            get_warehouse_creds()
        ).managed_cursor() as curr:
            curr.execute("TRUNCATE TABLE housing.user_enriched;")

    def test_data_pipeline(self):
        run()
        with WarehouseConnection(
            get_warehouse_creds()
        ).managed_cursor() as curr:
            curr.execute("Select id, price, name from housing.user_enriched")
            enriched_user_data = curr.fetchall()
        expected_data = [
            (user_id, price, make_name(user_id))
            for user_id, price in zip(range(1, 5), range(1, 5))
        ]
        assert enriched_user_data == expected_data


# import pytest
#
# from your.data_pipeline_path import run_your_datapipeline
#
#
# class TestYourDataPipeline:
#    @pytest.fixtures(scope="class", autouse=True)
#    def input_data_fixture(self):
#        # get input fixture data ready
#        yield
#        self.tear_down()
#
#    def test_data_pipeline_success(self):
#        run_your_datapipeline()
#        result = {"some data or file"}
#        expected_result = "predefined expected data or file"
#        assert result == expected_result
#
#    def tear_down(self):
#        # remove input fixture data
