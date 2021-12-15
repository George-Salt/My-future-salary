from terminaltables import AsciiTable
import requests
import os
from itertools import count
from dotenv import load_dotenv


PROGRAMMER_SPECIALIZATION = "1.221"
MOSCOW_ID = "1"
PERIOD_DAYS = 30
PROGRAMMING_CATALOGUE = 48


def predict_rub_salary(salary_from=None, salary_to=None):
    if salary_from and salary_to:
        expected_salary = int(salary_to + salary_from) / 2
    elif not salary_from:
        expected_salary = salary_to * 1.2
    elif not salary_to:
        expected_salary = salary_from * 0.8
    return expected_salary


def get_request_hh(language="Python", page=0):
    url = "https://api.hh.ru/vacancies/"
    params = {
        "specialization": PROGRAMMER_SPECIALIZATION,
        "area": MOSCOW_ID,
        "period": PERIOD_DAYS,
        "text": language,
        "page": page
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_description_of_languages_hh(languages):
    for language in languages:
        average_salaries = []
        count_used = 0
        count_vacancy = 0
        for page in count(0, 1):
            response = get_request_hh(language, page=page)

            for vacancy in response["items"]:
                if vacancy["salary"]:
                    if vacancy["salary"]["currency"] == "RUR":
                        average_salaries.append(predict_rub_salary(vacancy["salary"]["from"], vacancy["salary"]["to"]))
                        count_used += 1

            if page >= response["pages"] - 1:
                break

        count_vacancy = response["found"]
        average_salary = sum(average_salaries) / len(average_salaries)

        languages[language] = {
            "vacancies_found": count_vacancy,
            "vacancies_processed": count_used,
            "average_salary": int(average_salary)
        }
    return languages


def get_request_sj(key, language="Python", page=0):
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": key
    }

    params = {
        "town": "Moscow",
        "period": PERIOD_DAYS,
        "catalogues": PROGRAMMING_CATALOGUE,
        "keyword": language,
        "page": page
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def get_description_of_languages_sj(key, languages):
    for language in languages:
        count_used = 0
        average_salaries = []
        count_vacancy = 0
        for page in count(0, 1):
            response = get_request_sj(key, language, page=page)

            for vacancy in response["objects"]:
                if vacancy["payment_from"] or vacancy["payment_to"]:
                    if vacancy["currency"] == "rub":
                        average_salaries.append(predict_rub_salary(vacancy["payment_from"], vacancy["payment_to"]))
                        count_used += 1

            if not response["more"]:
                break

        count_vacancy = response["total"]
        average_salary = sum(average_salaries) / len(average_salaries)

        languages[language] = {
            "vacancies_found": count_vacancy,
            "vacancies_processed": count_used,
            "average_salary": int(average_salary)
        }
    return languages


def create_tables(key, languages):
    table_data_sj = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    ]
    description_sj = get_description_of_languages_sj(key, languages)
    title_sj = "SuperJob Moscow"
    for language, vacancies in description_sj.items():
        table_data_sj.append([language, vacancies["vacancies_found"], vacancies["vacancies_processed"], vacancies["average_salary"]])
    table_sj = AsciiTable(table_data_sj, title_sj)

    table_data_hh = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    ]
    description_hh = get_description_of_languages_hh(languages)
    title_hh = "HeadHunter Moscow"
    for language, vacancies in description_hh.items():
        table_data_hh.append([language, vacancies["vacancies_found"], vacancies["vacancies_processed"], vacancies["average_salary"]])
    table_hh = AsciiTable(table_data_hh, title_hh)
    return f"{table_sj.table}\n{table_hh.table}"


if __name__ == "__main__":
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
    load_dotenv()
    superjob_key = os.getenv("SUPERJOB_SECRET_KEY")
    print(create_tables(superjob_key, programming_languages))
