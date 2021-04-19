from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index2.html')


@app.route('/tmp', methods=['GET', 'POST'])
def tmp():
    value = {"xcode": 33.450705,
             "ycode": 126.570677}

    bus_stop = {"카카오": {"xcode": 33.450705, "ycode": 126.570677},
                "생태연못": {"xcode": 33.450936, "ycode": 126.569477},
                "텃밭": {"xcode": 33.450879, "ycode": 126.56994},
                "근린공원": {"xcode": 33.451393, "ycode": 126.570738}}
    return render_template('index3.html', value=value, bus_stop=bus_stop)


@ app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template("test.html", prediction=result)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
