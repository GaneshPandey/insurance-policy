from flask import url_for


class TestUserView(object):
    def test_main_route(self, client):
        response = client.get(url_for("user.index"))
        assert response.status_code == 200
