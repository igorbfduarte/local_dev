import pytest
from src.loader.load_user_data import load_user_data
from utils.db import WarehouseConnection
from utils.sde_config import get_warehouse_creds


def _truncate_user_data():
    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
        curr.execute("Truncate table housing.user;")


@pytest.fixture()
def set_up_tear_down():
    # Clean up existing data
    _truncate_user_data()
    yield
    _truncate_user_data()


class TestLoadUserData:
    def test_load_user_data(self, set_up_tear_down):
        load_user_data()
        with WarehouseConnection(
            get_warehouse_creds()
        ).managed_cursor() as curr:
            curr.execute("select count(*) from housing.user;")
            d = curr.fetchone()

        assert d[0] == 10

        
#import pytest
#
#from your.data_pipeline_path import run_your_datapipeline
#
#
#class TestYourDataPipeline:
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

