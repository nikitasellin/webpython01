# Консольный поисковик.
____
## Задача.
Создать программу поисковик (консольную). Пользователь вводит текст запроса, поисковую систему, количество результатов, рекурсивный поиск или нет, формат вывода.<br>
Программа находит в интернете начиная от стартовой точки все ссылки на веб-странице в заданном количестве (название ссылки и саму ссылку).<br>
В зависимости от выбранного формата вывода сохраняем результат (текст ссылки: ссылка) либо в консоль либо в файл выбранного формата.


## Конфигурация.
При запуске может считывать параметры из командной строки:
```
  -h, --help  Вывод "help"-сообщения и выход
  -q QUERY [QUERY ...], --query QUERY [QUERY ...]  Поисковый запрос
  -y, --yahoo           Search with yahoo  Использовать сервис Yahoo (по умолчанию - Google)
  -c RESULTS_COUNT, --results-count RESULTS_COUNT  Количество результатов поиска (по умолчанию - 10)
  -l LOGFILE, --logfile LOGFILE  Путь к лог-файлу (по умолчанию - вывод в консоль)

```

## Запуск.
Пример:
```
  $ pip3 install -r webpython_hw01/requirements.txt
  $ python3 webpython_hw01/searcher.py -q find me -c 20
```
Протестировано на Python 3.8.3.
Альтернативный вариант для старых систем - запуск через докер.
```
  $ docker build . -t searcher
  $ docker run -it searcher
```
Внутри контейнера:
```
  # searcher -q find me -y -c 20
```

## TODO.
Добавить:
```
  - рекурсивный поиск;
  - выбор формата вывода: текстовый (консоль)/JSON/CSV.
```
