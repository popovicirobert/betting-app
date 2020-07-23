
from casa_pariurilor import CasaPariurilor
from fortuna import Fortuna

if __name__ == '__main__':

    sites = []
    sites.append(CasaPariurilor())
    sites.append(Fortuna())

    data_list = []

    for site in sites:
        links = site.get_links()
        data_list.append(site.get_data(links))
        #print(len(data_list[-1]))

    def convert_to_float(string):
        answer = float(string.replace(",", "."))
        return answer

    merged_data = {}
    for data in data_list:
        for match, string_coefficients in data.items():
            if match in merged_data:
                for index, coefficient in enumerate(string_coefficients):
                    merged_data[match][index] = max(float(merged_data[match][index]), convert_to_float(coefficient))
            else:
                coefficients = []
                for index, string in enumerate(string_coefficients):
                    value = convert_to_float(string)
                    coefficients.append(value)
                merged_data[match] = coefficients

    #print(len(merged_data))
    #print(merged_data[('Bayern M.', 'Chelsea')])

    
    import os
    os.system('''g++ -O2 -std=c++11 ./Simplex/Simplex/Main.cpp ./Simplex/Simplex/Simplex.cpp ./Simplex/Simplex/Simplex.h -o ./Simplex/Debug/Simplex.exe''')

    for match, coefficients in merged_data.items():

        #print(match, coefficients)

        os.system(f'(./Simplex/Debug/Simplex.exe {coefficients[0]} {coefficients[1]} {coefficients[2]} 2000) > solutions.txt')

        with open('solutions.txt', 'r') as fd:
            bets = fd.readline().split(' ')
            print(bets)

            sum = 0
            for index in range(3):
                sum += float(bets[index]) * (float(coefficients[index]) - 3)

            average = sum / 3
            if average > 0:
                print(average, match, end = '\n')
     
