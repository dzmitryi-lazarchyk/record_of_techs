from read_data import read_file_offices


def write_file_techs(techs: dict, file_name_techs: str = 'techs.txt'):
    with open(file_name_techs, 'w', encoding='utf-8') as file:
        for printer in sorted([int(i) for i in techs.keys()]):
            printer = str(printer)
            file.write(
                '{}|{}|{}|{}|{}|{}\n'.format(printer, techs[printer][0], techs[printer][1], techs[printer][2],
                                             techs[printer][3], techs[printer][4]))

def write_file_offices(offices: dict, file_name_offices: str = 'offices.txt'):
    with open(file_name_offices, 'w', encoding='utf-8') as file:
        for office in sorted(offices.keys()):
            office = str(office)
            file.write(
                '{}|{}\n'.format(office, offices[office]))
