from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)


@app.route('/')
def index():
    """
    Render the index.html template.

    Returns:
        str: Rendered HTML page.
    """
    return render_template('index.html')


@app.route('/encode', methods=['POST'])
def encode():
    """
    Encode a message into an image.

    Returns:
        file: Encoded image file.
    """
    image_file = request.files['image']
    message = request.form['message']
    image = Image.open(io.BytesIO(image_file.read()))

    encoded_image = encode_image(image, message)
    encoded_image_io = io.BytesIO()
    encoded_image.save(encoded_image_io, format='PNG')
    encoded_image_io.seek(0)

    return send_file(encoded_image_io, as_attachment=True, download_name='encoded_image.png', mimetype='image/png')


def encode_image(image, message):
    """
    Encode a message into an image.

    Args:
        image (PIL.Image.Image): Image to encode the message into.
        message (str): Message to encode.

    Returns:
        PIL.Image.Image: Encoded image.

    Raises:
        ValueError: If the image is too small to encode the message.
    """
    encoded_image = image.copy()

    binary_message = ''.join(format(ord(c), '08b') for c in message)

    # Add stop marker to the binary message to indicate the end of the message
    binary_message += '1111111111111110'  # Stop marker

    data_index = 0
    for x in range(encoded_image.width):
        for y in range(encoded_image.height):
            pixel = list(encoded_image.getpixel((x, y)))
            for i in range(3):
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    data_index += 1
            encoded_image.putpixel((x, y), tuple(pixel))
            if data_index >= len(binary_message):
                return encoded_image

    raise ValueError("Image is too small to encode the message")


def decode_image(image):
    """
    Decode a message from an image.

    Args:
        image (PIL.Image.Image): Image to decode the message from.

    Returns:
        str: Decoded message.
    """
    decoded_message = ""
    binary_message = ""
    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            for i in range(3):
                binary_message += str(pixel[i] & 1)
                if len(binary_message) == 8:
                    if binary_message == '11111111':  # Stop marker
                        return decoded_message
                    decoded_message += chr(int(binary_message, 2))
                    binary_message = ""
    return decoded_message


@app.route('/decode', methods=['POST'])
def decode():
    """
    Decode a message from an image.

    Returns:
        str: Decoded message.
    """
    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read()))

    decoded_message = decode_image(image)

    return render_template('index.html', decoded_message=decoded_message)


if __name__ == '__main__':
    app.run(debug=True)
