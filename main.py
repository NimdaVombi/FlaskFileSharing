from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import datetime
import config
app = Flask(__name__)
# Specify the directory where uploaded files will be stored
UPLOAD_FOLDER = config.upload_folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def log_event(event):
    if config.log_events:
        with open('logs.txt', 'a') as log_file:
            log_file.write(f"{datetime.datetime.now()}: {event}\n")

@app.route('/')
def index():
    # List files in the "uploads" directory
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        log_event(f"File uploaded: {file.filename}")
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    # Change the host to '0.0.0.0' to listen on all network interfaces
    app.run(debug=True, host=config.host, port=config.port)
