import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, mock_open
from pathlib import Path

from app import app
from src.sematicsearch_api.models import Query, QueryResponse
from langchain_core.documents import Document


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_retriever():
    retriever = Mock()
    retriever.invoke.return_value = [
        Document(page_content="Test document 1"),
        Document(page_content="Test document 2")
    ]
    return retriever


@pytest.fixture
def sample_query():
    return {"text": "test query"}


class TestApp:
    
    @patch("builtins.open", mock_open(read_data="<h1>Test HTML</h1>"))
    @patch("os.path.exists", return_value=True)
    def test_home_with_html_file(self, mock_exists, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "<h1>Test HTML</h1>" in response.text

    @patch("os.path.exists", return_value=False)
    def test_home_without_html_file(self, mock_exists, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "<h1>Sematic Search Microservice</h1>" in response.text

    @patch("app.retriever")
    def test_search_valid_query(self, mock_retriever_patch, client, mock_retriever, sample_query):
        mock_retriever_patch.return_value = mock_retriever
        
        with patch("app.Search") as mock_search_class:
            mock_search_instance = Mock()
            mock_search_instance.sematic_results.return_value = [
                Document(page_content="Result 1"),
                Document(page_content="Result 2")
            ]
            mock_search_class.return_value = mock_search_instance
            
            response = client.post("/sematic", json=sample_query)
            
            assert response.status_code == 200
            assert "0. Result 1" in response.text
            assert "1. Result 2" in response.text

    def test_search_empty_text(self, client):
        response = client.post("/sematic", json={"text": ""})
        assert response.status_code == 400
        assert response.json()["detail"] == "Text input is required."

    def test_search_whitespace_only(self, client):
        response = client.post("/sematic", json={"text": "   "})
        assert response.status_code == 400
        assert response.json()["detail"] == "Text input is required."

    def test_search_missing_text_field(self, client):
        response = client.post("/sematic", json={})
        assert response.status_code == 422

    @patch("app.retriever")
    def test_search_single_result(self, mock_retriever_patch, client, mock_retriever):
        mock_retriever_patch.return_value = mock_retriever
        
        with patch("app.Search") as mock_search_class:
            mock_search_instance = Mock()
            mock_search_instance.sematic_results.return_value = [
                Document(page_content="Single result")
            ]
            mock_search_class.return_value = mock_search_instance
            
            response = client.post("/sematic", json={"text": "test"})
            
            assert response.status_code == 200
            assert response.text == '"0. Single result"'

    @patch("app.retriever")
    def test_search_no_results(self, mock_retriever_patch, client, mock_retriever):
        mock_retriever_patch.return_value = mock_retriever
        
        with patch("app.Search") as mock_search_class:
            mock_search_instance = Mock()
            mock_search_instance.sematic_results.return_value = []
            mock_search_class.return_value = mock_search_instance
            
            response = client.post("/sematic", json={"text": "test"})
            
            assert response.status_code == 200
            assert response.text == '""'


class TestModels:
    
    def test_query_model_valid(self):
        query = Query(text="test query")
        assert query.text == "test query"

    def test_query_response_model_valid(self):
        docs = [Document(page_content="test")]
        response = QueryResponse(results=docs)
        assert len(response.results) == 1
        assert response.results[0].page_content == "test"


@patch("app.pickle.load")
@patch("builtins.open", mock_open())
@patch("app.Path")
def test_retriever_loading(mock_path, mock_pickle_load):
    mock_retriever = Mock()
    mock_pickle_load.return_value = mock_retriever
    
    # Reload the module to test initialization
    import importlib
    import app
    importlib.reload(app)
    
    mock_pickle_load.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])