import csv as sv


class Record:
    """

    Class Record принимает лист-строку csv и разбивает её на параметры

    :param arr: list -- Лист-строка из csv файла

    """

    def __init__(self, arr: list):
        self.arr = arr
        self.category: str = arr[0]
        self.product: str = arr[1]
        self.date: Date = Date(arr[2])
        self.ppu: float | int = arr[3]
        self.count: float | int = arr[4]
        self.total: float = float(self.ppu) * float(self.count)

    def __str__(self):
        return str(self.arr)


class Date:
    """

    Class Date принимает строку с датой в формате dd.mm.yyyy и разбивает её на параметры

    :param date: str -- дата в формате строки dd.mm.yyyy

    """

    def __init__(self, date: str):
        dateformat = date.split(".")
        self.date = date
        self.day = dateformat[0]
        self.month = dateformat[1]
        self.year = dateformat[2]

    def __str__(self):
        return f"{self.date}: Day:{self.day} Month:{self.month} Year:{self.year}"


def sort(_records: list):
    """

    Сортирует записи по категории в порядке возрастания через перестановки

    :param _records: list -- Список записей
    :return: list -- Отсортированный список записей

    """
    for i in range(len(_records)):
        current = _records[i]
        lastindex = i - 1
        while lastindex >= 0 and _records[lastindex].category > current.category:
            _records[lastindex + 1] = _records[lastindex]
            lastindex -= 1
        _records[lastindex + 1] = current
    return _records


if __name__ == "__main__":
    #  Открываем оригинальный файл csv
    file = open("products.csv", encoding="utf-8-sig")

    #  Читаем csv файл через csv.reader
    csvfile = sv.reader(file, delimiter=";", quotechar="|")

    #  Создаём новый файл .csv
    newfile = open("products_new.csv", "w", encoding="utf-8-sig")

    #  Инициализируем writer для нового csv файла
    newcsvfile = sv.writer(newfile, delimiter=";", quotechar="|")

    #  Высчитывем total для каждой строки
    records = []
    for record in csvfile:
        if record[0] == "Category":
            record.append("total")
        else:
            rec = Record(record)
            records.append(rec)
            record.append(str(rec.total))
        newcsvfile.writerow(record)

    sortedData = sort(records)

    #  Задание 1 вывод
    #  Высчитывем и выводим итоговую сумму по категории закуски
    summ = 0
    for record in sortedData:
        if record.category == "Закуски":
            summ += record.total

    print(summ)

    #  Задание 2 вывод
    #  Создаем файл с отсортированными строками; выводим самый дорогой товар в первой категории по алфавиту
    newfilesort = open("products_sorted.csv", "w", encoding="utf-8-sig")
    newcsvfilesort = sv.writer(newfilesort, delimiter=";", quotechar="|")
    newcsvfilesort.writerow(["Category", "product", "Price per unit", "Count", "Total"])
    print(
        f"В категории: {sortedData[0].category} самый дорогой товар:{sortedData[0].product} его цена за единицу товара"
        f"составляет {sortedData[0].ppu}")

    #  Циклом записывем всё в новый файл
    for row in sortedData:
        newcsvfilesort.writerow(row.arr)

    #  Задание 3 loop
    while True:
        categ = input("Введите категорию>")
        if categ == "молоко":
            break
        mini = 50000
        minicat = 0
        for record in sortedData:
            if record.category == categ and float(record.count) <= float(mini):
                mini = record.count
                minicat = record

        if mini == 50000:
            print("Такой категории не существует в нашей БД")
        else:
            print(f"В категории:{minicat.category} товар: {minicat.product} был куплен {minicat.count} раз")
            print(minicat)
