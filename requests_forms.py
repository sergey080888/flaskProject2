import requests

url = 'http://127.0.0.1:5000/get_form'
params = {'field_name_1': '237264@mail.ru',
          'field_name_2': '+7 999 777 88 99',
          'field_name_3': '2.3.2023',
          'field_name_4': 'rhhttthtt',
          'field_name_5': '2.3.2023'}
response = requests.post(url=url, params=params)

assert response.json() == {"name": "Form template name"}
assert response.status_code == 200
print(response.json())

params_2 = {"field_1": '111@mail.ru',
            "field_2": '+7 444 557 88 99'}
response = requests.post(url=url, params=params_2)
print(response.json())
assert response.json() == {"name": "Form template name2"}
assert response.status_code == 200

params_3 = {"field_2": '+7 444 557 88 99'}
response = requests.post(url=url, params=params_3)
print(response.json())
assert response.json() == {'field_2': 'phone'}
assert response.status_code == 400

params_4 = {"field_222": '+7 444 557 88 99'}
response = requests.post(url=url, params=params_4)
print(response.json())
assert response.json() == {'field_222': 'phone'}
assert response.status_code == 400
