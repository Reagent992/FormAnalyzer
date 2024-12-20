correct_dates_format_test_cases = (
    # -
    "1-1-2022",
    "31-12-2022",
    "2022-01-01",
    "2022-1-1",
    # .
    "1.1.1000",
    "01.01.2000",
    "1000.01.01",
    "1000.1.1",
    # :
    "1:1:2022",
    "31:12:2022",
    "2022:12:31",
    "2022:1:1",
    # ,
    "1,1,2022",
    "31,12,2022",
    "2022,12,31",
    "2022,1,1",
    # /
    "1/1/2022",
    "31/12/2022",
    "2022/12/31",
    "2022/1/1",
)

invalid_dates_format_test_cases = (
    # Неполные даты
    "2022",  # Только год
    "2022.12",  # Год и месяц
    "12.2022",  # Месяц и год
    "31",  # Только день
    # Неверные форматы
    "31.12.22",  # Год из двух цифр (нужно 4)
    "2022-13-01",  # Месяц больше 12
    "2022.12.32",  # День больше 31
    "2022.02.30",  # Февраль с 30 днями
    "1000.0.1",  # Неполный месяц
    "1000.01.0",  # Неполный день
    "2022..01",  # Двойной разделитель
    # Лишние символы
    "31.12.2022.",  # Лишняя точка в конце
    "2022.12.31abc",  # Лишние символы
    "abc2022.12.31",  # Лишние символы в начале
    # Полностью некорректные строки
    "invalid_date",  # Несуществующая дата
    "31-31-31",  # Не соответствует формату
    "абвгд",  # Кириллица
    "",  # Пустая строка
)
