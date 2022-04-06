from collections import defaultdict
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
    elif salary_to:
        expected_salary = salary_to * 1.2
    elif salary_from:
        expected_salary = salary_from * 0.8
    return expected_salary


def get_vacancies_hh(specialty, period, moscow_id, language="Python", page=0):
    url = "https://api.hh.ru/vacancies/"
    params = {
        "specialization": specialty,
        "area": moscow_id,
        "period": period,
        "text": language,
        "page": page
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_statistics_of_one_language_hh(specialty, period, moscow_id, language):
    average_salaries = []
    count_used = 0
    for page in count(0, 1):
        response = get_vacancies_hh(
            specialty,
            period,
            moscow_id,
            language,
            page=page
        )

        for vacancy in response["items"]:
            if vacancy["salary"] and vacancy["salary"]["currency"] == "RUR":
                average_salaries.append(predict_rub_salary(
                    vacancy["salary"]["from"],
                    vacancy["salary"]["to"]
                ))
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


def get_statistics_of_languages_hh(specialty, period, moscow_id, languages):
    statistics = defaultdict()
    for language in languages:
        statistics[language] = get_statistics_of_one_language_hh(
            specialty,
            period,
            moscow_id,
            language
        )
    return statistics


def get_vacancies_sj(period, catalogue, key, language="Python", page=0):
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": key
    }

    params = {
        "town": "Moscow",
        "period": period,
        "catalogues": catalogue,
        "keyword": language,
        "page": page
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def get_statistics_of_one_language_sj(period, catalogue, key, language):
    count_used = 0
    average_salaries = []
    for page in count(0, 1):
        response = get_vacancies_sj(
            period,
            catalogue,
            key,
            language,
            page=page
        )

        for vacancy in response["objects"]:
            if vacancy["payment_from"] or vacancy["payment_to"] != 0 or None:
                if vacancy["currency"] == "rub":
                    average_salaries.append(predict_rub_salary(
                        vacancy["payment_from"],
                        vacancy["payment_to"]
                    ))
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


def get_statistics_of_languages_sj(period, catalogue, key, languages):
    statistics = defaultdict()
    for language in languages:
        statistics[language] = get_statistics_of_one_language_sj(
            period,
            catalogue,
            key,
            language
        )
    return statistics


def create_table(title, statistics):
    table_data = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
        ]
    ]
    for language, vacancies in statistics.items():
        table_data.append([
            language,
            vacancies["vacancies_found"],
            vacancies["vacancies_processed"],
            vacancies["average_salary"]
        ])
    table = AsciiTable(table_data, title)
    return table.table


if __name__ == "__main__":
    programming_languages = [
        "Python",
        "Java",
        "Javascript",
        "Ruby",
        "PHP",
        "C++",
        "C#",
        "C",
        "Go",
        "Shell"
    ]

    load_dotenv()
    superjob_key = os.getenv("SUPERJOB_SECRET_KEY")
    hh_table = create_table(
        HH_TITLE,
        get_statistics_of_languages_hh(
            PROGRAMMER_SPECIALIZATION,
            DAYS_IN_PERIOD,
            MOSCOW_ID,
            programming_languages
        )
    )
    sj_table = create_table(
        SJ_TITLE,
        get_statistics_of_languages_sj(
            DAYS_IN_PERIOD,
            PROGRAMMING_CATALOGUE,
            superjob_key,
            programming_languages
        )
    )
    print(f"{sj_table}\n{hh_table}")
