import json
import requests
from config import keys


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(*args):
        sum_error = ""# Создаем переменную для формирования общей ошибки
        quote, base, amount = args

        #Проверяем условия ошибок и формируем информацию по ним
        if quote in keys and quote == base:
            sum_error += "Названия валют совпадают. Введите разные валюты\n"

        if not quote in keys or not base in keys:
            if quote in keys:
                sum_error += f"Валюты {base} нет в списке валют. Проверьте правильность написания.\n"
            elif base in keys:
                sum_error += f"Валюты {quote} нет в списке валют. Проверьте правильность написания.\n"
            else:
                sum_error += f"Названия обоих валют отсутствую в списке. Проверьте правильность написания.\n"
        #Проверяем последнее условие и вызываем ошибку и выводим окончательную информацию по ошибке
        try:
            amount = float(amount)
        except:
            sum_error += "Неверный формат количества валюты. Третьим элементом введите положительное число./help"
            raise ConvertionException(sum_error)
        else:
            if sum_error:
                sum_error += "/help"
                raise ConvertionException(sum_error)

        #Если ошибок нет делаем запрос
        r = requests.get(
            f"https://exchange-rates.abstractapi.com/v1/live/?api_key=ee7d453209d04b5f8e9f6d8241f2ab81&base={keys[quote]}&target={keys[base]}")
        #Производим расчеты по полученному курсу и возвращаем результат
        total_change = float(amount) * (json.loads(r.content)["exchange_rates"])[keys[base]]
        return total_change
