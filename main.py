from flask import Flask, render_template, request
import requests
import base64
import io
from PIL import Image

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", visibility="hidden")

@app.route('/image', methods=['POST', 'GET'])
def image():
  user_input = request.form['user_prompt']
  API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
  headers = {"Authorization": "Bearer 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"}
  
  def query(payload):
  	response = requests.post(API_URL, headers=headers, json=payload)
  	return response.content
  image_bytes = query({
  	"inputs": user_input,
  })

  # opens and stores the image in memory
  image = Image.open(io.BytesIO(image_bytes))
  buffered = io.BytesIO()
  image.save(buffered, format="JPEG")
  encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
  
  return render_template("index.html", visibility="visible", encoded_image=encoded_image, user_input=user_input)


if __name__ == '__main__':
    app.run(debug=True)
