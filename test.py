from requests import get, post, delete

# тестирование API пользователя

# пользователь с id = 1, корректный запрос
print(get('http://localhost:8080/api/v2/users/1').json())
# пользователь с несуществующим id
print(get('http://localhost:8080/api/v2/users/23').json())

# все пользователи
print(get('http://localhost:8080/api/v2/users').json())

# добавление пользователя, корректный запрос
print(post('http://localhost:8080/api/v2/users', json={'name': 'Вася', 'surname': 'Пупкин', 'age': 12,
                                                       'position': 'chief', 'speciality': 'geography',
                                                       'address': 'где-то что-то когда-то',
                                                       'email': 'df@mars.org'}).json())
# добавление пользователя с незаполненными полями
print(post('http://localhost:8080/api/v2/users', json={'name': 'Вася', 'surname': 'Пупкин', 'age': 12,
                                                       'position': 'chief'}).json())

# все пользователи
print(get('http://localhost:8080/api/v2/users').json())

# удаление пользователя с id = 6, корректный запрос
print(delete('http://localhost:8080/api/v2/users/6').json())
# удаление несуществующего пользователя
print(delete('http://localhost:8080/api/v2/users/100').json())

# все пользователи
print(get('http://localhost:8080/api/v2/users').json())


# тестирование API работы

# работа с id = 1, корректный запрос
print(get('http://localhost:8080/api/v2/jobs/1').json())
# несуществующая работа
print(get('http://localhost:8080/api/v2/jobs/23').json())

# все работы
print(get('http://localhost:8080/api/v2/jobs').json())

# добавление работы, корректный запрос
print(post('http://localhost:8080/api/v2/jobs', json={'team_leader': 4,
                                                      'job': 'какое-то полезное занятие',
                                                      'work_size': 3,
                                                      'collaborators': '3, 4', 'is_finished': 1}).json())
# добавление работы с незаполненными полями
print(post('http://localhost:8080/api/v2/jobs', json={'job': 'что-то надо', 'work_size': 12}).json())

# все работы
print(get('http://localhost:8080/api/v2/jobs').json())

# удаление работы с id = 5
print(delete('http://localhost:8080/api/v2/jobs/5').json())
# удаление несуществующей работы
print(delete('http://localhost:8080/api/v2/jobs/100').json())

# все работы
print(get('http://localhost:8080/api/v2/jobs').json())