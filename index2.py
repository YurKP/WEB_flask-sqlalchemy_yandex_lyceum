from flask import Flask, render_template, abort, request
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import SubmitField
from flask_wtf.file import FileRequired, FileField
from data import db_session
from data.users import User
from data.jobs import Job
from data.departments import Department
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.job import AddJobForm
from forms.department import AddDepartmentForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():

    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()

    return render_template('index.html', title='Заготовка', jobs=jobs)


@app.route('/departments')
def show_departments():

    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()

    return render_template('departments.html', title='Заготовка', departments=departments)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    db_session.global_init("db/mars_explorer.db")
    form = RegisterForm()

    if form.validate_on_submit():

        if form.password.data != form.password_again.data:
            return render_template('register_form.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register_form.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')

    return render_template('register_form.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init("db/mars_explorer.db")

    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    db_session.global_init("db/mars_explorer.db")
    form = LoginForm()

    if form.validate_on_submit():

        db_sess = db_session.create_session()

        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, img='static/img/эмблема.png')

    return render_template('login.html', title='Авторизация', form=form, img='static/img/эмблема.png')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    db_session.global_init("db/mars_explorer.db")
    form = AddJobForm()

    if form.validate_on_submit():

        db_sess = db_session.create_session()
        ids = [i.id for i in db_sess.query(User).all()]

        if int(form.team_leader.data) not in ids:
            return render_template('add_job.html', title='Adding a job',
                                   form=form,
                                   message="Такого team_leader'а нет")

        for i in form.collaborators.data.split(', '):
            if int(i) not in ids:
                return render_template('add_job.html', title='Adding a job',
                                       form=form,
                                       message="Таких collaborators'ов нет")

        job = Job(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')

    return render_template('add_job.html',
                           title='Adding a job', form=form)


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    db_session.global_init("db/mars_explorer.db")
    form = AddJobForm()

    if request.method == "GET":
        db_sess = db_session.create_session()

        jobs = db_sess.query(Job).filter(Job.id == id,
                                         ((Job.team_leader == current_user.id) | (current_user.id == 1))).first()

        if jobs:
            form.job.data = jobs.job
            form.team_leader.data = jobs.team_leader
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        jobs = db_sess.query(Job).filter(Job.id == id,
                                         ((Job.team_leader == current_user.id) | (current_user.id == 1))).first()
        ids = [i.id for i in db_sess.query(User).all()]

        if jobs:
            if int(form.team_leader.data) not in ids:
                return render_template('add_job.html', title='Adding a job',
                                       form=form,
                                       message="Такого team_leader'а нет")

            for i in form.collaborators.data.split(', '):
                if int(i) not in ids:
                    return render_template('add_job.html', title='Adding a job',
                                           form=form,
                                           message="Таких collaborators'ов нет")

            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data

            db_sess.commit()
            return redirect('/')
        else:
            abort(404)

    return render_template('add_job.html', title='Редактирование работы', form=form)


@app.route('/delete_job/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).filter(Job.id == id,
                                     ((Job.team_leader == current_user.id) | (current_user.id == 1))).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)

    return redirect('/')


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    db_session.global_init("db/mars_explorer.db")
    form = AddDepartmentForm()

    if form.validate_on_submit():

        db_sess = db_session.create_session()
        ids = [i.id for i in db_sess.query(User).all()]

        if int(form.chief.data) not in ids:
            return render_template('add_departments.html', title='Adding a Department',
                                   form=form,
                                   message="Такого chief'а нет")

        for i in form.members.data.split(', '):
            if int(i) not in ids:
                return render_template('add_departments.html', title='Adding a Department',
                                       form=form,
                                       message="Таких members'ов нет")

        department = Department(
            chief=form.chief.data,
            title=form.title.data,
            members=form.members.data,
            email=form.email.data
        )
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')

    return render_template('add_departments.html',
                           title='Adding a Department', form=form)


@app.route('/edit_department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    db_session.global_init("db/mars_explorer.db")
    form = AddDepartmentForm()

    if request.method == "GET":
        db_sess = db_session.create_session()

        departments = db_sess.query(Department).filter(Department.id == id,
                                         ((Department.chief == current_user.id) | (current_user.id == 1))).first()

        if departments:
            form.title.data = departments.title
            form.chief.data = departments.chief
            form.members.data = departments.members
            form.email.data = departments.email
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ids = [i.id for i in db_sess.query(User).all()]

        departments = db_sess.query(Department).filter(Department.id == id,
                                                       ((Department.chief == current_user.id) | (
                                                                   current_user.id == 1))).first()

        if departments:
            if int(form.chief.data) not in ids:
                return render_template('add_departments.html', title='Adding a Department',
                                       form=form,
                                       message="Такого chief'а нет")

            for i in form.members.data.split(', '):
                if int(i) not in ids:
                    return render_template('add_departments.html', title='Adding a Department',
                                           form=form,
                                           message="Таких members'ов нет")

            departments.title = form.title.data
            departments.chief = form.chief.data
            departments.members = form.members.data
            departments.email = form.email.data

            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)

    return render_template('add_departments.html', title='Редактирование департамента', form=form)


@app.route('/delete_department/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).filter(Department.id == id,
                                                   ((Department.chief == current_user.id) | (
                                                               current_user.id == 1))).first()
    if departments:
        db_sess.delete(departments)
        db_sess.commit()
    else:
        abort(404)

    return redirect('/departments')


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