# Important imports
from app import app
from flask import request, render_template, url_for
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import EfficientNetB7, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import string
import random
import os

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

# Loading model
model = EfficientNetB7(weights='imagenet')

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():
	# Execute if request is GET
	if request.method == "GET":
		full_filename = 'images/white_bg.jpg'
		return render_template("index.html", full_filename=full_filename)

	# Execute if request is POST
	if request.method == "POST":
		try:
			# Generating unique image name
			letters = string.ascii_lowercase
			name = ''.join(random.choice(letters) for i in range(10)) + '.png'
			full_filename = 'uploads/' + name

			# Reading, resizing, saving and preprocessing image for prediction
			image_upload = request.files['image_upload']
			imagename = image_upload.filename
			image = Image.open(image_upload)
			image = image.resize((600, 600))
			image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))
			image_arr = np.array(image.convert('RGB'))
			image_arr.shape = (1, 600, 600, 3)

			# Predicting output
			result = model.predict(preprocess_input(image_arr))
			decoded_result = decode_predictions(result, top=1)[0][0]
			prediction = decoded_result[1]
			confidence = decoded_result[2]

			# Returning template, filename, and prediction
			return render_template('index.html', full_filename=full_filename, pred=prediction, confidence=confidence)

		except Exception as e:
			full_filename = 'images/white_bg.jpg'
			return render_template('index.html', full_filename=full_filename,pred='Please Upload an Image',error='An error occurred while processing the request')


# Main function
if __name__ == '__main__':
    app.run(debug=True)
