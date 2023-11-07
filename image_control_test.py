import unittest
import os
from ImageControl import ImageControl
from base64 import b64encode

class ImageControlTests(unittest.TestCase):
    def setUp(self):
        self.ik = ImageControl()

    def testUploadAndDeleteImage(self):
        image_path = os.environ.get('IMAGE_SAMPLE_PATH', '../21k.jpeg')
        image = None
        with open(image_path, "rb") as f:
            image = b64encode(f.read())
        self.assertTrue(image)

        response = self.ik.upload_64_encoded_image(image, image_path)
        self.assertTrue(response['success'])
        self.assertTrue(response['metadata'])
        self.assertTrue(response['metadata']['fileId'])

        imageId = response['metadata']['fileId']
        response = self.ik.delete_image(imageId)
        self.assertTrue(response['success'])
        self.assertFalse(response['metadata'])

        response = self.ik.delete_image(imageId)
        self.assertFalse(response['success'])
        self.assertTrue(response['message'])

if __name__ == "__main__":
    unittest.main()