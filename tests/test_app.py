from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

url = "/respond"

request_data = [
    {
        "active_skills": [["dff_friendship_skill", "dff_friendship_skill", "dff_music_skill"]],
        "cobot_topics": [["Phatic", "Phatic", "Phatic", "Music", "Phatic"]],
    }
]

expected_results = [["dff_gossip_skill", "dff_movie_skill"]]


def test_respond_one_correct():
    response = client.post(url, json=request_data[0])
    assert response.status_code == 200
    assert response.json() == [["dff_gossip_skill", "dff_movie_skill"]]


def test_not_valid_request():
    response = client.post(url, json={
        "active_skills": [[]]
    })
    assert response.status_code == 422

    response = client.post(url, json={
        "cobot_topics": [[]]
    })

    assert response.status_code == 422


def test_respond_many():
    for data, result in zip(request_data, expected_results):
        response = client.post(url, json=data)
        assert response.status_code == 200
        assert response.json()[0] == result
