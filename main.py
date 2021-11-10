import requests


def get_count_vacancies():
    url = "https://api.hh.ru/vacancies"
    count_vacancy = 0
    programming_languages = {
        "Python": 0,
        "Java": 0,
        "Javascript": 0,
        "Ruby": 0,
        "PHP": 0,
        "C++": 0,
        "C#": 0,
        "C": 0,
        "Go": 0,
        "Shell": 0
    }

    for language in programming_languages:
        params = {
            "specialization": "1.221",
            "area": "1",
            "period": 30,
            "text": f"{language}"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        count_vacancy = response.json()["found"]
        programming_languages[language] = count_vacancy
        count_vacancy = 0
    return programming_languages


def get_salary_of_python():
    url = "https://api.hh.ru/vacancies"
    salary = []
    params = {
        "specialization": "1.221",
        "area": "1",
        "period": 30,
        "text": "Python"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    for vacancy_num in range(20):
        salary_in_vacancy = response.json()["items"][vacancy_num]["salary"]
        salary.append(salary_in_vacancy)
    return salary


def get_request():
    url = "https://api.hh.ru/vacancies"
    params = {
        "specialization": "1.221",
        "area": "1",
        "period": 30,
        "text": "Python",
        "currency": "RUR",
        "only_with_salary": True
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def predict_rub_salary(vacancy):
    salary_of_vacancy = vacancy["salary"]
    if salary_of_vacancy["from"] and salary_of_vacancy["to"]:
        expected_salary = int(salary_of_vacancy["to"] + salary_of_vacancy["from"]) / 2
    elif not salary_of_vacancy["from"]:
        expected_salary = salary_of_vacancy["to"] * 1.2
    elif not salary_of_vacancy["to"]:
        expected_salary = salary_of_vacancy["from"] * 0.8
    return expected_salary


for vacancy in get_request()["items"]:
    print(predict_rub_salary(vacancy))
