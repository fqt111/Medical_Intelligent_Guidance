import jieba
import fasttext
from gevent import pywsgi
from flask import Flask, render_template, request
import csv

app = Flask(__name__)
classifier = fasttext.load_model("model.bin")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    
    userText = request.args.get('msg')
    print('userText',userText)
    input_line = " ".join( list( jieba.cut(userText) ) )
    print('input_line',input_line)
    print(classifier.predict([input_line]))
    response = classifier.predict([input_line])[0][0][0]
    print(response)
    recommend_keshi = response[response.find("__label__")+len("__label__"):] 
    print("推荐您到 "+ recommend_keshi + "就诊")

    payload = []
    content = {}
    with open("newdata.csv", "r", encoding="utf-8") as csvFile:
        reader = csv.reader(csvFile)
        for info in reader:
            intro = list(info);
            if len(intro) != 0 and len(payload) != 3:
                (name, title, hospital, keshi, introduction) = intro[0], intro[1], intro[2], intro[3], "".join(
                    intro[4:]);
                if (keshi == recommend_keshi):
                    content = {'name': name, 'position': title, 'hospital': hospital,
                               'department': keshi, 'good_at': introduction}
                    payload.append(content)
                    content = {}
    for info in payload:
        print(info);

    return "推荐您到: "+ recommend_keshi + "，点击[挂号]，一键直达。"

if __name__ == "__main__":
    app.run()
