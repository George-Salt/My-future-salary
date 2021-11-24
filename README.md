# Сравниваем вакансии программистов

Это программа, которая выводит таблицу с найденными вакансиями и среднюю зарплату по языкам программирования в Москве.

### Как установить

В папке проекта создайте файл `.env` и поместите в него ключ токен от сервиса SuperJob в переменную `SUPERJOB_SECRET_KEY`:
```
SUPERJOB_SECRET_KEY="secretkey"
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Примеры запуска

Для запуска проекта используйте команду в папке проекта:
```
python main.py
```
Сразу результат выводиться не будет. Нужно подождать около 2 минут (программе нужно пройтись по тысячам вакансий, чтобы посчитать среднюю зарплату).

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
