from flask import (
    Flask,
    url_for,
    render_template,
    request
)

# Архив весил больше, поэтому сдаю ссылку на git
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Миссия Колонизация Марса</h1>"

@app.route('/index')
def index():
    return "<h2>И на Марсе будут яблони цвести!</h2"

@app.route('/promotion')
def promotion():
    lines = ("Человечество вырастает из детства.",
             "Человечеству мала одна планета.",
             "Мы сделаем обитаемыми безжизненные пока планеты.",
             "И начнем с Марса!",
             "Присоединяйся!"
    )
    return "<h2>" + "<br>".join(lines) + "</h1>"

@app.route('/image_mars')
def image_mars():
    return render_template('mars_image.html',
        title="Привет, Марс!",
        path_to_image=url_for('static', filename='img/mars.png')
    )

@app.route('/promotion_image')
def promotion_image():
    return render_template('promotion_image.html',
        title="Колонизация",
        path_to_css=url_for('static', filename='css/style.css'),
        path_to_image=url_for('static', filename='img/mars.png'),
        lines=("Человечество вырастает из детства.",
             "Человечеству мала одна планета.",
             "Мы сделаем обитаемыми безжизненные пока планеты.",
             "И начнем с Марса!",
             "Присоединяйся!"
        )
    )

@app.route('/astronaut_selection', methods=['POST', 'GET'])
def astronaut_selection():
    if  request.method == 'GET':
        return render_template('astronaut_selection_form.html')
    elif request.method == 'POST':
        print(request.form)
        return render_template('astronaut_selection_results.html',
            name=request.form['name'],
            surname=request.form['surname'],
            email=request.form['email'],
            education=request.form.get('education', "Нет"),
            motivation=request.form['motivation'],
            live_on_mars=request.form.get('accept', ''),
            gender=request.form['sex'],
            profession=request.form['profession']
        )

@app.route('/choice/<planet_name>')
def choice_planet(planet_name):
    return render_template('choice_planet.html',
        planet=planet_name,
        path_to_css=url_for('static', filename='css/style.css'),
        lines=(
            "На ней много необходимых ресурсов",
            "На ней есть и вода, и атмосфера",
            "На ней есть небольшое магнитное поле",
            "Она просто красива"
        )
    )

@app.route('/results/<name>/<int:level>/<float:rating>')
def results(name, level, rating):
    return render_template('results.html',
        name=name, level=level, rating=rating
    )

@app.route('/load_photo', methods=['POST', 'GET'])
def load_photo():
    if request.method == 'GET':
        return render_template('load_pic.html',
            path_to_css=url_for('static', filename='css/style.css')
        )
    elif request.method == 'POST':
        f = request.files['file']
        file_name = request.form.get('file', 'form')
        with open(f'static/{file_name}', 'wb') as save_file:
            save_file.write(f.read())
        return render_template('done.html')

@app.route('/carousel')
def carousel():
    images = ['c' + str(i) + '.jpg' for i in range(1, 5)]
    return render_template('carousel.html',
        first_image=url_for('static', filename='img/' + images[0]),
        images=[url_for('static', filename='img/' + image) for image in images[1:]]
    )

if __name__ == "__main__":
    app.run(port=8080)