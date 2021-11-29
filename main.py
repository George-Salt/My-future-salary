from terminaltables import AsciiTable
import requests
import os
from dotenv import load_dotenv


def get_request_hh(language="Python", page=0):
    url = "https://api.hh.ru/vacancies"
    params = {
        "specialization": "1.221",
        "area": "1",
        "period": 30,
        "text": language,
        "currency": "RUR",
        "only_with_salary": True,
        "page": page
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def predict_rub_salary_hh(vacancy):
    salary_of_vacancy = vacancy["salary"]
    if salary_of_vacancy["from"] and salary_of_vacancy["to"]:
        expected_salary = int(salary_of_vacancy["to"] + salary_of_vacancy["from"]) / 2
    elif not salary_of_vacancy["from"]:
        expected_salary = salary_of_vacancy["to"] * 1.2
    elif not salary_of_vacancy["to"]:
        expected_salary = salary_of_vacancy["from"] * 0.8
    return expected_salary


def get_description_of_languages_hh():
    count_used = 0
    predict_salaries = []
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
        for page in range(get_request_hh()["pages"]):
            response = get_request_hh(language, page=page)

            for vacancy in response["items"]:
                predict_salaries.append(predict_rub_salary_hh(vacancy))
                count_used += 1

        count_vacancy = response["found"]
        predict_salary = sum(predict_salaries) / len(predict_salaries)

        programming_languages[language] = {
            "vacancies_found": count_vacancy,
            "vacancies_processed": count_used,
            "average_salary": int(predict_salary)
        }
        count_vacancy = 0
        count_used = 0
    return programming_languages


def create_table_hh():
    description = get_description_of_languages_hh()
    title = "HeadHunter Moscow"
    table_data = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"],
        ["Python", description["Python"]["vacancies_found"], description["Python"]["vacancies_processed"], description["Python"]["average_salary"]],
        ["Java", description["Java"]["vacancies_found"], description["Java"]["vacancies_processed"], description["Java"]["average_salary"]],
        ["Javascript", description["Javascript"]["vacancies_found"], description["Javascript"]["vacancies_processed"], description["Javascript"]["average_salary"]],
        ["Ruby", description["Ruby"]["vacancies_found"], description["Ruby"]["vacancies_processed"], description["Ruby"]["average_salary"]],
        ["PHP", description["PHP"]["vacancies_found"], description["PHP"]["vacancies_processed"], description["PHP"]["average_salary"]],
        ["C++", description["C++"]["vacancies_found"], description["C++"]["vacancies_processed"], description["C++"]["average_salary"]],
        ["C#", description["C#"]["vacancies_found"], description["C#"]["vacancies_processed"], description["C#"]["average_salary"]],
        ["C", description["C"]["vacancies_found"], description["C"]["vacancies_processed"], description["C"]["average_salary"]],
        ["Go", description["Go"]["vacancies_found"], description["Go"]["vacancies_processed"], description["Go"]["average_salary"]],
        ["Shell", description["Shell"]["vacancies_found"], description["Shell"]["vacancies_processed"], description["Shell"]["average_salary"]],
    ]
    table = AsciiTable(table_data, title)
    return table.table


def get_request_sj(key, language="Python", page=0):
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": key
    }

    params = {
        "town": "Moscow",
        "period": 30,
        "catalogues": 48,
        "currency": "rub",
        "keyword": language,
        "page": page
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def predict_rub_salary_sj(vacancy):
    if vacancy["payment_from"] and vacancy["payment_to"]:
        expected_salary = int(vacancy["payment_to"] + vacancy["payment_from"]) / 2
    elif not vacancy["payment_from"]:
        expected_salary = vacancy["payment_to"] * 1.2
    elif not vacancy["payment_to"]:
        expected_salary = vacancy["payment_from"] * 0.8
    return expected_salary


def get_description_of_languages_sj(key):
    count_used = 0
    predict_salaries = []
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
        for page in range(int(get_request_sj(key, language)["total"] / 20 + 1)):
            response = get_request_sj(key, language, page=page)

            for vacancy in response["objects"]:
                predict_salaries.append(predict_rub_salary_sj(vacancy))
                count_used += 1

        count_vacancy = response["total"]
        predict_salary = sum(predict_salaries) / len(predict_salaries)

        programming_languages[language] = {
            "vacancies_found": count_vacancy,
            "vacancies_processed": count_used,
            "average_salary": int(predict_salary)
        }
        count_vacancy = 0
        count_used = 0
    return programming_languages


def create_table_sj():
    description = get_description_of_languages_sj(superjob_key)
    title = "SuperJob Moscow"
    table_data = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"],
        ["Python", description["Python"]["vacancies_found"], description["Python"]["vacancies_processed"], description["Python"]["average_salary"]],
        ["Java", description["Java"]["vacancies_found"], description["Java"]["vacancies_processed"], description["Java"]["average_salary"]],
        ["Javascript", description["Javascript"]["vacancies_found"], description["Javascript"]["vacancies_processed"], description["Javascript"]["average_salary"]],
        ["Ruby", description["Ruby"]["vacancies_found"], description["Ruby"]["vacancies_processed"], description["Ruby"]["average_salary"]],
        ["PHP", description["PHP"]["vacancies_found"], description["PHP"]["vacancies_processed"], description["PHP"]["average_salary"]],
        ["C++", description["C++"]["vacancies_found"], description["C++"]["vacancies_processed"], description["C++"]["average_salary"]],
        ["C#", description["C#"]["vacancies_found"], description["C#"]["vacancies_processed"], description["C#"]["average_salary"]],
        ["C", description["C"]["vacancies_found"], description["C"]["vacancies_processed"], description["C"]["average_salary"]],
        ["Go", description["Go"]["vacancies_found"], description["Go"]["vacancies_processed"], description["Go"]["average_salary"]],
        ["Shell", description["Shell"]["vacancies_found"], description["Shell"]["vacancies_processed"], description["Shell"]["average_salary"]],
    ]
    table = AsciiTable(table_data, title)
    return table.table


if __name__ == "__main__":
    load_dotenv()
    superjob_key = os.getenv("SUPERJOB_SECRET_KEY")
    print(f"{create_table_sj()}\n{create_table_hh()}")
