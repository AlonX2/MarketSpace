import sys, pytest, requests
sys.path.extend(["../../../../.", "../../../.", "../../."])

from unittest.mock import patch

from crunchbase.src.crunchbase_query import CrunchbaseSearchQuery, CrunchbaseQueryError

@pytest.fixture()
def crunchbase_search_query_fixture():
    url = "test/url"
    fields = ["testfield1", "testfield2"]
    return CrunchbaseSearchQuery(url, fields)

def test_noSortingDefined_defineSorting_addSortingToQuery(crunchbase_search_query_fixture: CrunchbaseSearchQuery):
    crunchbase_search_query_fixture.define_sorting("sortfield")
    assert "order" in crunchbase_search_query_fixture._query
    assert crunchbase_search_query_fixture._query["order"] == {"field_id": "sortfield", "sort": "desc"}

def test_sortingAlreadyDefined_defineSorting_error(crunchbase_search_query_fixture: CrunchbaseSearchQuery):
    crunchbase_search_query_fixture.define_sorting("")
    with pytest.raises(CrunchbaseQueryError):
        crunchbase_search_query_fixture.define_sorting("")

def test_filterInfo_addFilter_addQueryFieldToQuery(crunchbase_search_query_fixture: CrunchbaseSearchQuery):
    crunchbase_search_query_fixture.add_filter("testfield", "op", "val")
    assert len(crunchbase_search_query_fixture._query["query"]) == 1
    assert crunchbase_search_query_fixture._query["query"][0] == {"type": "predicate",
                                                                  "field_id": "testfield",
                                                                  "operator_id": "op",
                                                                  "values": ["val"]}  

def test_filterAlreadyExists_addFilter_addQueryFieldToQuery(crunchbase_search_query_fixture: CrunchbaseSearchQuery):
    crunchbase_search_query_fixture.add_filter("testfield", "op", "val")
    crunchbase_search_query_fixture.add_filter("testfield2", "op2", "val2")
    assert len(crunchbase_search_query_fixture._query["query"]) == 2
    assert crunchbase_search_query_fixture._query["query"][1] == {"type": "predicate",
                                                                  "field_id": "testfield2",
                                                                  "operator_id": "op2",
                                                                  "values": ["val2"]}  
    
def test_onePageResult_execute_returnEntities(crunchbase_search_query_fixture: CrunchbaseSearchQuery):
    with (patch("requests.post") as requests_post_mock,
          patch("crunchbase.src.crunchbase_query.CrunchbaseSearchQuery._ensure_query_integrity") as ensure_query_mock,
          patch("crunchbase.src.crunchbase_query.get_env_vars") as get_env_mock):
        
        requests_post_mock.return_value.json.return_value = {"entities": ["e1", "e2", "e3"]}
        requests_post_mock.return_value.status_code = 200
        get_env_mock.return_value = ["API_KEY"]

        assert crunchbase_search_query_fixture.execute() == ["e1", "e2", "e3"]

        get_env_mock.assert_called_once()
        ensure_query_mock.assert_called_once()
        requests_post_mock.assert_called_once_with("test/url", params={"user_key": "API_KEY"}, json={"field_ids": ["testfield1", "testfield2"], "limit": 500})
        
def test_twoPageResult_execute_returnEntities(crunchbase_search_query_fixture: CrunchbaseSearchQuery):
    with (patch("requests.post") as requests_post_mock,
          patch("crunchbase.src.crunchbase_query.CrunchbaseSearchQuery._ensure_query_integrity") as ensure_query_mock,
          patch("crunchbase.src.crunchbase_query.get_env_vars") as get_env_mock,
          patch("crunchbase.src.crunchbase_query.PAGINATION_BATCH_SIZE", 2)):
        
        requests_post_mock.return_value.json.side_effect = [{"entities": [{"uuid": 1}, {"uuid": 2}]},
                                                            {"entities": [{"uuid": 3}]}]
        requests_post_mock.return_value.status_code = 200
        get_env_mock.return_value = ["API_KEY"]

        assert crunchbase_search_query_fixture.execute() == [{"uuid": 1}, {"uuid": 2}, {"uuid": 3}]

        get_env_mock.assert_called_once()
        ensure_query_mock.assert_called_once()

        assert requests_post_mock.call_count == 2
        requests_post_mock.assert_called_with("test/url", params={"user_key": "API_KEY"}, json={"field_ids": ["testfield1", "testfield2"], "limit": 2, "after_id": 2})

def test_error_execute_queryError(crunchbase_search_query_fixture: CrunchbaseSearchQuery):
    with (patch("requests.post") as requests_post_mock,
          patch("crunchbase.src.crunchbase_query.CrunchbaseSearchQuery._ensure_query_integrity") as ensure_query_mock,
          patch("crunchbase.src.crunchbase_query.get_env_vars") as get_env_mock):
        
        requests_post_mock.side_effect = requests.exceptions.RequestException
        get_env_mock.return_value = ["API_KEY"]

        with pytest.raises(CrunchbaseQueryError):
            crunchbase_search_query_fixture.execute()