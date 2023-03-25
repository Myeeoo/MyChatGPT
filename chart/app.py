from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/train', methods=['POST'])
def train():
    subprocess.Popen(['python3', 'train.py'])
    return render_template('training.html')

if __name__ == '__main__':
    app.run(debug=True)
