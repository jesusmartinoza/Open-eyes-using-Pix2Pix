from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        print(request.files)
        response = {success: True}

        # check if the post request has the images
        if 'input_image' not in request.files:
            response['success'] = False
            response['message'] = 'No input file provided'
        if 'target_image' not in request.files:
            response['success'] = False
            response['message'] = 'No target file provided'

        if not response.success:
            return jsonify(response)

        input_file = request.files['input_image']
        target_file = request.files['target_image']

        return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)