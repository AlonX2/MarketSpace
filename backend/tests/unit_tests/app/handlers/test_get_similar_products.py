import sys, pytest
sys.path.extend([".", "../."])

from flask import Flask
from unittest.mock import patch, MagicMock

from backend.app.handlers._get_similar_products import *
from backend.app.custom_config import CustomConfig


@pytest.fixture
def custom_config_fixture():
    app = Flask(__name__)
    custom_config_mock = MagicMock()
    def mock_ms_client(*_, **__):
        return "{\"feature1\": [0.1, 0.2], \"feature2\": [0.3, 0.4]}"
    custom_config_mock.microservice_client.invoke.side_effect = mock_ms_client
    
    with app.app_context():
        with patch("app.handlers._get_similar_products.current_app.config", {"CUSTOM": custom_config_mock}):
            yield custom_config_mock

def test_featureResolverUnavailable_getSimilarProducts_raiseError(custom_config_fixture: CustomConfig):
    custom_config_fixture.microservice_client.invoke.side_effect = MicroserviceClientException()
    with pytest.raises(GetSimilarProductsException, match="Feature resolvance and embedding failed"):
        get_similar_products("test_product_desc_json")
    custom_config_fixture.microservice_client.invoke.assert_called_once_with(target_queue=FEATURE_RESOLVER_QUEUE, data_json="test_product_desc_json")

def test_dbUnavailable_getSimilarProducts_raiseError(custom_config_fixture: CustomConfig):
    custom_config_fixture.db_client.query.side_effect = DbClientException()
    with pytest.raises(GetSimilarProductsException, match="Vector DB client failed getting similar embeddings for features"):
        get_similar_products("test_product_desc_json")
    custom_config_fixture.db_client.query.assert_called_once_with(vector=[0.1, 0.2], space="feature1", num=5)

def test_servicesAvailable_getSimilarProducts_returnResults(custom_config_fixture: CustomConfig):
    def db_client_query_side_effect(vector, space, num):
        return f"similar_products_on_space_{space}"
    custom_config_fixture.db_client.query.side_effect = db_client_query_side_effect
    
    res = get_similar_products("")

    assert "feature1" in res and "feature2" in res and len(res.keys()) == 2
    assert res["feature2"] == "similar_products_on_space_feature2"

    query_mock_calls = custom_config_fixture.db_client.query.mock_calls
    assert len(query_mock_calls) == 2
    first_call_kwargs, second_call_kwargs = (call[2] for call in query_mock_calls)
    assert first_call_kwargs["vector"] == [0.1, 0.2] and first_call_kwargs["space"] == "feature1" and first_call_kwargs["num"] == 5
    assert second_call_kwargs["vector"] == [0.3, 0.4] and second_call_kwargs["space"] == "feature2" and second_call_kwargs["num"] == 5