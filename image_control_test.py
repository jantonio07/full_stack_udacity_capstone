import unittest
import os
from image_control import ImageControl


class ImageControlTests(unittest.TestCase):
    def setUp(self):
        self.ik = ImageControl()

    def testUploadAndDeleteImage(self):
        image_path = os.environ.get('IMAGE_SAMPLE_PATH', 'avatar_1.jpg')
        image = None
        with open(image_path, "rb") as f:
            image = f.read()

        self.assertTrue(image)

        response = self.ik.upload_image(image, image_path)
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
