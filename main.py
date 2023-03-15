from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = 'timkarazvod'

@app.route('/')
def index():
    return render_template('base.html')


def main():
    app.run()


if __name__ == '__main__':
    main()
