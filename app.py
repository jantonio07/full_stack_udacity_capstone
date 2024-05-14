import os
from flask import Flask, render_template, jsonify, request, abort
from flask_cors import CORS
from image_control import ImageControl
from auth import AuthError, requires_auth
from models import setup_db, create_all, Album, Image
from sqlalchemy import asc
from flask_migrate import Migrate

NO_FILE_IN_UPLOAD_REQUEST_MESSAGE = "There was no file in upload request"
NO_NAME_IN_CREATE_ALBUM_REQUEST_MESSAGE = "There was no file in upload request"
NO_NEW_NAME_IN_PATCH_ALBUM_REQUEST_MESSAGE = "There was no \
    new name in patch request"
NO_ALBUMS_TO_SHOW_MESSAGE = "No albums to show"
NO_IMAGES_TO_SHOW_MESSAGE = "No images to show"
NO_ALBUM_FOUND_MESSAGE = "No album found"
NO_IMAGE_FOUND_MESSAGE = "No image found"
IMAGEKIT_EXCEPTION_MESSAGE = "Something went wrong in imagekit"

app = Flask(__name__)
db = setup_db(app)
migrate = Migrate(app, db)
CORS(app)

# with app.app_context():
#     create_all()

ik = ImageControl()


@app.route("/")
def hello_world():
    return render_template(
            "index.html",
            AUTH0_DOMAIN=os.environ.get('AUTH0_DOMAIN', ''),
            AUTH0_CLIENT_ID=os.environ.get('AUTH0_CLIENT_ID', ''),
            AUTH0_AUDIENCE=os.environ.get('AUTH0_AUDIENCE', '')
        )


@app.route("/albums/<int:albumId>/images")
def get_images(albumId):
    try:
        query = Image.query.filter_by(albumId=albumId)
        query = query.order_by(asc(Image.id))
        images = [image.getData() for image in query.all()]
        if len(images) == 0:
            raise Exception(NO_IMAGES_TO_SHOW_MESSAGE)
        return jsonify({
                "success": True,
                "images": images,
            })
    except Exception as e:
        print("\nEXCEPTION get_images", e, end='\n\n')
        if e.__str__() == NO_IMAGES_TO_SHOW_MESSAGE:
            abort(400)
        else:
            abort(422)


@app.route("/images/<int:imageId>", methods=["DELETE"])
@requires_auth('delete:images')
def delete_image(payload, imageId):
    try:
        image = Image.query.filter_by(id=imageId).first()
        if image is None:
            raise Exception(NO_IMAGE_FOUND_MESSAGE)
        imageKitId = image.imageKitId
        try:
            ik.delete_image(imageKitId)
        except Exception as e:
            print("\nIMAGEKIT_EXCEPTION upload_image", e, end='\n\n')
            raise Exception(IMAGEKIT_EXCEPTION_MESSAGE)
        image.delete()
        return jsonify({
                "success": True,
                "delete": imageId,
            })

    except Exception as e:
        print("\nEXCEPTION delete_image", e, end='\n\n')
        if e.__str__() == NO_IMAGE_FOUND_MESSAGE:
            abort(404)
        else:
            abort(422)


@app.route("/albums/<int:albumId>/images", methods=["POST"])
@requires_auth('post:images')
def upload_image(payload, albumId):
    try:
        response = {
            "success": False,
            "message": None
        }
        if 'file' not in request.files:
            raise Exception(NO_FILE_IN_UPLOAD_REQUEST_MESSAGE)
        album = Album.query.filter_by(id=albumId).first()
        if album is None:
            raise Exception(NO_ALBUM_FOUND_MESSAGE)
        try:
            image = request.files['file'].read()
            response = ik.upload_image(image, "image.jpeg")
        except Exception as e:
            print("\nIMAGEKIT_EXCEPTION upload_image", e, end='\n\n')
            raise Exception(IMAGEKIT_EXCEPTION_MESSAGE)
        image = Image(
            w=response['metadata']['width'],
            h=response['metadata']['height'],
            url=response['metadata']['url'],
            imageKitId=response['metadata']['fileId'],
            albumId=albumId
        )
        image.insert()
        response = {}
        response["success"] = True
        response["images"] = [image.getData()]
        return jsonify(response)
    except Exception as e:
        print("\nEXCEPTION upload_image", e, end='\n\n')
        if e.__str__() == NO_FILE_IN_UPLOAD_REQUEST_MESSAGE:
            abort(400)
        else:
            abort(422)


@app.route("/albums", methods=["POST"])
@requires_auth('post:albums')
def create_album(payload):
    try:
        data = request.get_json()
        albumName = None
        if 'albumName' in data:
            albumName = data['albumName']
        if albumName is not None and len(albumName) > 0:
            album = Album(
                name=albumName
            )
            album.insert()
            response = {}
            response["success"] = True
            response["albums"] = [album.getData()]
            return jsonify(response)
        else:
            raise Exception(NO_NAME_IN_CREATE_ALBUM_REQUEST_MESSAGE)
    except Exception as e:
        print("\nEXCEPTION create_album", e, end='\n\n')
        if e.__str__() == NO_NAME_IN_CREATE_ALBUM_REQUEST_MESSAGE:
            abort(400)
        else:
            abort(422)


@app.route("/albums")
def get_albums():
    try:
        albums = [
            album.getData() for
            album in Album.query.order_by(asc(Album.id)).all()
        ]
        if len(albums) == 0:
            raise Exception(NO_ALBUMS_TO_SHOW_MESSAGE)
        return jsonify({
                "success": True,
                "albums": albums,
            })
    except Exception as e:
        print("\nEXCEPTION get_albums", e, end='\n\n')
        if e.__str__() == NO_ALBUMS_TO_SHOW_MESSAGE:
            abort(400)
        else:
            abort(422)


@app.route("/albums/<int:albumId>", methods=["DELETE"])
@requires_auth('delete:albums')
def delete_album(payload, albumId):
    try:
        album = Album.query.filter_by(id=albumId).first()
        if album is None:
            raise Exception(NO_ALBUM_FOUND_MESSAGE)
        album.delete()
        return jsonify({
                "success": True,
                "delete": albumId,
            })

    except Exception as e:
        print("\nEXCEPTION get_albums", e, end='\n\n')
        if e.__str__() == NO_ALBUM_FOUND_MESSAGE:
            abort(404)
        else:
            abort(422)


@app.route("/albums/<int:albumId>", methods=["PATCH"])
@requires_auth('patch:albums')
def patch_album(payload, albumId):
    try:
        data = request.get_json()
        newName = None
        if 'newName' in data:
            newName = data['newName']
        if newName is not None:
            album = Album.query.filter_by(id=albumId).first()
            if album is None:
                raise Exception(NO_ALBUM_FOUND_MESSAGE)
            album.name = newName
            album.update()
            return jsonify({
                    "success": True,
                    "albums": [album.getData()]
                })
        else:
            raise Exception(NO_NEW_NAME_IN_PATCH_ALBUM_REQUEST_MESSAGE)

    except Exception as e:
        print("\nEXCEPTION patch_album", e, end='\n\n')
        if e.__str__() == NO_ALBUM_FOUND_MESSAGE:
            abort(404)
        elif e.__str__() == NO_NEW_NAME_IN_PATCH_ALBUM_REQUEST_MESSAGE:
            abort(400)
        else:
            abort(422)


@app.errorhandler(AuthError)
def unauthorized(error):
    return jsonify(
                {
                    "success": False,
                    "error": error.status_code,
                    "message": error.error,
                }
            ), error.status_code


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                "success": False,
                "error": 400,
                "message": "bad request"
            }), 400


@app.errorhandler(405)
def not_found(error):
    return jsonify({
                "success": False,
                "error": 405,
                "message": "method not allowed"
            }), 405
