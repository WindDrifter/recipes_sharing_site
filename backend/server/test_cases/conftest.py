from ...appcreate import create_app

import pytest

collect_ignore = ["lib", "var", "frontend2"]
@pytest.fixture
def app():
    app = create_app(testing=True)
    return app
