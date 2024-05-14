import unittest
import os
from base64 import b64encode
import json
from app import app
from models import setup_db, db_drop_and_create_all, Album, Image
import io


class APITests(unittest.TestCase):
    def setUp(self):
        self.avatarToken = os.environ.get('AVATAR_TOKEN', '')
        self.adminImageToken = os.environ.get('ADMIN_IMAGE_TOKEN', '')
        self.simpleUserToken = os.environ.get('SIMPLE_USER_TOKEN', '')
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
        self.assertEqual(
            data["message"]['description'],
            'Authorization header is expected.')

        res = self.client().post('/albums', headers=headers, json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

        # test post albums
        res = self.client().post(
            '/albums',
            headers=headers,
            json={'albumName': 'First Album'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        albumId = data["albums"][0]["id"]

        # test patch albums error
        res = self.client().patch(
            '/albums/{0}'.format(albumId),
            headers=headers,
            json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

        # test patch album
        newName = 'newName 2.0'
        res = self.client().patch(
            '/albums/{0}'.format(albumId),
            headers=headers,
            json={'newName': newName})
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
        res = self.client().delete(
            '/albums/{0}'.format(albumId),
            headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # test delete albums error
        res = self.client().delete(
            '/albums/{0}'.format(albumId),
            headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

        # test get albums error
        res = self.client().get('/albums')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

    '''
        There is not need to test the get since
        the token is omitted in other tests
    '''
    def albumsWithNoPermission(self, token):
        # test post albums error
        headers = {
            'Authorization': 'Bearer ' + token,
            "Content-Type": "application/json"
        }
        res = self.client().post(
            '/albums',
            headers=headers,
            json={'albumName': 'First Album'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(
            data["message"]['description'],
            'User does not have the right permissions')

        # test patch albums error
        newName = 'newName 2.0'
        albumId = 1
        res = self.client().patch(
            '/albums/{0}'.format(albumId),
            headers=headers,
            json={'newName': newName})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(
            data["message"]['description'],
            'User does not have the right permissions')

        # test delete albums error
        res = self.client().delete(
            '/albums/{0}'.format(albumId),
            headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(
            data["message"]['description'],
            'User does not have the right permissions')

    def testAlbumsWithAdminImage(self):
        self.albumsWithNoPermission(self.adminImageToken)

    def testAlbumsWithSimpleUser(self):
        self.albumsWithNoPermission(self.simpleUserToken)

    def imagesWithPermissions(
                self, token, albumId, expectedErrorWhenDeleteAlbum):
        headers = {
            'Authorization': 'Bearer ' + token,
        }
        # test post images errors
        res = self.client().post("/albums/{0}/images".format(albumId))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(
            data["message"]['description'],
            'Authorization header is expected.')

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
        res = self.client().delete(
            '/albums/{0}'.format(albumId),
            headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, expectedErrorWhenDeleteAlbum)
        self.assertEqual(data["success"], False)

        # test delete images
        res = self.client().delete(
            '/images/{0}'.format(imageId),
            headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # test delete images error
        res = self.client().delete(
            '/images/{0}'.format(imageId),
            headers=headers)
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
        res = self.client().post(
            '/albums',
            headers=headers,
            json={'albumName': 'First Album'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        albumId = data["albums"][0]["id"]

        self.imagesWithPermissions(self.avatarToken, albumId, 422)

        # delete album
        res = self.client().delete(
            '/albums/{0}'.format(albumId),
            headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def testImagesWithAdminImage(self):
        # create album for test with avatar
        headers = {
            'Authorization': 'Bearer ' + self.avatarToken,
            "Content-Type": "application/json"
        }
        res = self.client().post(
            '/albums',
            headers=headers,
            json={'albumName': 'First Album'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        albumId = data["albums"][0]["id"]

        self.imagesWithPermissions(self.adminImageToken, albumId, 403)

        # delete album
        res = self.client().delete(
            '/albums/{0}'.format(albumId),
            headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    '''
        There is not need to test the get since
        the token is omitted in other tests
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
        self.assertEqual(
            data["message"]['description'],
            'User does not have the right permissions')

        # test delete images error
        res = self.client().delete('/images/{0}'.format(1), headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(
            data["message"]['description'],
            'User does not have the right permissions')


if __name__ == "__main__":
    unittest.main()
