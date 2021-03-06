import gevent.monkey
import gevent
gevent.monkey.patch_all()
from gevent.pywsgi import WSGIServer
from deep_ovel import DeepOVel
import werkzeug
from flask import send_from_directory, abort
from flask import Flask, flash, request, redirect, render_template
from markupsafe import escape
import os
import time
from datetime import datetime

app = Flask(__name__)
app.uploadVideoName = ""
app.CamTilt = 0
app.CamHeight = 0
app.CamFov = 0
app.VelScale = 0
app.VertImageDim = -1  # vertical dimension of 35 mm image format which can be found from camera specifications.
app.CamFocalLength = -1  # focal length of the camera
app.StartTime = 0
app.VideoDuration = -1


app.deepOVel = DeepOVel()

app.config.from_object("app_config.TestingConfig")

if app.config["ENV"] == "production":
    app.config.from_object("app_config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("app_config.TestingConfig")
else:
    app.config.from_object("app_config.DevelopmentConfig")


def show_time():
    now = datetime.now().strftime("%A %d, %B %Y  %H:%M:%S")
    return str(f"{escape(now)}")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try:
        lst = os.listdir(path)
    except OSError:
        pass  # ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree


def dirtree():
    path = os.path.expanduser(u'~')
    return render_template('dirtree.html', tree=make_tree(path))


@app.route('/processing_done/<filename>')
def processing_done(filename):
    print(filename)
    return render_template("client/processing_done.html", filename=filename)


@app.route("/download/<filename>")
def download(filename):
    try:
        folder = app.config["DOWNLOAD_FOLDER"]
        print(f"Download folder: {folder}")
        return send_from_directory(folder, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/static/')
def dirtree():
    path = os.path.join(os.getcwd(), 'static')
    return render_template('client/dirtree.html', tree=make_tree(path))


@app.route('/get_status')
def get_status():
    yolo_progress, vel_progress = app.deepOVel.GetProgress()
    progress_str = str(yolo_progress) + ',' + str(vel_progress)
    if(app.deepOVel.IsRunning):
        return progress_str
    else:
        return redirect('/')


@app.route('/processing_file/<video_name>', methods=['GET', 'POST'])
def process_file(video_name):
    if request.method == 'GET':
        app.uploadVideoName = video_name
        return render_template('client/processing_video_msg.html', filename=video_name)

    if request.method == 'POST':
        full_upload_video_name = werkzeug.utils.safe_join(app.config['UPLOAD_FOLDER'], app.uploadVideoName)

        print(
            f"Selected Params:  Tilt: {app.CamTilt}, height: {app.CamHeight}, scale: {app.VelScale}, FOV: {app.CamFov}, v: {app.VertImageDim}, f: {app.CamFocalLength}")
        # if(not app.DeepOVel.IsRunning):
        app.deepOVel = DeepOVel()
        app.deepOVel.SetCameraParams(app.CamTilt, app.CamHeight, app.CamFov, app.CamFocalLength, app.VertImageDim)
        app.deepOVel.SetVelCalibarion(app.VelScale)
        download_video_name = app.deepOVel.Run(full_upload_video_name, app.config['DOWNLOAD_FOLDER'], app.VideoDuration, app.StartTime)
        filename = os.path.basename(download_video_name)
        return filename
    return render_template('client/processing_video_msg.html', filename=video_name)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        app.CamTilt = float(escape(request.form['CamTilt']))
        app.CamHeight = float(escape(request.form['CamHeight']))
        app.VelScale = float(escape(request.form['VelScale']))

        app.CamFov = float(escape(request.form['CamFov']))
        app.VertImageDim = float(escape(request.form['VertImageDim']))
        app.CamFocalLength = float(escape(request.form['CamFocalLength']))

        app.StartTime = float(escape(request.form['StartTime']))
        app.VideoDuration = float(escape(request.form['VideoDuration']))

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            video_name = werkzeug.utils.secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)
            full_upload_name = werkzeug.utils.safe_join(app.config['UPLOAD_FOLDER'], video_name)
            file.save(full_upload_name)
            return redirect('/processing_file/' + video_name)

    return render_template("client/file_upload_page.html")


if __name__ == "__main__":
    print(f'ENV is set to: {app.config["ENV"]}')
    # app.run(debug=True)
    http_server = WSGIServer((app.config["HOST_IP"], app.config["PORT"]), app)
    http_server.serve_forever()
