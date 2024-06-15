from flask import Flask, request, render_template, redirect, url_for
import json
from precrawl import *

app = Flask(__name__, static_folder='./static')
star = ''
lion = ''

@app.route('/', methods=['GET'])
def StarT():
    global star
    return render_template('star.html', cities=star.city)

@app.route('/lion', methods=['GET'])
def LionT():
    global lion
    return render_template('lion.html', infos=lion.infos)
    


if __name__ == '__main__':
    star = Starlux(1, 's_html_src.txt')
    star.getCity()
    lion = Lion(1, 'l_html_src.txt')
    lion.getInfo()
    app.run(debug=True, port=5000)
