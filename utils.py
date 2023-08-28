# Подключение библиотек для обработки данных и взаимодействия с базой данных
import psycopg2
from classes_dir.db_manager import DBManager


def get_vacancies(data: list[dict]) -> list[DBManager]:
    """
    Приведение полученых данных от API к виду для дальнейшей записи в базу данных
    :param data:
    :return:
    """
    new_list = []
    for item in data:
        vacancy = DBManager(item['id'],
                            item['employer']['id'],
                            item['name'],
                            item['alternate_url'],
                            item['salary'])
        new_list.append(vacancy)
    return new_list


def create_database(database_name: str, params: dict) -> None:
    """
    Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях
    :param database_name:
    :param params:
    :return:
    """
    # Создание базы данных
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'drop database if exists {database_name}')
    cur.execute(f'create database {database_name}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    # Создание таблици о работодателях
    with conn.cursor() as cur:
        cur.execute(
            """
            create table employers (
                employer_id int PRIMARY KEY,
                employer_title varchar(100)
            )
            """
        )
    # Создание таблици о вакансиях
    with conn.cursor() as cur:
        cur.execute(
            """
            create table vacancies (
                vacancy_id int PRIMARY KEY,
                employer_id int REFERENCES employers(employer_id),
                vacancy_name varchar not NULL,
                salary int,
                currency varchar(10),
                vacancy_url text
            )
            """
        )
    conn.commit()
    conn.close()


def save_employers_to_database(data: dict, database_name: str, params: dict) -> None:
    """
    Сохранение данных о работодателях в базу данных
    :param data:
    :param database_name:
    :param params:
    :return:
    """
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for k, v in data.items():
            cur.execute("""insert into employers (employer_id, employer_title) values (%s, %s)
                        """, (k, v))
    conn.commit()
    conn.close()


def save_vacancies_to_database(data_list: list.__dict__, database_name: str, params: dict) -> None:
    """
        Сохранение данных о вакансиях в базу данных
        :param data_list:
        :param database_name:
        :param params:
        :return:
        """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for item in data_list:
            cur.execute("""insert into vacancies (vacancy_id, employer_id,
             vacancy_name, salary, currency, vacancy_url ) values (%s, %s, %s, %s, %s, %s)
                            """, (item.vacancy_id, item.employer_id, item.vacancy_name,
                                  item.salary, item.currency, item.vacancy_url))
    conn.commit()
    conn.close()
