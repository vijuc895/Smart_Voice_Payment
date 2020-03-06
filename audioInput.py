import os
import inspect
import subprocess
from flask import Flask, Response

@app.route('/playaudio')
def playaudio():
    sendFileName=""
    def generate():

        #  get_list_all_files_name this function gives all internal files inside the folder

        filesAudios=get_list_all_files_name(currentDir+"/streamingAudios/1")

        # audioPath is audio file path in system
        for audioPath in filesAudios:
            data=subprocess.check_output(['cat',audioPath])
            yield data
    return Response(generate(), mimetype='audio/mp3')