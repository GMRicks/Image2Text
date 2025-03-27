# app.py
"""
A comprehensive Flask application for an extraordinary image captioning website.
This application uses the pre-trained BLIP model from Hugging Face Transformers
to generate descriptive captions for any uploaded image. The website is designed
with polished aesthetics, smooth transitions, and interactive elements.
"""

from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image
import torch
from transformers import pipeline

app = Flask(__name__)

# Configure the device: use GPU if available, otherwise CPU.
device = 0 if torch.cuda.is_available() else -1

# Load the BLIP image captioning pipeline from Hugging Face.
# Force PyTorch framework to avoid TensorFlow/Keras dependencies.
captioner = pipeline(
    "image-to-text",
    model="Salesforce/blip-image-captioning-base",
    device=device,
    framework="pt"
)

# Global list to store caption history.
caption_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main route for the homepage.
    GET: Renders the homepage with an image upload form and a caption history grid.
    POST: Processes the uploaded image, generates a caption using BLIP, and stores the result.
    """
    if request.method == "POST":
        # Validate file part in the request
        if "image" not in request.files:
            return redirect(request.url)
        file = request.files["image"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            # Save the uploaded file in the static/uploads folder
            filepath = os.path.join("static", "uploads", file.filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            
            # Open the image in RGB (required for BLIP)
            image = Image.open(filepath).convert("RGB")
            
            # Pass the image as a list to treat it as a batch of size 1.
            result = captioner([image])
            
            # Check the structure of the result.
            # Sometimes result[0] is a dict, and sometimes it may be a list containing a dict.
            if isinstance(result, list) and len(result) > 0:
                first_item = result[0]
                if isinstance(first_item, list) and len(first_item) > 0:
                    caption = first_item[0].get("generated_text", "No caption generated.")
                elif isinstance(first_item, dict):
                    caption = first_item.get("generated_text", "No caption generated.")
                else:
                    caption = "No caption generated."
            else:
                caption = "No caption generated."
            
            # Save the result to the caption history.
            caption_history.append({
                "filename": file.filename,
                "caption": caption
            })
            
            return render_template("result.html", caption=caption, filename=file.filename)
    return render_template("index.html", history=caption_history)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    """
    Serves uploaded image files from the static/uploads directory.
    """
    return redirect(url_for("static", filename="uploads/" + filename), code=301)

if __name__ == "__main__":
    # Run the Flask app. You can change host/port as needed.
    app.run(debug=True)
