import unittest
import os
from base64 import b64encode
import json
from app import app
from models import setup_db, db_drop_and_create_all, Album, Image
import io

class APITests(unittest.TestCase):
    def setUp(self):
        self.avatarToken = os.environ.get('AVATAR_TOKEN', 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVXdXJydm95ZUwzU0tlR29GOUdTVSJ9.eyJpc3MiOiJodHRwczovL2Rldi13enJ1dXJpMzVhNDIzcnoyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNDY1MjMxMTg5MjMzMTc0NzYyOCIsImF1ZCI6WyJjYXBzdG9uZVByb2plY3QiLCJodHRwczovL2Rldi13enJ1dXJpMzVhNDIzcnoyLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTkzMjM1NjQsImV4cCI6MTY5OTQwOTk2NCwiYXpwIjoiUkVNVVVnNVNUcnpPbDF0SXhxZ01sZUxEQnNkc2tJZ1YiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFsYnVtcyIsImRlbGV0ZTppbWFnZXMiLCJwYXRjaDphbGJ1bXMiLCJwb3N0OmFsYnVtcyIsInBvc3Q6aW1hZ2VzIl19.ctquxU4DT3vEIJz6pxCWm8CdLDAq1YperGoNTtRkzjPrp-8w057bhilIDlvn4wJgv7GgbMRaeF-JKWJaj5oKbCXeessYxmNycM86JLhSt7sIIxXpvB7lGUV7MC3PrCQyiEPO4qWJQgQPP0hOheREcnJGCZJm0IxHHny2Gm2zr-lEb1IhMT5idlqfFFJbfgXsT2JmvKKFcMNB0zy1zMNzf-uwAJvcB4tifWCO1IsD9D7XSHRujiK3BMBeH_9tw6plCs5eq5-06QqPoLeA1bcqkzYr0CpXEPMcpeOrGNZa1-XYoWC_jpRnwxOw225hhL7RYd_Jk_KIzyCz5fMskqQ2Jg')
        self.adminImageToken = os.environ.get('ADMIN_IMAGE_TOKEN', 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVXdXJydm95ZUwzU0tlR29GOUdTVSJ9.eyJpc3MiOiJodHRwczovL2Rldi13enJ1dXJpMzVhNDIzcnoyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMTI1MTM2MDUxMzM0NjYyNzU4OCIsImF1ZCI6WyJjYXBzdG9uZVByb2plY3QiLCJodHRwczovL2Rldi13enJ1dXJpMzVhNDIzcnoyLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTkzMzA5MzQsImV4cCI6MTY5OTQxNzMzNCwiYXpwIjoiUkVNVVVnNVNUcnpPbDF0SXhxZ01sZUxEQnNkc2tJZ1YiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmltYWdlcyIsInBvc3Q6aW1hZ2VzIl19.ZQKY6MUzdKhObcoYtOnyktyUQakdflgfVsu_hqd_msPGFQtBd-Ey4qb-E2t4N2Y2Ts8XVy0xu-HLVxOWZ_im_HlNZWNYO9q5cRY_PpV9vDk6yOfh6lrpwcPkc8HCRPjGJ-s51UW_UqIUsxIOzNyK29WMlbR7Nqr988DKcTGRfrxg-beCQmfvZaJsTHSE35eJiYP3LaQxEqJRB215kMN3gJRPfkeFfG9qBU1yHC8x2ZHfVKuoq-3E4C0b1uK7s0doITnIvDWpAyddDtLh-3qKzX8e8aR0S9OoTEW6nqofpGbnBJzfMh4nKnQLMp41vWqceQrQMmEKyqYFWLob12E9yw')
        self.simpleUserToken = os.environ.get('SIMPLE_USER_TOKEN', 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVXdXJydm95ZUwzU0tlR29GOUdTVSJ9.eyJpc3MiOiJodHRwczovL2Rldi13enJ1dXJpMzVhNDIzcnoyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNzE4MTU4ODEyNjU0ODc4MjE1OCIsImF1ZCI6WyJjYXBzdG9uZVByb2plY3QiLCJodHRwczovL2Rldi13enJ1dXJpMzVhNDIzcnoyLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTkzMzIzMDYsImV4cCI6MTY5OTQxODcwNiwiYXpwIjoiUkVNVVVnNVNUcnpPbDF0SXhxZ01sZUxEQnNkc2tJZ1YiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOltdfQ.UljRa1LoLugw4L0223YST2tXKUAnQ-0WqBAz6KrlHHkhI-fWL-TZacFlZ6m-rcHw1jeJAroRN5IYGXcssrIu4DV297zR6EpGNlTkvHb3YASq_WEQHcRnpgDZs-fbZBUPTy_dPXF8mbFW7FvXSOCNuorUGvBjXWVJpDmBaDfUp9KJgx_IPbW5STCKNNls35-l9HeQL97FDyVvdUrIGgmyiD8zVPzY2lv-QqUfuRXEV1-P2XmBvhIaH-yvJm2BV3NGHxuoVLb-dDYVTjQ85AHhbmCcTdmJ_bMOUlX8Yd7hPGYrfi9IRHI-B9NrsV531cwsnH7wPlD8etXP-GKJeIl3mw')
        with app.app_context():
            db_drop_and_create_all()
        self.client = app.test_client
        self.image_path = os.environ.get('IMAGE_SAMPLE_PATH', 'avatar_1.jpg')
        pass

    def testAlbumAsAvatar(self):
        # test post albums errors
        headers = {
            'Authorization': 'Bearer ' + self.avatarToken,
            "Content-Type": "application/json"
        }
        res = self.client().post('/albums')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]['description'], 'Authorization header is expected.')

        res = self.client().post('/albums', headers=headers, json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

        # test post albums
        res = self.client().post('/albums', headers=headers, json={'albumName': 'First Album'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        albumId = data["albums"][0]["id"]

        # test patch albums error
        res = self.client().patch('/albums/{0}'.format(albumId), headers=headers, json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

        # test patch album
        newName = 'newName 2.0'
        res = self.client().patch('/albums/{0}'.format(albumId), headers=headers, json={'newName': newName})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # test get albums
        res = self.client().get('/albums')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["albums"][0]["name"], newName)

        # test delete albums
        res = self.client().delete('/albums/{0}'.format(albumId), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # test delete albums error
        res = self.client().delete('/albums/{0}'.format(albumId), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

        # test get albums error
        res = self.client().get('/albums')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

    '''
        There is not need to test the get since the token is omitted in other tests
    '''
    def albumsWithNoPermission(self, token):
        # test post albums error
        headers = {
            'Authorization': 'Bearer ' + token,
            "Content-Type": "application/json"
        }
        res = self.client().post('/albums', headers=headers, json={'albumName': 'First Album'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]['description'], 'User does not have the right permissions')

        # test patch albums error
        newName = 'newName 2.0'
        albumId = 1
        res = self.client().patch('/albums/{0}'.format(albumId), headers=headers, json={'newName': newName})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]['description'], 'User does not have the right permissions')

        # test delete albums error
        res = self.client().delete('/albums/{0}'.format(albumId), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]['description'], 'User does not have the right permissions')

    def testAlbumsWithAdminImage(self):
        self.albumsWithNoPermission(self.adminImageToken)

    def testAlbumsWithSimpleUser(self):
        self.albumsWithNoPermission(self.simpleUserToken)

    def imagesWithPermissions(self, token, albumId, expectedErrorWhenDeleteAlbum):
        headers = {
            'Authorization': 'Bearer ' + token,
        }
        # test post images errors
        res = self.client().post("/albums/{0}/images".format(albumId))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]['description'], 'Authorization header is expected.')

        res = self.client().post(
                '/albums/{0}/images'.format(albumId),
                data=dict(),
                follow_redirects=True,
                headers=headers
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

        # test post images
        image = None
        with open(self.image_path, "rb") as f:
            image = f.read()
        self.assertTrue(image)
        res = self.client().post(
                '/albums/{0}/images'.format(albumId),
                data=dict(file=(io.BytesIO(image), self.image_path)),
                follow_redirects=True,
                headers=headers
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        imageId = data["images"][0]["id"]
        imageURL = data["images"][0]["url"]

        # test get images
        res = self.client().get('/albums/{0}/images'.format(albumId))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["images"][0]["url"], imageURL)

        # test delete album error
        res = self.client().delete('/albums/{0}'.format(albumId), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, expectedErrorWhenDeleteAlbum)
        self.assertEqual(data["success"], False)

        # test delete images
        res = self.client().delete('/images/{0}'.format(imageId), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # test delete images error
        res = self.client().delete('/images/{0}'.format(imageId), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

        # test get images error
        res = self.client().get('/albums/{0}/images'.format(albumId))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

    def testImagesWithAvatar(self):
        # create album for test with avatar
        headers = {
            'Authorization': 'Bearer ' + self.avatarToken,
            "Content-Type": "application/json"
        }
        res = self.client().post('/albums', headers=headers, json={'albumName': 'First Album'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        albumId = data["albums"][0]["id"]

        self.imagesWithPermissions(self.avatarToken, albumId, 422)

        # delete album
        res = self.client().delete('/albums/{0}'.format(albumId), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


    def testImagesWithAdminImage(self):
        # create album for test with avatar
        headers = {
            'Authorization': 'Bearer ' + self.avatarToken,
            "Content-Type": "application/json"
        }
        res = self.client().post('/albums', headers=headers, json={'albumName': 'First Album'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        albumId = data["albums"][0]["id"]

        self.imagesWithPermissions(self.adminImageToken, albumId, 403)

        # delete album
        res = self.client().delete('/albums/{0}'.format(albumId), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    '''
        There is not need to test the get since the token is omitted in other tests
    '''
    def testImagesWithSimpleUser(self):
        # test post images error
        headers = {
            'Authorization': 'Bearer ' + self.simpleUserToken,
        }
        image = None
        with open(self.image_path, "rb") as f:
            image = f.read()
        self.assertTrue(image)
        res = self.client().post(
                '/albums/{0}/images'.format(1),
                data=dict(file=(io.BytesIO(image), self.image_path)),
                follow_redirects=True,
                headers=headers
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]['description'], 'User does not have the right permissions')

        # test delete images error
        res = self.client().delete('/images/{0}'.format(1), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]['description'], 'User does not have the right permissions')

if __name__ == "__main__":
    unittest.main()