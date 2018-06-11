# coding: utf-8
import requests


def search_book(keywords):

    params = {
        'countryCode': 'GB',
        'p': keywords,
        'categoryId': [28780, 28763, 28769, 28766, 28770, 28767, 28772, 28773,
                       28775, 28776, 28777, 28778, 28779, 28781, 28782, 27724,
                       28784, 28787, 28785, 28786],  # category of Books
        'app_key': "F2PuHhMGDNK21S0X1iyGeTVB6oHpX2OA"
    }

    r = requests.get(
        url='https://api.indix.com/v2/summary/products?',
        params=params,
        headers={'Content-Type': 'application/json'}
        )

    return r.text

print(search_book('Harry Potter'))