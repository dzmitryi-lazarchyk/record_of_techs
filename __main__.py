from read_data import read_file_techs, read_file_offices, get_id
from write_data import write_file_techs, write_file_offices

file_name_techs = 'techs.txt'
file_name_offices = 'offices.txt'


def delete_by_office(name, techs):
    for printer in techs:
        if techs[printer][2] == name:
            return delete_by_office(name, techs.pop(printer))
        else:
            return techs


def main():
    # Учёт техники в компании, ключ это предмет в компании, значение это список["адрес","человек","id","цена"]
    # вывод информации, перемещение в другое место, перепривяку к другому человеку, удаление, добавление, редактирование
    # сделать словарь для учёта офисов
    exit = True
    while exit:
        choose = int(input("1.Заниматься предметами\n2.Заниматься офисами\n3.ВЫХОД\n-> "))
        if choose == 1:
            while exit:
                choose = int(input(
                    "1.ДОБАВИТЬ\n2.РЕДАКТИРОВАТЬ\n3.УДАЛИТЬ\n4.ПЕРЕМЕЩЕНИЕ\n5.ПЕРЕПРИВЯЗКА\n6.ВЫВОД ВСЕХ\n7.ВЫВОД ТЕХНИКИ В ОФИСЕ\n8.ВЫХОД\n-> "))
                if choose == 1:
                    name = input("Введите название нового товара\n>")
                    adres = input("Введите адрес нового товара\n>")
                    owner = input("Введите нового владельца\n>")
                    specs = input("Введите описание нового товара\n>")
                    new_id = get_id(file_name_techs)
                    try:
                        cost = float(input("Введите цену нового товара\n>").replace(',', '.').strip())
                    except ValueError:
                        print("Некорректный ввод")
                    else:
                        techs = read_file_techs(file_name_techs)
                        techs.update({str(new_id): [name, specs, owner, adres, f'{cost:{2}}']})
                        write_file_techs(techs, file_name_techs)

                elif choose == 2:
                    techs_id = input("Введите id товра\n>")
                    techs = read_file_techs(file_name_techs)
                    if techs_id in techs.keys():
                        try:
                            new_coast = float(input("Введите новую цену товара\n>").replace(',', '.').strip())
                        except ValueError:
                            print("Некорректный ввод")
                        else:
                            techs[techs_id][4] = new_coast
                            write_file_techs(techs, file_name_techs)
                    else:
                        print("Нет такого товара")
                elif choose == 3:
                    techs_id = input("Введите id товара\n>")
                    techs = read_file_techs(file_name_techs)
                    if techs_id in techs.keys():
                        techs.pop(techs_id)
                        write_file_techs(techs, file_name_techs)
                    else:
                        print("Нет такого товара")
                elif choose == 4:
                    techs_id = input("Введите id товара\n>")
                    techs = read_file_techs(file_name_techs)
                    if techs_id in techs.keys():
                        new_adres = input("Введите новый адрес\n>")
                        new_person = input("Введите нового владельца\n>")
                        techs[techs_id][3] = new_adres
                        techs[techs_id][2] = new_person
                        write_file_techs(techs, file_name_techs)
                    else:
                        print("Нет такого товара\n>")
                elif choose == 5:
                    techs_id = input("Введите id товарa\n>")
                    techs = read_file_techs(file_name_techs)
                    if techs_id in techs.keys():
                        new_person = input("Введите нового владельца\n>")
                        techs[techs_id][2] = new_person
                        write_file_techs(techs, file_name_techs)
                    else:
                        print("Нет такого товара")

                elif choose == 6:
                    techs = read_file_techs(file_name_techs)
                    for printer in sorted([int(i) for i in techs.keys()]):
                        printer = str(printer)
                        print(printer, techs[printer][0], techs[printer][1], techs[printer][2], techs[printer][3],
                              techs[printer][4])
                elif choose == 7:
                    name = input("Введите офис\n>")
                    offices = read_file_offices(file_name_offices)
                    if name in offices.keys():
                        print(name, ':')
                        techs = read_file_techs(file_name_techs)
                        for printer in techs.keys():
                            if techs[printer][2] == name:
                                print(f'{printer}:{techs[printer][0]}')
                    else:
                        print("Нет такого офиса")
                elif choose == 8:
                    exit = False
                else:
                    print("Некорректный ввод, повторите попытку")
            exit = True
        elif choose == 2:
            while exit:
                choose = int(input("1.ДОБАВИТЬ\n2.РЕДАКТИРОВАТЬ\n3.УДАЛИТЬ\n4.ВЫВОД ВСЕХ\n5.ВЫХОД\n-> "))
                if choose == 1:
                    name = input("Ввести название\n>")
                    adres = input("Ввести адрес\n>")
                    offices = read_file_offices(file_name_offices)
                    offices.update({name: adres})
                    write_file_offices(offices, file_name_offices)

                elif choose == 2:
                    name = input("Ввести название ")
                    offices = read_file_offices(file_name_offices)
                    if name in offices.keys():
                        new_adres = input("Ввести адрес\n> ")
                        offices[name] = new_adres
                        techs = read_file_techs(file_name_techs)
                        for printer in techs:
                            if techs[printer][2] == name:
                                techs[printer][3] = new_adres
                        write_file_techs(techs, file_name_techs)
                        write_file_offices(offices, file_name_offices)


                    else:
                        print("Нет такого офиса")
                elif choose == 3:
                    name = input("Ввести название\n> ")
                    offices = read_file_offices(file_name_offices)
                    if name in offices.keys():
                        offices.pop(name)
                        techs = read_file_techs(file_name_techs)
                        techs = delete_by_office(name, techs)
                        write_file_techs(techs, file_name_techs)
                        write_file_offices(offices, file_name_offices)

                    else:
                        print("Нет такого офиса")
                elif choose == 4:
                    offices = read_file_offices(file_name_offices)
                    for office in offices:
                        print(f'{office}:{offices[office]}')
                elif choose == 5:
                    exit = False
                else:
                    print("Некорректный ввод, повторите попытку")
            exit = True
        elif choose == 3:
            exit = False
        else:
            print("Некорректный ввод, повторите попытку")


main()
