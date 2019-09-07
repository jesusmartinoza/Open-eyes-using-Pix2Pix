from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from keras.models import load_model
import cv2
import numpy as np
import tensorflow as tf
from FacePatcher import FacePatcher
import uuid

# load model
def get_model():
    global graph
    graph = tf.get_default_graph()
    with graph.as_default():
        global model
        model = load_model('model.h5')

app = Flask(__name__)
get_model()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_image():
    with graph.as_default():
        if request.method == 'POST':
            print(request.files)
            response = {'success': True}

            # Check if the request has images
            if 'input_image' not in request.files:
                response['success'] = False
                response['message'] = 'No input file provided'
            if 'target_image' not in request.files:
                response['success'] = False
                response['message'] = 'No target file provided'

            if not response['success']:
                return jsonify(response)

            # Patch image
            try:
                fp = FacePatcher(is_test = False)
            except ValueError as err:
                response['message'] = err
                return jsonify(response)

            fp.load_from_files(request.files['input_image'], request.files['target_image'])
            patching_result = fp.result

            # Prepare image for model
            patching_result = tf.cast(patching_result, tf.float32)
            resized = tf.image.resize(patching_result, [256, 256])
            normalized = (resized / 127.5) - 1
            batched = tf.expand_dims(normalized, 0)

            # Apply model! :D
            predicted = model.predict(batched, steps=1)
            predicted = predicted[0,:,:,:]

            unnormalized = (predicted + 1) / 2

            # Save result on disk to eventually show to user
            result_name = 'static/tmp/{}.jpg'.format(uuid.uuid4())
            cv2.imwrite(result_name, unnormalized * 255)

            response['processed_image'] = result_name
            return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)