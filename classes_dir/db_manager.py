# Подключение библиотек для работы с базой данных и файлом конфигурации базы данных
import psycopg2
from config import config


class DBManager:
    """
    Класс для обработки запроса к API, для подключения к базе данных и получения определенных запросов из базы данных
    """
    def __init__(self, vacancy_id, employer_id, vacancy_name, vacancy_url, salary):

        self.vacancy_id = vacancy_id
        self.vacancy_name = vacancy_name
        self.vacancy_url = vacancy_url
        self.employer_id = employer_id
        if salary is not None:
            if salary['from'] is not None:
                self.salary = salary['from']
                self.currency = salary['currency']
            else:
                self.salary = salary['to']
                self.currency = salary['currency']
        else:
            self.salary = 0
            self.currency = 'RUR'

    def __repr__(self):

        return f'DBManager(vacancy_id={self.vacancy_id},' \
               f'employer={self.employer_id}' \
               f'vacancy_name={self.vacancy_name}, ' \
               f'vacancy_url={self.vacancy_url},' \
               f'salary={self.salary}' \
               f'currency={self.currency}'

    def __str__(self):

        return f'vacancy_id: {self.vacancy_id}\n' \
               f'ID Организации: {self.employer_id}\n' \
               f'Название вакансии: {self.vacancy_name}\n' \
               f'Зарплата: {self.salary} {self.currency}\n' \
               f'Ссылка на web страницу вакансии: {self.vacancy_url}\n'

    @staticmethod
    def base_connect(params: dict):
        """
        Метод подключения к базе данных
        :param params:
        :return:
        """
        conn = psycopg2.connect(dbname='vacancies_hh', **params)
        return conn

    @staticmethod
    def get_companies_and_vacancies_count():
        """
        Получение из базы данных наименований организаций и количества вакансий в этих организациях
        :return:
        """

        conn = DBManager.base_connect(config())
        with conn.cursor() as cur:
            cur.execute(
                """
                select employer_title, count(*) from employers 
                inner join vacancies using(employer_id)
                group by employer_id
                order by count(*) desc
                """
            )
            vacancies = cur.fetchall()
        conn.close()
        for item in vacancies:
            print(f'Название организации - "{item[0]}". В организации доступно {item[1]} вакансий(-и).')

    @staticmethod
    def get_all_vacancies():
        """
        Получение из базы данных наименований организаций,
        наименований вакансий, зарплат, курса валют, ссылок на web страници
        :return:
        """

        conn = DBManager.base_connect(config())
        with conn.cursor() as cur:
            cur.execute(
                """
                select employer_title, vacancy_name, salary, currency, vacancy_url from vacancies
                join employers using(employer_id)
                order by salary desc
                """
            )
            vacancies = cur.fetchall()
        conn.close()
        for item in vacancies:
            print(f'Компания: {item[0]}. Вакансия: {item[1]}. '
                  f'Зарплата: {item[2]} {item[3]}. '
                  f'Ссылка на вакансию: {item[4]}.\n')

    @staticmethod
    def get_avg_salary():
        """
        Получение среднего значения поля salary в таблице vacancies из базы данных
        :return:
        """

        conn = DBManager.base_connect(config())
        with conn.cursor() as cur:
            cur.execute(
                """
                select avg(salary), (
                select distinct currency from vacancies
                ) as currency 
                from vacancies
                where salary > 0
                """
            )
            result = cur.fetchone()
        conn.close()
        print(f"\nСредняя заработная плата по вакансиям с указаным размером з\п: {round(result[0])} {result[1]} .")

    @staticmethod
    def get_vacancies_with_higher_salary():
        """
        Получение списка вакансий из базы данных, у которых зарплата выше среднего значения зарплаты вакансий,
        у которых указана зарплата
        :return:
        """

        conn = DBManager.base_connect(config())
        with conn.cursor() as cur:
            cur.execute(
                """
                select employer_title, vacancy_name, salary, currency, vacancy_url from vacancies
                join employers using(employer_id)
                where salary > (
                select avg(salary) from vacancies
                where salary > 0
                )
                order by salary desc
                """
            )
            vacancies = cur.fetchall()
        conn.close()
        notes = 0
        for item in vacancies:
            print(f'Компания: {item[0]}. Вакансия: {item[1]}. '
                  f'Зарплата: {item[2]} {item[3]}. '
                  f'Ссылка на вакансию: {item[4]}.\n')
            notes += 1
        print(f"Получено {notes} записи(-ей)".upper())

    @staticmethod
    def get_vacancies_with_keyword(word):
        """
        Получение списка вакансий из базы данных, в названии которых содержиться введеное пользователем слово
        :param word:
        :return:
        """

        conn = DBManager.base_connect(config())
        with conn.cursor() as cur:
            cur.execute(
                f"""
                select employer_title, vacancy_name, salary, currency, vacancy_url from vacancies
                join employers using(employer_id)
                where vacancy_name like '%{word}%'
                """
            )
            vacancies = cur.fetchall()
        conn.close()
        notes = 0
        if len(vacancies) == 0:
            print("Совпадений не найдено!\n"
                  "Повторите запрос...")
        else:
            for item in vacancies:
                print(f'Компания: {item[0]}. Вакансия: {item[1]}. '
                      f'Зарплата: {item[2]} {item[3]}. '
                      f'Ссылка на вакансию: {item[4]}.\n')
                notes += 1
            print(f"Получено {notes} записи(-ей)".upper())
