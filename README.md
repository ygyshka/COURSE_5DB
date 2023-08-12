# COURSE_5DB

## Проект проектирования программы для получения информации о вакансиях определенных 10 компаний на HeadHunter.

    """ Необходимо реализовать проект по парсингу сайта HeadHunter с получением итнформации о работадателях и их активных 
    вакансиях.
    Отличительная особенность проекта заключается в обязательном хранении информации в базе данных PostgresSQL.
    После получения информации, ее нужно записать в базу данных и дальнейшую обработку обработку запросов к информации,
    реализовывать через запросы к базе данных и язык SQL. """

## Основные шаги проекта

- Получить данные о работодателях и их вакансиях с сайта hh.ru. 
  Для этого использовать публичный API и библиотеку `requests`.
- Выбрать не менее 10 интересных компаний, от которых пользователь будет получать данные о вакансиях по API.
- Спроектировать таблицы в БД Postgres для хранения полученных данных о работодателях и их вакансиях. 
  Для работы с БД использовать библиотеку `psycopg2`.
- Реализовать код, который заполняет созданные таблицы в БД Postgres данными о работодателях и их вакансиях.
- Создать класс `DBManager` для работы с данными в БД.