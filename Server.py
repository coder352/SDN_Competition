#!/usr/bin/python
# coding: utf-8

from flask import Flask
from flask import request
from Network import Network

app = Flask(__name__)


@app.route('/test', methods=['GET', 'POST'])
def home():
    network.draw()
    return '<h1>Home</h1>'

if __name__ == '__main__':
    network = Network()
    network.start()
    app.run()
