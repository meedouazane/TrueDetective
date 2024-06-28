#!/usr/bin/python3
"""
app module
"""
from flask import Flask, request, jsonify, render_template, send_from_directory
from gtts import gTTS
from Traitement.Speech2Text import extract_audio_from_youtube, speech_to_text
from Traitement.zephyrChat import check
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.template_folder = 'web/'


@app.route('/translate', methods=['POST'], strict_slashes=False)
def translate_vid():
    """ Extracting audio from YouTube videos and translate it """
    url = request.form.get('url')
    local_file = request.form.get('path')
    if not url and not local_file:
        return jsonify({"error": "Url or Path parameters are required"}), 400
    try:
        if url:
            file = {"file": open(extract_audio_from_youtube(url), "rb")}
            text = speech_to_text(file, translate=True)
        else:
            file = {"file": open(extract_audio_from_youtube(local_file), "rb")}
            text = speech_to_text(file, translate=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    myobj = gTTS(text=text, lang='en', slow=False)
    if url:
        myobj.save("./Translated_Audio/myAudio.mp3")
        return jsonify({"Result": text})
    else:
        myobj.save("./Translated_Audio/Audio.mp3")
        return jsonify({"Result": text})


@app.route('/convert', methods=['POST'], strict_slashes=False)
def convert_vid():
    """ Convert video to mp3 file """
    url = request.form.get('url')
    if not url:
        return jsonify({"error": "Url or Path parameters are required"}), 400
    try:
        file = {"file": open(extract_audio_from_youtube(url), "rb")}
        if file:
            return jsonify({"Path": "/tmp_Audio/myAudio.mp3"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/check', methods=['POST'], strict_slashes=False)
def check_vid():
    """ processing fact-check """
    url = request.form.get('url')
    local_file = request.form.get('path')
    if not url and not local_file:
        return jsonify({"error": "Url or Path parameters are required"}), 400
    try:
        if url:
            file = {"file": open(extract_audio_from_youtube(url), "rb")}
            text = speech_to_text(file)
            result = check(text)
        else:
            file = {"file": open(extract_audio_from_youtube(local_file), "rb")}
            text = speech_to_text(file)
            result = check(text)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"checking pdf file": "/tmp_Result/",
                    "Result": result})


@app.route('/Translated_Audio/myAudio.mp3')
def mp3_file():
    """ Route to serve mp3 file """
    filename = 'myAudio.mp3'
    return send_from_directory('Translated_Audio/', filename)


@app.route('/tmp_Audio/myAudio.mp3')
def mp3_convert():
    """ Route to serve mp3 file """
    filename = 'myAudio.mp3'
    return send_from_directory('tmp_Audio/', filename)


@app.route('/tmp_Result/translation.pdf')
def pdf_file():
    """ Route to serve pdf file """
    filename = 'translation.pdf'
    return send_from_directory('tmp_Result/', filename)


@app.route('/tmp_Result/checking.pdf')
def pdf_file_checking():
    """ Route to serve pdf file of fact-check """
    filename = 'checking.pdf'
    return send_from_directory('tmp_Result/', filename)


@app.route('/web/images/logo.png')
def serve_jpg():
    """ Route to serve jpg file """
    filename = 'logo.png'
    return send_from_directory('web/images/', filename)


@app.route('/', strict_slashes=False)
def index():
    """ The main page"""
    return render_template('index.html')


@app.route('/web/styles/style.css')
def serve_css():
    """ Route to serve css file """
    filename = 'style.css'
    return send_from_directory('web/styles/', filename)


@app.route('/web/scripts/main_page.js')
def serve_script():
    """ Route to serve script file """
    filename = 'main_page.js'
    return send_from_directory('web/scripts/', filename)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
