import os
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
# from preprocessAudio import split_into_5
from subprocess import Popen, PIPE
from preprocessAudio import split_into_5,remove_noise_silence
import os
from automateTrain import addUser
import subprocess
import speech_recognition as sr
import pandas as pd
ALLOWED_EXTENSIONS = set(['wav'])

df=pd.DataFrame({"Account Holder":['Vijender',"Shuvam","Anshaj","Shubham","Harsh"],"Balance":[1000,2000,1500,1300,1200]})
print(df.head())
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def data(speaker,text):
    account_holder=['Vijender',"Shuvam","Anshaj","Shubham","Harsh"]
    account_To_deduct=speaker
    amount_to_deduct=[int(s) for s in text.split() if s.isdigit()]
    if(amount_to_deduct!=[]):
        amount_to_deduct=amount_to_deduct[0]
    account_to_credit=" "
    print(text.split(" ")[1:])
    account_holder.remove(speaker)
    for i in text.split(" ")[1:]:
        if i in account_holder:
            account_to_credit=i
        if(amount_to_deduct==[] and i in ["hundred","ten","twenty","fifty"]):
            amount_to_deduct=100

    df.loc[df['Account Holder'] == account_To_deduct, 'Balance'] -= amount_to_deduct
    df.loc[df['Account Holder'] == account_to_credit, 'Balance'] += amount_to_deduct
    print(df)
    return account_To_deduct+" will pay "+str(amount_to_deduct)+"Rs to "+account_to_credit

def predict_speaker(filename):
    file_path = os.path.join(os.getcwd(), filename)

    p = Popen(["python2", "tester.py", file_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    speaker_name, err = p.communicate()
    if err:
        print(err)
    speaker_name = speaker_name.decode().strip()
    return speaker_name

@app.route('/upload.html', methods=['POST'])
def register():
    return render_template('upload.html')

@app.route('/verify.html', methods=['POST'])
def verify():
    return render_template('verify.html')


@app.route('/')
def upload_form():
    return render_template('home.html',tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = str(filename).split(".")[1]
            filename = request.form['username']
            path="./train_data/"+filename
            os.mkdir(path)
        

            file.save(os.path.join(path, filename + "." + file_ext))
            flash('File successfully uploaded')
            split_into_5(filename)
            addUser(filename)
            return redirect('/')
        else:
            flash('Allowed file types are wav.')
            return redirect(request.url)



@app.route('/verify', methods=['POST'])
def verify_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file:
            filename = file.filename
            
            print(filename)
            path="./test_data/"
            '''remove_noise_silence(path+filename)'''
            file.save(os.path.join(path, filename))
            '''filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))'''
            speaker = predict_speaker(path+filename)
            speaker=filename.split('.')[0]
            # initialize the recognizer
            r = sr.Recognizer()

            # open the file
            with sr.AudioFile(path+filename) as source:
                # listen for the data (load audio to memory)
                audio_data = r.record(source)
                # recognize (convert from speech to text)
                text = r.recognize_google(audio_data)
            
            msg=data(speaker,text)
            
            
            return render_template('verify.html', result=speaker,text1=text,text=msg,  tables=[df.to_html(classes='data')], titles=df.columns.values)
        else:
            flash('Allowed file types are wav.')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
