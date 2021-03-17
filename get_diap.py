def get_diap():
    print('Введите начало периода в формате ГГГГ ММ ДД ЧЧ ММ')
    inp = input().split()
    beg = [int(i) for i in inp]
    beg.append(0)
    print('Введите конец периода в формате ГГГГ ММ ДД ЧЧ ММ')
    inp = input().split()
    end = [int(i) for i in inp]
    end.append(0)

    return [beg, end]
