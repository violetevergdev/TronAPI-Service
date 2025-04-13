import random


def validate_item_structure(item):
    assert isinstance(item["address"], str)
    assert isinstance(item["bandwidth"], int)
    assert isinstance(item["energy"], int)
    assert isinstance(item["trx_balance"], int)
    assert isinstance(item["timestamp"], str)


class TestTronAPI:
    def test_post_torn_info(self, _setup_api, test_client):
        TEST_URL, config, _ = _setup_api

        valid_test_post_data = {
            "address": random.choice(config['test-data']['tron-addresses'])
        }
        invalid_test_post_data = {
            "address": 'TDUQAb7c1hqTR4TJdxZ4MASEN6NhNbXTDo'
        }
        invalid_type_test_post_data = {
            "address": 1242342
        }

        invalid_res = test_client.post(TEST_URL, json=invalid_test_post_data)
        assert invalid_res.status_code == 404

        empty_res = test_client.post(TEST_URL, json={})
        assert empty_res.status_code == 422

        invalid_type_res = test_client.post(TEST_URL, json=invalid_type_test_post_data)
        assert invalid_type_res.status_code == 422

        valid_res = test_client.post(TEST_URL, json=valid_test_post_data)
        assert valid_res.status_code == 200
        res_data = valid_res.json()
        validate_item_structure(res_data)
        assert valid_res.headers["Content-Type"] == "application/json"

        get_res = test_client.get(TEST_URL)
        post_timestamp = res_data['timestamp']
        get_timestamp = get_res.json()['items'][0]['timestamp']
        assert post_timestamp == get_timestamp

    def test_get_torn_info(self, _setup_api, test_client):
        TEST_URL, _, _ = _setup_api

        res = test_client.get(TEST_URL)
        assert res.status_code == 200

        res_data = res.json()
        assert "items" in res_data and isinstance(res_data["items"], list)
        assert "pagination" in res_data and isinstance(res_data["pagination"], dict)

        if len(res_data['items']) > 0:
            item = res_data['items'][0]
            validate_item_structure(item)

        pagination_data = res_data['pagination']
        for key in ("total_items", "total_pages", "page", "per_page"):
            assert isinstance(pagination_data[key], int)
