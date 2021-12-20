from terminaltables import AsciiTable
import requests
import os
from itertools import count
from dotenv import load_dotenv


PROGRAMMER_SPECIALIZATION = "1.221"
MOSCOW_ID = "1"
DAYS_IN_PERIOD = 30
PROGRAMMING_CATALOGUE = 48
HH_TITLE = "HeadHunter Moscow"
SJ_TITLE = "SuperJob Moscow"


def predict_rub_salary(salary_from=None, salary_to=None):
    if salary_from and salary_to:
        expected_salary = int(salary_to + salary_from) / 2
    elif not salary_from:
        expected_salary = salary_to * 1.2
    elif not salary_to:
        expected_salary = salary_from * 0.8
    return expected_salary


def get_vacancies_hh(language="Python", page=0):
    url = "https://api.hh.ru/vacancies/"
    params = {
        "specialization": PROGRAMMER_SPECIALIZATION,
        "area": MOSCOW_ID,
        "period": DAYS_IN_PERIOD,
        "text": language,
        "page": page
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_statistics_of_one_language_hh(language):
    average_salaries = []
    count_used = 0
    for page in count(0, 1):
        response = get_vacancies_hh(language, page=page)

        for vacancy in response["items"]:
            if vacancy["salary"] and vacancy["salary"]["currency"] == "RUR":
                average_salaries.append(predict_rub_salary(vacancy["salary"]["from"], vacancy["salary"]["to"]))
                count_used += 1

        if page >= response["pages"] - 1:
            break

    vacancy_count = response["found"]
    average_salary = sum(average_salaries) / len(average_salaries)

    vacancies_for_language = {
        "vacancies_found": vacancy_count,
        "vacancies_processed": count_used,
        "average_salary": int(average_salary)
    }
    return vacancies_for_language


def get_statistics_of_languages_hh(languages):
    for language in languages:
        languages[language] = get_statistics_of_one_language_hh(language)
    return languages


def get_vacancies_sj(key, language="Python", page=0):
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": key
    }

    params = {
        "town": "Moscow",
        "period": DAYS_IN_PERIOD,
        "catalogues": PROGRAMMING_CATALOGUE,
        "keyword": language,
        "page": page
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def get_statistics_of_one_language_sj(key, language):
    count_used = 0
    average_salaries = []
    for page in count(0, 1):
        response = get_vacancies_sj(key, language, page=page)

        for vacancy in response["objects"]:
            if vacancy["payment_from"] or vacancy["payment_to"]:
                if vacancy["currency"] == "rub":
                    average_salaries.append(predict_rub_salary(vacancy["payment_from"], vacancy["payment_to"]))
                    count_used += 1

        if not response["more"]:
            break

    vacancy_count = response["total"]
    average_salary = sum(average_salaries) / len(average_salaries)

    vacancies_for_language = {
        "vacancies_found": vacancy_count,
        "vacancies_processed": count_used,
        "average_salary": int(average_salary)
    }
    return vacancies_for_language


def get_statistics_of_languages_sj(key, languages):
    for language in languages:
        languages[language] = get_statistics_of_one_language_sj(key, language)
    return languages


def create_table(title, statistics):
    table_data = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    ]
    for language, vacancies in statistics.items():
        table_data.append([language, vacancies["vacancies_found"], vacancies["vacancies_processed"], vacancies["average_salary"]])
    table = AsciiTable(table_data, title)
    return table.table


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
    hh_table = create_table(HH_TITLE, get_statistics_of_languages_hh(programming_languages))
    sj_table = create_table(SJ_TITLE, get_statistics_of_languages_sj(superjob_key, programming_languages))
    print(f"{sj_table}\n{hh_table}")
