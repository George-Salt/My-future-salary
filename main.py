import requests


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


def get_description_of_vacancies():
    count_used = 0
    predict_salaries = []
    url = "https://api.hh.ru/vacancies"
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
            "text": f"{language}",
            "currency": "RUR",
            "only_with_salary": True
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        for vacancy in response.json()["items"]:
            predict_salaries.append(predict_rub_salary(vacancy))
            count_used += 1

        predict_salary = sum(predict_salaries) / len(predict_salaries)

        count_vacancy = response.json()["found"]
        programming_languages[language] = {
            "vacancies_found": count_vacancy,
            "vacancies_processed": count_used,
            "average_salary": int(predict_salary)
        }
        count_vacancy = 0
        count_used = 0
    return programming_languages


print(get_description_of_vacancies())
