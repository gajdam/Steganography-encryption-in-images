import unittest
from PIL import Image
from main import encode_image, decode_image


class TestSteganography(unittest.TestCase):
    def setUp(self):
        # Create a sample image for testing
        self.image = Image.new('RGB', (100, 100), color='white')

    def test_encode_decode_message(self):
        # Test encoding and decoding a message
        message = "This is a test message"
        encoded_image = encode_image(self.image, message)
        decoded_message = decode_image(encoded_image)
        self.assertEqual(decoded_message, message)

    def test_decode_empty_image(self):
        # Test decoding an empty image
        empty_image = Image.new('RGB', (100, 100), color='white')
        decoded_message = decode_image(empty_image)
        self.assertEqual(decoded_message, "")

    def test_encode_message_too_large(self):
        # Test encoding a message that is too large for the image
        image = Image.new('RGB', (10, 10), color='white')
        message = "This message is too large for the image"
        with self.assertRaises(ValueError):
            encode_image(image, message)


if __name__ == '__main__':
    unittest.main()
