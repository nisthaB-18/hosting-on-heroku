from flask import Flask, jsonify, request
from encode import Encode
from decode import Decode
import base64
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the encode and decode app'

@app.route('/encode', methods=['POST'])
def encode_text():
    try:
        # Extract input for text_to_encode, image and password used to hide secret message from user
        text_to_encode = request.json.get('text_to_encode')
        password = request.json.get('password')
        image_path = request.json.get('image_path')

        if not text_to_encode or not password :
            raise ValueError("error! text or password missing")
        else:
            if  not image_path:
                raise ValueError("error! select image")

        # Decode the base64-encoded image data
        image_path = base64.b64decode(image_path)
        
        # Save the image data to a temporary file
        image_file = 'temp_image.png'
        with open(image_file, 'wb') as f:
            f.write(image_path)

        # Create an object of the Encode class defined in encode.py
        encoding = Encode(image_path,password,text_to_encode)

        # Call the encode_text method with the path to the temporary image file
        encoded_image = encoding.encode_into_image()
        encoded_image[0].save('saved.png')
        # Encode the resulting image as base64 and return it
        with open('./saved.png', "rb") as f:
            encoded_image_path = base64.b64encode(f.read())
        os.remove(image_file)  # Remove the temporary file
        response =  jsonify({'encoded_image': encoded_image_path.decode()})
        response.status_code = 200
        return response
    except (FileNotFoundError, ValueError) as e:
        response =  jsonify({'error': str(e)})
        response.status_code = 200
        return response

@app.route('/decode', methods=['POST'])
def decode_text():
    try:
        # Extract input for image and password to decode the message from user
        password = request.json.get('password')
        image_path = request.json.get('image_path')

        if not password :
            raise ValueError("error! enter password")
        else:
            if not image_path:
                    raise ValueError("error! select your image ")

        # Decode the base64-encoded image data
        image_path = base64.b64decode(image_path)

        # Save the image data to a temporary file
        image_file = 'temp_image.png'
        with open(image_file, 'wb') as f:
            f.write(image_path)

        # Create an object of the Decode class defined in decode.py
        decoding = Decode(image_path,password)

        # Call the decode_text method with the path to the temporary image file
        decoded_text = decoding.decode_from_image()

        os.remove(image_file)  # Remove the temporary file
        response =  jsonify({'decoded_text': decoded_text})
        response.status_code= 200
        return response
    except (FileNotFoundError, ValueError) as e:
        response  = jsonify({'error': str(e)})
        response.status_code = 200
        return response
    

if __name__ == '__main__':
    app.run(debug=True)