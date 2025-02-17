from Levenshtein import distance

s0 = 5816297

db95 = open("rutemplate.txt", "r")
while True:

    line = db95.readline()
    if not line:
        break
    n = line.strip()

    db = open("ru.txt", "r")

    s1 = 0
    d = []

    while True:
        # считываем строку
        line = db.readline()
        # прерываем цикл, если строка пустая
        if not line:
            break
        # выводим строку
        y = line.strip()
        dist = distance(n, y)
        max_len = max(len(n), len(y))
        if dist/max_len <= 0.3:
            s1 += 1
            if dist/max_len <= 0.15:
                d.append(y)
    print(n)
    print(s1/s0*100)
    print(f'Наиболее похожие варианты: {d}')
