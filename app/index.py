import pymongo
from flask import Flask, send_file
from flask import request,jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
from io import BytesIO


# connect to the database
myclient =  pymongo.MongoClient("mongodb+srv://txeafrica:txeafrica2023@txe-africa.bn2btt0.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["firstclassmaterial"]
mycul = mydb['users']

# create an app
app = Flask(__name__) 
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


# process image function
def process_image(image_bytes):
    # Remove the background using rembg
    img = Image.open(BytesIO(image_bytes))
    img = img.convert("RGB")
    img = remove(img)

    # Additional processing with pillow
    img.thumbnail((300,300))

    # save and return the process image
    output_io = BytesIO()
    img.save(output_io,format="PNG")
    return output_io.getvalue()




# routes 
# default route
@app.route("/")
def index():
    return jsonify({"message":"Welcome to firstclass material API"}),200


#process image route
@app.route("/remove-bg", methods=['POST'])
def remove_image_route():
    # check if there's image in the client file
    if 'image' not in request.files:
        return jsonify({"message":"No Image Provided"}), 400
    
    image = request.files['image'].read()
    processed_image = process_image(image)
    return send_file(BytesIO(processed_image), mimetype='image/png')






# error Routes
# Custom error handler for 403 Forbidden
@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({
        'error': 'Forbidden', 
        'message': 'You do not have permission to access this resource'
        }), 403

# custom error for not found route
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "message":"Sorry, This page does not exist.",
        "error":"page not found"
        }),404

# custom error for not allowed method
@app.errorhandler(405)
def not_found(error):
    return jsonify({
        "message":"Sorry, This page does not exist.",
        "error":"You do not have permission to perform this operation"
        }),405

# Custom error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'error': 'Internal Server Error', 
        'message': 'Something went wrong on the server',
        }), 500







# run the app
if __name__ == "__main__":
    app.run()
