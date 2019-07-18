import os
import io

import pytest

from models import db, Project

def test_upload_projects(app):
    path_to_csv = os.path.abspath(os.path.dirname(__file__))
    path_to_csv = os.path.join(path_to_csv,
                    os.path.pardir, 'data', 'upload_projects.csv')
    data = dict([])
    with open(path_to_csv, 'rb') as csv:
        data['file'] = (io.BytesIO(csv.read()), 'test.csv')

    # import pdb; pdb.set_trace()
    with app.test_client() as client:
        # response = client.post(
        #     '/uploads',
        #     data = data,
        #     content_type = 'multipart/form-data'
        # )
        response = client.post(
            '/projects/upload/csv',
            data=data,
            content_type = 'multipart/form-data'
        )

    assert response.status_code == 200
    # get projects from database
    cool_project, lame_project, best_project  = Project.query.all()
    print(cool_project)
    print(lame_project)
    print(best_project)
    assert cool_project.name == 'SuperCoolProject'
    assert cool_project.description == 'the coolest project'
    assert cool_project.photo_url == 'www.superCoolPhoto'
    assert cool_project.website_url == 'www.superCoolProject'
    assert cool_project.year == 2000
    assert cool_project.ghg_reduced == 456
    assert cool_project.gge_reduced == 123.0

    assert lame_project.name == 'LameProject'
    assert lame_project.description == 'the lamest project'
    assert lame_project.photo_url == 'www.LamePhoto'
    assert lame_project.website_url == 'www.lameProject'
    assert lame_project.year == 1000
    assert lame_project.ghg_reduced == 987.0
    assert lame_project.gge_reduced == 543.0

    assert best_project.name == 'America'
    assert best_project.description == 'the greatest freest country on earth'
    assert best_project.photo_url == 'www.GeorgeWashington'
    assert best_project.website_url == 'www.DownWithEngland'
    assert best_project.year == 1776
    assert best_project.ghg_reduced == 5774.0
    assert best_project.gge_reduced == 704.0


#
#
# def test_get_project_type_list(app):
#     pass
#
# def test_get_project_type_by_id(app):
#     pass
#
# def test_post_project_type(app):
#     pass
#
# def test_put_project_type(app):
#     pass
#
# def test_delete_project_type(app):
#     pass
