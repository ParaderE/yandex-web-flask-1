import os
import json
from random import choice

from werkzeug.utils import secure_filename
from flask import (
    Flask,
    url_for,
    render_template,
    request,
    redirect
)

from forms import (
    LoginForm,
    ImageForm,
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['IMAGES'] = 5


@app.route('/<title>')
@app.route('/index/<title>')
def home(title="Mars"):
    return render_template('base.html',
                           title=title)


@app.route('/training/<prof>')
def prof_training(prof: str):
    prof = prof.lower()
    profession = ""
    image = "ship.jpg"
    if prof == "врач":
        profession = "Научные симуляторы"
        image = "scn_ship.jpg"
    elif "инжинер" in prof or "строитель" in prof:
        profession = "Инжинерные тренажёры"
        image = "ing_ship.jpg"
    return render_template('training.html',
                           profession=profession,
                           image=url_for('static', filename='img/' + image))


@app.route('/list_prof/<list_type>')
def list_prof(list_type):
    professions = (
        "инженер-исследователь",
        "пилот",
        "экзобиолог",
        "врач",
        "инженер по терраформированию",
        "климатолог",
        "специалист по радиационной защите",
        "астрогеолог",
        "гляциолог",
        "инженер жизнеобеспечения",
        "метеоролог",
        "оператор марсохода",
        "киберинженер",
        "штурман",
        "пилот дронов",
    )
    return render_template('list.html',
                           list_type=list_type,
                           professions=professions)


@app.route('/answer', methods=['POST', 'GET'])
@app.route('/auto_answer', methods=['POST', 'GET'])
def answer():
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('index')
    return render_template('login.html',
                           form=form)


@app.route('/distrebtion')
def distrebution():
    return render_template('distrebution.html', astronauts=astronauts)


@app.route('/table_param/<gender>/<int:age>')
def table_param(gender: str, age: int):
     return render_template('table_param.html',
                            age=age,
                            gender=1 if gender == "male" else 0,
                            image=url_for('static', filename=f'img/{gender}_{1 if age > 21 else 2}.jpg'))


@app.route('/carousel', methods=['POST', 'GET'])
def carousel():
    form = ImageForm()
    if form.validate_on_submit():
        i = form.image.data
        filename = secure_filename(i.filename)
        with open('static/img/carousel/' + filename, 'wb') as f:
            f.write(i.read())
        app.config['IMAGES'] += 1
        return redirect('carousel')
    images = os.listdir('static/img/carousel/')
    return render_template('carousel.html',
        images=[url_for('static', filename='img/carousel/' + image) for image in images],
        form=form
    )


@app.route('/member')
def member():
    with open('templates/members.json') as members_file:
        members = json.load(members_file)
    member = choice(members)
    return render_template('member.html',
                           user=member)


if __name__ == "__main__":
    app.run(port=8080)