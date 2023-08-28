# Подключение файлов для реализации основного блока программы
from utils import save_employers_to_database, create_database, save_vacancies_to_database, get_vacancies
from config import config
from classes_dir.api_connect import HhAPI, EMPLOYERS_ID
from classes_dir.db_manager import DBManager


def main():
    """
    Основной блок программы
    :return:
    """
    # Обозначение, создание базы данных, сохранение списка работадателей в базу
    db_name = 'vacancies_hh'
    params = config()
    create_database(db_name, params)
    save_employers_to_database(EMPLOYERS_ID, db_name, params)
    # Получение и сохранение списков вакансий в базу данных
    vacancy_count = 0
    emp = HhAPI
    for _id in EMPLOYERS_ID:
        fill_vacancies_list = get_vacancies(emp.get_request(_id))
        for _ in fill_vacancies_list:
            vacancy_count += 1
        save_vacancies_to_database(fill_vacancies_list, db_name, params)
    print(f"Итого вакансий: {vacancy_count}.\n"
          f"Вакансии успешно получены и записанны в базу данных!")
    # Запуск цикла операций над данными из базы данных
    while True:
        user_input = input("\n"
                           "1 - Получить список всех копманий и количество их вакансий.\n"
                           "2 - Получить список всех вакансий с указанием названия компании,\n"
                           "    названия вакансии и зарплаты, и ссылки на вакансию.\n"
                           "3 - Получить среднюю зарплату по вакансиям.\n"
                           "4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
                           "5 - Получить список всех вакансий, в названии которых содержится введеное слово.\n"
                           "Чтобы завершить программу введите 'exit'.\n"
                           "Введите номер операции для обработки данных:")

        if user_input == "1":
            DBManager.get_companies_and_vacancies_count()

        elif user_input == "2":
            DBManager.get_all_vacancies()

        elif user_input == "3":
            DBManager.get_avg_salary()

        elif user_input == "4":
            DBManager.get_vacancies_with_higher_salary()

        elif user_input == "5":
            search_word = input("Введите слово для поиска вакансий:").lower()
            DBManager.get_vacancies_with_keyword(search_word)

        elif user_input.lower() == "exit":
            exit()
        else:
            print("Некорректный ввод!\n")


if __name__ == '__main__':
    print("Поиск вакансий на платформе HeadHunter...\n")
    main()
