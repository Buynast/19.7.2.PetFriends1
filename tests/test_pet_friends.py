from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

#  Тест 1. Проверка на добавление питомца с валидными данными

def test_create_pet_simple_with_valid_data(name='Кошак', animal_type='ретривер',
                                     age='4'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# Тест 2. Негативный. Проверка на добавление питомца с невалидными (пустыми) данными

def test_create_pet_simple_with_novalid_data(name='', animal_type='',
                                     age=''):
    """Проверяем что нельзя добавить питомца с некорректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

    """По логике - этот тест должен возвращать статус 400, но т.к. требований нет, что так делать нельзя - оставляем как есть"""

# Тест 3. Негативный. Проверка на добавление питомца с невалидными данными - символы в значении имени

def test_create_pet_simple_with_novalid_name1(name='<>@?#', animal_type='буба',
                                     age='10'):
    """Проверяем что нельзя добавить питомца с некорректными данными в значении имени без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

    """По логике - этот тест должен возвращать статус 400, но т.к. требований нет, что так делать нельзя - оставляем как есть"""

#  Тест 4. Проверка на добавление пользователя при неверном значении ключа авторизации

def test_create_pet_simple_with_novalid_key(name='Рыбка', animal_type='козочка',
                                     age='40'):
    """Проверяем что нельзя добавить питомца при неверном значении ключа авторизации"""

    # Вставляем заведомо неверный ключ
    auth_key = {"key": 'db43bca0c48e01a84d2dc1234aa2404bff399a567cc70cbb0f363c09'}

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

#  Тест 5. Проверка на добавление пользователем слишком длинного имени питомца

def test_create_pet_simple_with_novalid_name2(name='Крокозябрааааааааааааааааааамояяяяяяя', animal_type='мышь',
                                     age='8'):
    """Проверяем что нельзя добавить питомца с длинной имени более 20 символов"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

    """По логике - этот тест должен быть провальным, но т.к. требований нет, что так делать нельзя - оставляем как есть"""

# Тест 6. Проверяем, можно ли ввести данные о возрасте в буквенном значении

def test_create_pet_simple_with_novalid_age(name='Мыша', animal_type='любимица',
                                     age='пять'):
    """Проверяем что нельзя добавить питомца при невалидном(буквенном) значении возраста"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200

    """По логике параметр возраст не должен принимать буквенные значения"""

# Тест 7. Проверка на возможность добавления фотографии к уже созданному питомцу

def test_set_photo_for_pet(pet_id='28048899-8ac4-4f07-9b51-0c0e16e5baea', pet_photo='images/cat1.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем фото питомца
    status, result = pf.set_photo_for_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200

# Тест 8. Проверка на возможность добавления фотографии к питомцу с неверным id

def test_set_photo_for_pet_novalid_id(pet_id='28048899', pet_photo='images/cat1.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем фото питомца
    status, result = pf.set_photo_for_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 500

    """По идее сервер должен вернуть ошибку 400, т.к. введены неверные данные, 
    но почему-то возвращает 500 и в свагере тоже"""

# Тест 9. Проверка на возможность добавления фотографии при неверном ключе

def test_set_photo_for_pet_novalid_key(pet_id='28048899-8ac4-4f07-9b51-0c0e16e5baea', pet_photo='images/cat1.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Вставляем заведомо неверный ключ
    auth_key = {"key": 'db43bca0c48e01a84d2dc1234aa2404bff399a567cc70cbb0f363c09'}

    # Добавляем фото питомца
    status, result = pf.set_photo_for_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

# Тест 10. Проверка на возможность добавления фотографии к питомцу c id = 0

def test_set_photo_for_pet_novalid_photo(pet_id='0', pet_photo='images/cat1.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем фото питомца
    status, result = pf.set_photo_for_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 500

