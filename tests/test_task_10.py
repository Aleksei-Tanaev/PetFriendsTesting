from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_add_new_pet_with_different_case(name='МоНсТрУоЗнЫйХрЯк', animal_type='ЖиВоТиНкАрЕдЧаЙщАя',
                                     age='156', pet_photo='images/wheel.bmp'):
    """Проверяем что можно добавить питомца с корректными данными,
    поля name и animal_type состоят из кириллических чередующихся заглуавных и
     строчных символов не менее 12 единиц"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_empty_fields(name='', animal_type='',
                                     age='', pet_photo='images/catty.jpg'):
    """Проверяем что можно добавить питомца с корректными данными,
    поля name, animal_type, age пустые"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_get_all_pets_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос своих питомцев с валидными данными
    возвращает не пустой список."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_without_photo_with_valid_data(name='Котярка', animal_type='Кот',
                                           age='3'):
    """Проверяем возможность добавления питомца без изображения с валидными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_without_photo_with_empty_fields(name='', animal_type='',
                                           age=''):
    """Проверяем возможность добавления питомца без изображения с пустыми полями"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['animal_type'] == animal_type


def test_add_photo_with_valid_data(pet_photo='images/timon.jpg'):
    """Проверяем возможность добавления изображения подходящего формата"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    assert status == 200
    assert result['pet_photo'] != None


def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем что запрос всех питомцев с невалидным api-ключом
    возвращает статус 403"""

    auth_key = {'key': 'v2'}
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403



def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """Проверяем невозможность получения api-ключа незарегистрированным пользователем"""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_add_without_photo_with_negative_age(name='Мурзик', animal_type='Мохнатый Зверь',
                                           age='-10001'):
    """Проверяем невозможность добавления питомца c заведомо невозможным
     значением поля age (отрицательное число). Имеется баг"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_without_photo(auth_key, name, animal_type, age)

    assert status == 400

def test_add_without_photo_with_invalid_age(name='Сохатый', animal_type='Олень',
                                           age='five'):
    """Проверяем невозможность добавления питомца c невалидным значением поля age
    В данном случае имеется баг, т.к. в api-документации указано, что
     поле age принимает только число, отправелена же строка, статус в полученном
      ответе 200, а не ожидаемый 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_without_photo(auth_key, name, animal_type, age)

    assert status == 400


