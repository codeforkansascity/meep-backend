import pytest

from models import Project, db


def test_post_project(app):
    db.create_all()
    with app.test_client() as client:
        response = client.post(
            '/locations',
            json=dict(
                name='some project',
                photo_url='path.to.photo.jpg',
                website_url='www.awesomesite.org',
                year=2019,
                gge_reduced=42.0,
                ghg_reduced=43.0
            )
        )
        assert response.status_code == 201

        [project] = Project.query.limit(1).all()
        assert project.name == 'some project'

# def test_get_project_list(app):
#     pass
#
# def test_get_project_by_id(app):
#     pass
#
#
# def test_put_project(app):
#     pass
#
# def test_delete_project(app):
#     pass
