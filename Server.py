#!/usr/bin/python
# coding: utf-8

from flask import Flask
from flask import request
from flask import render_template
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required
from Network import Network

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jrp'


# # 处理 路径请求的表单
# class PathCreate(Form):
#     # api = StringField("api", [Required()])
#     # submit = SubmitField("Submit")
#     # alias = StringField("alias for api")
#     def __init__(self):
#         self.src = IntegerField("src[0]")
#         self.dst = IntegerField("dst[0]")
#         print type(self.src)
#         print dir(self.src)
#     # dst = StringField("dst[0]")
#         print "##########################################################"


@app.route("/getpath", methods=['GET', 'POST'])
def getpath():
    src = int(str(request.args.get('src', '')))
    dst = int(str(request.args.get('dst', '')))
    path = network.findPath(src, dst)
    return str(path)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")
    # return render_template("topo_left.html")
    # return render_template("ajax_index2.html")


@app.route('/draw', methods=['GET', 'POST'])
def draw():
    network.draw()
    return network.findPath(fo, to)

if __name__ == '__main__':
    network = Network()
    network.start()
    app.run()
