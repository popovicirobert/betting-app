import requests
from bs4 import BeautifulSoup
import multiprocessing as mp


def get_link_data(link, CHARACTERS):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    pretenders = soup.find_all("span")

    teams = []
    coefficients = [[], [], []]


    for element in pretenders:
        if "class" in element.attrs and "event-name" in element.attrs["class"]:
            team1, team2 = element.string.split('-')
            team1 = team1.strip(' \n\r')
            team2 = team2.strip(' \n\r')
            if team1 and team2:
                teams.append(team1)
                teams.append(team2)

    if teams:
        pretenders = soup.find_all("a")
        index = 0
        for element in pretenders:
            if "class" in element.attrs and "odds-button" in element.attrs["class"]:
                if index % 6 < 3:
                    coefficients[index % 6].append(element.attrs["data-value"])
                index += 1

    return (teams, coefficients)


class Fortuna:

    def __init__(self):
        self.BASE_URL = "https://efortuna.ro"
        self.MAIN_URL = "https://efortuna.ro/pariuri-online/fotbal"

        self.main_page = requests.get(self.MAIN_URL)
        self.main_soup = BeautifulSoup(self.main_page.content, 'html.parser')

        self.CHARACTERS = ["1", "X", "2"]

    def get_links(self):
        soccer = self.main_soup.find_all("li")
        links = []

        for element in soccer:
            if "id" in element.attrs and "STMRO3" in element.attrs["id"]:
                child_elements = element.find_all("a")
                for child in child_elements:
                    if "href" in child.attrs:
                        links.append(self.BASE_URL + child.attrs["href"])
                break

        links = links[1:] # am scos /fotbal

        return links

    def get_data(self, links):
        teams = []
        coefficients = [[], [], []]

        cpu_count = mp.cpu_count()

        from itertools import repeat

        pool = mp.Pool(cpu_count)
        results = pool.starmap(get_link_data, zip(links, repeat(self.CHARACTERS)))
        pool.close()

        '''for link in links:
            get_link_data(link, self.CHARACTERS)'''

        for team, coefficient in results:
            for name in team:
                teams.append(name)
            for index in range(3):
                for value in coefficient[index]:
                    coefficients[index].append(value)

        try:
            assert(len(teams) % 2 == 0)
            assert(len(coefficients[0]) == len(coefficients[1]))
            assert(len(coefficients[1]) == len(coefficients[2]))
            assert(len(teams) // 2 == len(coefficients[0]))
        except AssertionError:
            print('Soomthing went wrong!')

        data = {}
        for index in range(0, len(teams), 2):
            win_index = index // 2
            data[(teams[index], teams[index + 1])] = (coefficients[0][win_index],
                                                      coefficients[1][win_index],
                                                      coefficients[2][win_index])

        return data



if __name__ == '__main__':

    site = Fortuna()
    links = site.get_links()
    data = site.get_data(links)
    print(data)
