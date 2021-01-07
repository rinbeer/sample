import os
import sqlite3
import datetime
import string
import speech_recognition as sr
import json
from pydub import AudioSegment

from flask import Flask , render_template , request , redirect , session ,jsonify
app = Flask(__name__)
app.secret_key = 'honyaku'


UPLOAD_FOLDER = './static/audio'
UPLOAD_FOLDER_DELITE = './static/audio/*'


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/submit", methods=["POST"])
def submit():
  time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
  # 音声データをファイルに格納
  upload = request.files['upload']
  filename = upload.filename
  upload.save(os.path.join(UPLOAD_FOLDER,filename))
  print(filename)
  # return render_template('index.html')

  length = request.form.get("length")
  print(length)


  audio_pass = "./static/audio/"+ filename



  # wavファイルの読み込み
  sound = AudioSegment.from_file(audio_pass, format="wav")



  # リセット
  with open('./static/honyaku/honyaku_text.txt','w')as f:
    f.write("<start>"+time+"\n")


  """ここから音声分割スタート"""
  n = 0
  m = 0

  # nの右側は１秒1000でカウント（例：１h = 3600000）
  while n <= int(length)*60000: 
    sounds = sound[n:n+30000]
    n = n+30000
    m = m+1
    sounds.export("./static/audio/audio("+str(m)+").wav", format='wav')
    print(sound)



  """ここから翻訳・テキスト出力スタート"""
  r = sr.Recognizer()
  for l in range(1,m):
    with sr.AudioFile("./static/audio/audio("+ str(l) +").wav") as source:
      audio = r.record(source)
  # 日本語テキスト化
    text = r.recognize_google(audio, language='ja-JP')
  # 文字の出力(ターミナル画面)
    print(text)
  # 文字をテキストファイルに起こす
    with open('./static/honyaku/honyaku_text.txt','a')as f:
      if m%5 == 0:
        f.write("<5min>"+"\n")
      f.write(text + "\n\n")

  print("end")

  return render_template('return.html')


@app.route('/submit_record', methods=['POST'])
def uploaded_wav():
  fname = "sounds/" + datetime.now().strftime('%m%d%H%M%S') + ".wav"
  with open(f"{fname}", "wb") as f:
    f.write(request.files['data'].read())
  print(f"posted sound file: {fname}")
  return jsonify({"data": fname})

  # os.remove('./static/honyaku/honyaku_text.txt')
  # os.remove(UPLOAD_FOLDER_DELITE)


if __name__ == "__main__":
    app.run(debug = True)



