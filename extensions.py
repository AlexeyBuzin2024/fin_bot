import requests
import json
from config import keys
class APIException(Exception):                      #класс реакции на ошибки
    pass

class FinConverter:                                     #класс обеспечивающий рассчёт конвертации валюты
    @staticmethod
    def get_price(quote: str, base: str, amount: str):            #метод конвертации
        if quote == base:                                                               #отлавливание ошибки ввода
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')       #одинаковых валют

        try:                                                                            #отлавливание ошибки ввода в
            quote_ticker = keys[quote]                                                  #исходной валюте
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:                                                                            #отлавливание ошибки ввода в
            base_ticker = keys[base]                                                    #конечной валюте
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:                                                                            #отлавливание ошибки ввода в
            amount = float(amount)                                                      #количестве валюты
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

                                                                                                #получение курса
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = round(float(json.loads(r.content)[keys[base]])*float(amount), 2)           #рассчёт конвертации
                                                                                    #валюты, с округлением до второго
                                                                                    #знака после запятой
        return total_base