
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html') 

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request['username']
    password = request['password']
    #if username == 'admin' and password  == 'password':
    #return render_template('signin-ok.html', username="zhouwei")
    return render_template('form.html', username='zhouwei')

if __name__ == '__main__':
    app.run()

