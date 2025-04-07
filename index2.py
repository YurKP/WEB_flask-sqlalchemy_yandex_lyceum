from flask import Flask, render_template
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileField
from data import db_session
from data.jobs import Job
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():

    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()

    return render_template('index.html', title='Заготовка', jobs=jobs)


@app.route('/training/<prof>')
def professions(prof):
    return render_template('training.html', title='Заготовка', profession=prof)


@app.route('/list_prof/<typ>')
def work_with_list(typ):
    return render_template('list_professions.html', title='Заготовка', type_of_list=typ,
                           lst=['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач',
                                'инженер по терраформированию', 'климатолог',
                                'специалист по радиационной защите', 'астрогеолог', 'гляциолог',
                                'инженер жизнеобеспечения', 'метеоролог', 'оператор марсохода',
                                'киберинженер', 'штурман', 'пилот дронов'])


@app.route('/answer')
@app.route('/auto_answer')
def questionnaire_answer():
    dict_with_information = {'surname': 'Watny', 'name': 'Mark', 'education': 'выше среднего',
                             'profession': 'штурман марсохода', 'sex': 'male',
                             'motivation': 'Всегда мечтал ...', 'ready': 'True'}

    return render_template('auto_answer.html', title='Анкета', data=dict_with_information)


class LoginForm(FlaskForm):
    id_astronaut = StringField('Id астронавта', validators=[DataRequired()])
    astronaut_password = PasswordField('Пароль астронавта', validators=[DataRequired()])

    id_captain = StringField('Id капитана', validators=[DataRequired()])
    captain_password = PasswordField('Пароль капитана', validators=[DataRequired()])

    submit = SubmitField('Доступ')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form, img='static/img/эмблема.png')


@app.route('/success')
def success():
    return render_template('success.html', title='Авторизация')


@app.route('/distribution')
def distribution():
    passenger_list = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венката Капур', 'Тедди Сандерс', 'Шон Бин']

    return render_template('distribution.html', title='Распределение', passenger_list=passenger_list)


@app.route('/table/<gender>/<int:age>')
def cabin_color(gender, age):
    return render_template('cabin_decoration.html', title='Оформление каюты', gender=gender,
                           age=age)


class LoadPhotoForm(FlaskForm):
    photo = FileField('Добавить картинку', validators=[FileRequired()])

    submit = SubmitField('Загрузить')

    lst_photo = ['2.png', '3.png']


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    load_photo = LoadPhotoForm(meta={'csrf': False})

    if load_photo.validate_on_submit():
        f = load_photo.photo.data

        f.save(f'static/img/gallery/{f.filename}')
        LoadPhotoForm.lst_photo.append(f.filename)

        return redirect('/upload')

    return render_template('gallery.html', title='Загрузка фотографии', form=load_photo,
                           lst=LoadPhotoForm.lst_photo)


@app.route('/member')
def member():
    with open('templates/document.json', encoding='utf-8') as f:
        data = json.load(f)

    lst = list()

    for i in range(1, 4):
        x = ((data['mission_participant'][str(i)]['name'],
             data['mission_participant'][str(i)]['surname']),
             data['mission_participant'][str(i)]['photo'],
             data['mission_participant'][str(i)]['profession'])
        lst.append(x)

    return render_template('member.html', title='Участник', lst=lst)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')