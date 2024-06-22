# Интернет-магазин Megano<br>документация


### Оглавление:

1. [Структура проекта](#cтруктура-проекта)
2. [Основные сведения](#основные-сведения)
3. [Приложения](#приложения)
4. [Инструкция по запуску проекта](#инструкция-по-запуску-проекта)
5. [Руководство пользователя](#руководство-пользователя)


## Cтруктура проекта

```
  .
  ├── ./README.md
  ├── ./db.sqlite3
  ├── ./diploma-frontend/
  ├── ./requirements.txt
  ├── ./images/
  ├── ./manage.py
  ├── ./media/
  ├── ./megano/
  │   ├── ./megano/__init__.py
  │   ├── ./megano/asgi.py
  │   ├── ./megano/settings.py
  │   ├── ./megano/urls.py
  │   └── ./megano/wsgi.py
  ├── ./orders/
  │   ├── ./orders/__init__.py
  │   ├── ./orders/admin.py
  │   ├── ./orders/apps.py
  │   ├── ./orders/migrations/
  ├── ./products/
  │   ├── ./products/__init__.py
  │   ├── ./products/admin.py
  │   ├── ./products/apps.py
  │   ├── ./products/cart.py
  │   ├── ./products/migrations/
  │   ├── ./products/models.py
  │   ├── ./products/pagination.py
  │   ├── ./products/serializers.py
  │   ├── ./products/tests.py
  │   ├── ./products/urls.py
  │   └── ./products/views.py
  └── ./profiles
      ├── ./profiles/__init__.py
      ├── ./profiles/admin.py
      ├── ./profiles/apps.py
      ├── ./profiles/models.py
      ├── ./profiles/serializers.py
      ├── ./profiles/tests.py
      ├── ./profiles/urls.py
      ├── ./profiles/views.py
      └── ./profiles/migrations/
```

## Основные сведения


&nbsp;&nbsp;&nbsp;Данный проект представляет собой интернет магазин, в котором администратор может разместить информацию о своём товаре,
а пользователь просмотреть эту информацию, заказать доставку понравившихся товаров, а также оставить отзыв и
поставить оценку по каждому продукту.

&nbsp;&nbsp;&nbsp;Backend разработан на языке программирования **Python 3.11**, с использованием фреймворков **Django версии 4.2**, **DjangoRestFramework версии 3.15**, в качестве базы данных используется СУБД **SQLite 3**


## Приложения


* profiles:
  * регистрация пользователя;
  * изменение данный профиля;
  * изменение пароля;
  * login / logout

| Endpoint          | Метод |
|-------------------|-------|
| /sign-in          | POST  |
| /sign-up          | POST  |
| /sign-out         | POST  |
| /profile          | GET   |
| /profile          | POST  |
| /profile/password | POST  |
| /profile/avatar   | POST  |

* products:
  * список тегов;
  * список категорий и подкатегорий;
  * список всех товаров:
    * спецификации товаров;
    * отзывы о товарах;
  * рекламные баннеры;
  * список лимитных товаров;
  * список популярных товаров;
  * распродажи;
  * корзина покупок

| Endpoint             | Метод  |
|----------------------|--------|
| /categories          | GET    |
| /catalog             | GET    |
| /products/popular    | GET    |
| /products/limited    | GET    |
| /sales               | GET    |
| /banners             | GET    |
| /basket              | GET    |
| /basket              | POST   |
| /basket              | DELETE |
| /tags                | GET    |
| /product/{id}        | GET    |
| /product/{id}/review | POST   |

* orders:
  * создание заказа;
  * просмотр заказа;
  * оплата заказа

| Endpoint     | Метод |
|--------------|-------|
| /orders      | GET   |
| /orders      | POST  |
| /orders/{id} | GET   |
| /orders/{id} | POST  |
| /payment     | POST  |

## Инструкция по запуску проекта


1. Скачайте проект командой *git clone*: `git clone <адрес Git-репозитория>`

2. Измените значение **SECRET_KEY** в файле **megano/.env**: `SECRET_KEY='<ваше значение>'`

3. Установка зависимостей:

    * Перед установкой зависимостей необходимо установить и активировать виртуальное окружения
    * для Windows `python -m venv venv` -> `venv\Script\Activate`
    * Установите зависимости командой `pip install -r requirements.txt`;

4. Установите пакет frontend:
    * Соберите пакет:  директории diploma frontend выполните команду `python setup.py sdist`;
    * Установите пакет: выполните команду `pip install dist/diploma-frontend-0.6.tar.gz`;

5. Выполните миграции: из корня проекта выполните команду `python manage.py migrate`;

6. Запустите проект командой `python manage.py runserver`

## Руководство пользователя


&nbsp;&nbsp;&nbsp;На главной странице сайта пользователь видит рекламные банеры, а также список лимитированных и 
популярных товаров.

![](/images/main_page.png)

&nbsp;&nbsp;&nbsp;Просматривать товары, отзывы и добавлять товары в корзину пользователь может и в режиме гостя, но,
для того чтобы добавить отзыв и оформить заказ необходимо пройти авторизацию. 

![](/images/login.png)

&nbsp;&nbsp;&nbsp;После авторизации можно пройти на страницу своего профиля и настроить его.

![](/images/default.png)
![](/images/user.png)

&nbsp;&nbsp;&nbsp;В каталоге приведён список товаров.

![](/images/catalog.png)

&nbsp;&nbsp;&nbsp;Щелкнув по товару, пользователь переходит на его страницу где можно просмотреть фотографии товара,
его описание и отзывы пользователей. После авторизации есть возможность оставить свой отзыв. Здесь так же можно выбрать
нужное количество товара и добавить в корзину.

![](/images/product.png)
![](/images/review.png)

&nbsp;&nbsp;&nbsp;На странице Sales приведен список товаров со скидкой с информацией о времени проведения акции, 
и старой и новой цены.

![](/images/sales.png)

&nbsp;&nbsp;&nbsp;В корзине приведён список добавленных товаров их стоимость и количество. Количество можно изменить в
большую или меньшую сторону. После авторизации пользователь может оформить заказ.

![](/images/cart.png)

&nbsp;&nbsp;&nbsp;На странице заказа пользователь вводит адрес доставки и выбирает тип оплаты и доставки. После чего 
ему выводится вся информация о заказе с итоговой стоимостью. Кнопка "Оплатить" переводит нас на страницу оплаты. После
чего корзина опустошается

![](/images/order.png)
![](/images/payment.png)
