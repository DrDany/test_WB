# Test task for WB

## Specification

Используя любой язык программирования необходимо написать следующие автотесты для сайта https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all

1. Вывести все строки таблицы *Customers* и убедиться, что запись с ContactName равной 'СGiovanni Rovelli' имеет Address = 'Via Ludovico il Moro 22'.

2. Вывести только те строки таблицы *Customers*, где city='London'. Проверить, что в таблице ровно 6 записей.

3. Добавить новую запись в таблицу *Customers* и проверить, что эта запись добавилась.

4. Обновить все поля (кроме CustomerID) в любой записи таблицы *Customers*и проверить, что изменения записались в базу.

5. Придумать собственный автотест и реализовать (тут все ограничивается только вашей фантазией).

Заполнить поле ввода можно с помощью js кода, используя объект window.editor.

Требования:
- Для реализации обязательно использовать Selenium WebDriver
- Код автотестов нужно выложить в любой git-репозиторий


## Make virtualenv and install requirements:
    
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run test
### This test works only with ```Chrome``` browser
```shell
pytest test_wb.py
```
