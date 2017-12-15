from flask import Flask, request, render_template, jsonify, redirect, flash, Response
from werkzeug.utils import secure_filename
import boto3
from helpers import *
from config import *
from converter import *

app = Flask(__name__)
app.config.from_object('config')

ALLOWED_EXTENSIONS = set(['eps'])

s3resource = boto3.resource(
	"s3",
	aws_access_key_id=S3_KEY,
	aws_secret_access_key=S3_SECRET
	)

client = boto3.client(
	"s3",
	aws_access_key_id=S3_KEY,
	aws_secret_access_key=S3_SECRET
	)

bucket_res = s3resource.Bucket('epsconverter')

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
	if request.method=='POST':
		print("Attempting Post")
		# Case A, check that the file input key is there
		if "user_file" not in request.files:
			return "No user_file key in request.files"

		# Case B, if the key is there, save it
		file = request.files["user_file"]

		# Case C, make sure there is a file
		if file.filename == "":
			return "Please select a file"

		# Case D, check if authorized
		if file and allowed_file(file.filename):
			file.filename = secure_filename(file.filename)
			output = upload_file_to_s3(file, app.config["S3_BUCKET"])
			file_loc = str("{}{}".format(app.config["S3_LOCATION"], file.filename))
			flash('Upload successful!')
			
			#download and convert the uploaded eps file
			if not os.path.isdir("tmp"):
				os.mkdir('tmp')
			#Download the file corresponding with the URL
			bucket_res.download_file(file.filename, f'tmp/{file.filename}')
			new_filename, new_filename_address = convert_to_png()
			bucket_res.upload_file(new_filename_address, new_filename)
			
			download_file = client.get_object(Bucket=app.config["S3_BUCKET"], Key=new_filename)
			
			return Response(
				download_file['Body'].read(),
				mimetype='image/png',
				headers={"Content-Disposition": f"attachment;filename={new_filename}"}
				)

		else:
			return redirect("/upload")
	else:
		return render_template('upload.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True, port=4999)