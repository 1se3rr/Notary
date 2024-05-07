from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/notarial_acts")
def notarial_acts():
    return render_template('notarial_acts.html')


@app.route("/tariffs")
def tariffs():
    return render_template('tariffs.html')


@app.route("/about_us")
def about_us():
    return render_template('about_us.html')


@app.route("/contact_us")
def contact_us():
    return render_template('contact_us.html')


@app.route("/FAQ ")
def FAQ():
    return render_template('FAQ.html')




if __name__ == '__main__':
    app.run()

