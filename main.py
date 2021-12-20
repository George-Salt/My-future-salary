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


def get_vacancies_hh(language="Python", page=0):
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


def get_statistics_of_languages_hh(languages):
    for language in languages:
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

        languages[language] = {
            "vacancies_found": vacancy_count,
            "vacancies_processed": count_used,
            "average_salary": int(average_salary)
        }
    return languages


def get_get_vacancies_hh_sj(key, language="Python", page=0):
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


def get_statistics_of_languages_sj(key, languages):
    for language in languages:
        count_used = 0
        average_salaries = []
        for page in count(0, 1):
            response = get_vacancies_hh(key, language, page=page)

            for vacancy in response["objects"]:
                if vacancy["payment_from"] or vacancy["payment_to"]:
                    if vacancy["currency"] == "rub":
                        average_salaries.append(predict_rub_salary(vacancy["payment_from"], vacancy["payment_to"]))
                        count_used += 1

            if not response["more"]:
                break

        vacancy_count = response["total"]
        average_salary = sum(average_salaries) / len(average_salaries)

        languages[language] = {
            "vacancies_found": vacancy_count,
            "vacancies_processed": count_used,
            "average_salary": int(average_salary)
        }
    return languages


def create_tables(key, languages):
    sj_table_data = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    ]
    sj_statistics = get_statistics_of_languages_sj(key, languages)
    sj_title = "SuperJob Moscow"
    for language, vacancies in sj_statistics.items():
        sj_table_data.append([language, vacancies["vacancies_found"], vacancies["vacancies_processed"], vacancies["average_salary"]])
    sj_table = AsciiTable(sj_table_data, sj_title)

    hh_table_data = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    ]
    hh_statistics = get_statistics_of_languages_hh(languages)
    hh_title = "HeadHunter Moscow"
    for language, vacancies in hh_statistics.items():
        hh_table_data.append([language, vacancies["vacancies_found"], vacancies["vacancies_processed"], vacancies["average_salary"]])
    hh_table = AsciiTable(hh_table_data, hh_title)
    return f"{sj_table.table}\n{hh_table.table}"


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
