from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from base64 import b64encode
from pprint import pprint
import os
import functools


class ImageControl():
    def __init__(self):
        self.PRIVATE_KEY = os.environ.get('IMAGEKIT_PRIVATE_KEY', '')
        self.PUBLIC_KEY = os.environ.get('IMAGEKIT_PUBLIC_KEY', '')
        self.URL_ENDPOINT = os.environ.get('IMAGEKIT_URL_ENDPOINT', '')

        PRIVATE_KEY_MESSAGE = "Please set ImageKit PRIVATE_KEY \
            as environment variable"
        PUBLIC_KEY_MESSAGE = "Please set ImageKit PUBLIC_KEY \
            as environment variable"
        URL_ENDPOINT_MESSAGE = "Please set ImageKit URL_ENDPOINT \
            as environment variable"
        assert len(self.PRIVATE_KEY) > 0, PRIVATE_KEY_MESSAGE
        assert len(self.PUBLIC_KEY) > 0, PUBLIC_KEY_MESSAGE
        assert len(self.URL_ENDPOINT) > 0, URL_ENDPOINT_MESSAGE

        self.imagekit = ImageKit(
            private_key=self.PRIVATE_KEY,
            public_key=self.PUBLIC_KEY,
            url_endpoint=self.URL_ENDPOINT
        )

    def makes_request_to_imagekit(function):
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            try:
                response = function(self, *args, **kwargs)
                status_code = response.response_metadata.http_status_code
                return {
                    "success": status_code == 200 or status_code == 204,
                    "metadata": response.response_metadata.raw,
                }
            except Exception as e:
                print("\nIMAGEKIT_EXCEPTION:", e, end='\n\n')
                return {
                    "success": False,
                    "message": e,
                }
        return wrapper

    @makes_request_to_imagekit
    def upload_64_encoded_image(self, encodedImage, image_name):
        options = UploadFileRequestOptions(is_private_file=False)
        return self.imagekit.upload_file(
            file=encodedImage,
            file_name=image_name,
            options=options
        )

    def upload_image(self, image, image_name):
        encodedImage = b64encode(image)
        return self.upload_64_encoded_image(encodedImage, image_name)

    @makes_request_to_imagekit
    def delete_image(self, image_id):
        return self.imagekit.delete_file(file_id=image_id)


if __name__ == '__main__':
    image_path = os.environ.get('IMAGE_SAMPLE_PATH', '../21k.jpeg')
    image = None
    with open(image_path, "rb") as f:
        image = f.read()
    assert image is not None, "Make sure to specify the image path!"

    image_control = ImageControl()

    response = image_control.upload_image(image, "21k.jpeg")
    pprint(response)
    file_id = response['metadata']['fileId']

    # response = image_control.delete_image(file_id)
    # pprint(response)

    '''
    image_url = image_control.imagekit.url({
        "path": "/image_6P3QUg775.jpeg",
        "transformation": [{
            "height": "320",
            "width": "320",

        }],
        "signed": True,
        "expire_seconds": 30
    })
    print(image_url)
    '''
