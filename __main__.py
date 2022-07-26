def main():
    # Учёт техники в компании, ключ это предмет в компании, значение это список["адрес","человек","id","цена"]
    # вывод информации, перемещение в другое место, перепривяку к другому человеку, удаление, добавление, редактирование
    # сделать словарь для учёта офисов
    id = 1
    techs={"Монитор":["Одинцова 8","Офис_1",1,400]}
    offices={"Офис_1":"Одинцова 8"}
    exit = True
    while exit:
        choose=int(input("1.Заниматься предметами\n2.Заниматься офисами\n3.ВЫХОД\n-> "))
        if choose ==1:
            while exit:
                choose = int(input("1.ДОБАВИТЬ\n2.РЕДАКТИРОВАТЬ\n3.УДАЛИТЬ\n4.ПЕРЕМЕЩЕНИЕ\n5.ПЕРЕПРИВЯЗКА\n6.ВЫВОД ВСЕХ\n7.ВЫВОД ТЕХНИКИ В ОФИСЕ\n8.ВЫХОД\n-> "))
                if choose == 1:
                    name = input("Введите название нового товара ")
                    adres = input("Введите адрес нового товара ")
                    owner = input("Введите нового владельца ")
                    id+=1
                    new_id = id
                    coast= int(input("Введите цену нового товара "))
                    techs.update({name:[adres,owner,new_id,coast]})
                elif choose == 2:
                    name = input("Введите название товара ")
                    if name in techs.keys():
                        new_coast=int(input("Введите новую цену "))
                        techs[name][3]=new_coast
                    else:
                        print("Нет такого товара")
                elif choose == 3:
                    name =input("Введите название товара ")
                    if name in techs.keys():
                        techs.pop(name)
                    else:
                        print("Нет такого товара")
                elif choose == 4:
                    name = input("Введите товар ")
                    if name in techs.keys():
                        new_adres = input("Введите новый адрес ")
                        new_person = input("Введите нового владельца ")
                        techs[name][0] = new_adres
                        techs[name][1] = new_person
                    else:
                        print("Нет такого товара")
                elif choose == 5:
                    name = input("Введите товар ")
                    if name in techs.keys():
                        new_person = input("Введите нового владельца ")
                        techs[name][1] = new_person
                    else:
                        print("Нет такого товара")

                elif choose == 6:
                    for element in techs:
                        print(element, techs[element][0],techs[element][1],techs[element][2],techs[element][3])
                elif choose==7:
                    name = input("Введите офис")
                    if name in offices.keys():
                        for element in techs.keys():
                            if techs[element][1]==name:
                                print(element,techs[element])
                    else:
                        print("Нет такого офиса")
                elif choose == 8:
                    exit = False
                else:
                    print("Некорректный ввод, повторите попытку")
            exit = True
        elif choose ==2:
            while exit:
                choose = int(input("1.ДОБАВИТЬ\n2.РЕДАКТИРОВАТЬ\n3.УДАЛИТЬ\n4.ВЫВОД ВСЕХ\n5.ВЫХОД\n-> "))
                if choose == 1:
                    name =input("Ввести название ")
                    adres = input("Ввести адрес ")
                    offices.update({name:adres})
                elif choose == 2:
                    name = input("Ввести название ")
                    if name in offices.keys():
                        new_adres = input("Ввести адрес ")
                        offices[name]= new_adres
                        for element in techs:
                            if techs[element][1]==name:
                                techs[element][0]=new_adres
                    else:
                        print("Нет такого офиса")
                elif choose == 3:
                    name = input("Ввести название ")
                    if name in offices.keys():
                        offices.pop(name)

                        for element in techs:
                            if techs[element][1] == name:
                                techs.pop(element)
                    else:
                        print("Нет такого офиса")
                elif choose == 4:
                    for element in offices:
                        print(element,offices[element])
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