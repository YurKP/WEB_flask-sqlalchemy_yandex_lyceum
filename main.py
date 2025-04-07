from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Job
from random import shuffle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")

    captain = User()
    captain.surname = 'Scott'
    captain.name = 'Ridley'
    captain.age = 21
    captain.position = 'captain'
    captain.speciality = 'research engineer'
    captain.address = 'module_1'
    captain.email = 'scott_chief@mars.org'

    db_sess = db_session.create_session()
    db_sess.add(captain)

    surname_and_name = [('Спилберг', 'Стивен'), ('Лукас', 'Джордж'), ('Ричи', 'Гай'), ('Нолан', 'Кристофер')]
    ages = [78, 80, 56, 54]
    positions = ['navigator', 'doctor']
    specialities = ['design constructor', 'zoologist']
    count_1 = 2
    count_2 = 1

    for item in surname_and_name:
        mission_participant = User()
        mission_participant.surname = item[0]
        mission_participant.name = item[1]
        mission_participant.age = ages[surname_and_name.index(item)]

        shuffle(positions)
        shuffle(specialities)

        mission_participant.position = positions[0]
        mission_participant.speciality = specialities[0]
        mission_participant.address = f'module_{count_1}'
        mission_participant.email = f'mission_participant{count_2}@mars.org'

        db_sess.add(mission_participant)

        count_1 += 1
        count_2 += 1

    new_job = Job()
    new_job.team_leader = 1
    new_job.job = 'deployment of residential modules 1 and 2'
    new_job.work_size = 15
    new_job.collaborators = '2, 3'
    new_job.is_finished = False
    db_sess.add(new_job)

    db_sess.commit()
    # app.run()


if __name__ == '__main__':
    main()