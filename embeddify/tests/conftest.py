from embeddify import Embedder
import pytest

@pytest.fixture
def embedder():
    return Embedder()


