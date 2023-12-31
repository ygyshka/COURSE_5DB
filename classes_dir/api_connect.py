from classes_dir.db_manager import DBManager
import requests
from typing import Any


EMPLOYERS_ID = {852361: 'Ростелеком - Центры обработки данных',
                36227: '000 МАГАЗИН МАГАЗИНОВ - Эксперт по торговой недвижимости', 1473866: 'Сбербанк-Сервис',
                407: 'Гарант', 2238: 'КонсультантПлюс', 1570067: 'SAMSUNG авторизованный фирменный магазин',
                5920492: 'DNS Головной офис', 165121: 'Toyota & Lexus, Группа компаний ИАТ',
                39209: 'Газпром бурение', 2211644: 'ЮМАТЕКС Росатом'}


class HhAPI:
    """
    Класс для получения запроса к API сайта HeadHunter
    """

    URl_HH = 'https://api.hh.ru/vacancies'

    @staticmethod
    def get_request(employer_ids: int) -> list[dict[str, Any]]:
        """
        Метод отрабатывает запрос пользователя и возвращает ответ API сайта
        :param employer_ids:
        :return:
        """

        params = {
            'page': 0,  # Индекс страницы поиска на HH
            'per_page': 100,  # Кол-во вакансий на 1 странице
            'employer_id': employer_ids
        }

        response = requests.get(HhAPI.URl_HH, params)
        response.close()
        data_get = response.json()['items']
        return data_get


def get_vacancies(data: list[dict]) -> list[DBManager]:
    new_list = []
    for item in data:
        vacancy = DBManager(item['id'],
                            item['employer']['id'],
                            item['name'],
                            item['alternate_url'],
                            item['salary'])
        new_list.append(vacancy)
    return new_list
