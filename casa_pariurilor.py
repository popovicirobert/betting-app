import requests
from bs4 import BeautifulSoup
import multiprocessing as mp


def get_link_data(link, CHARACTERS):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    pretenders = soup.find_all("div")

    teams = []
    coefficients = [[], [], []]

    for element in pretenders:
        if "class" in element.attrs and "psk-sport-group" in element.attrs["class"]:
            child_elements = element.find_all("div")

            team1, team2 = "", ""

            for child in child_elements:
                if "class" in child.attrs and\
                        "event-header-team" in child.attrs["class"] and\
                        "top" in child.attrs["class"]:

                    team1 = child.string.strip(' \n\r')

                if "class" in child.attrs and\
                        "event-header-team" in child.attrs["class"] and\
                        "bottom" in child.attrs["class"]:

                    team2 = child.string.strip(' \n\r')


                    if team1 and team2:
                        teams.append(team1)  # numele echipelor
                        teams.append(team2)


            if team1 and team2: # conditia asta nu era pusa in codul vechi si e importanta!!!

                for index, character in enumerate(CHARACTERS):
                    for child in child_elements:
                        if "data-original-title" in child.attrs and\
                                child.attrs["data-original-title"] == character and\
                                "data-pick" in child.attrs and\
                                child.attrs["data-pick"] == character:

                            coefficients[index].append(child.string.strip(' \n\r'))

            break

    return (teams, coefficients)


class CasaPariurilor:

    def __init__(self):
        self.BASE_URL = "https://www.casapariurilor.ro/"
        self.MAIN_URL = "https://www.casapariurilor.ro/Sport/Fotbal/51?date=sve"

        self.main_page = requests.get(self.MAIN_URL)
        self.main_soup = BeautifulSoup(self.main_page.content, 'html.parser')

        self.CHARACTERS = ["1", "X", "2"]

    def get_links(self):
        soccer = self.main_soup.find_all("ul")
        links = []

        for element in soccer:
            if "class" in element.attrs and "inner-list" in element.attrs["class"]:
                child_elements = element.find_all("a")
                for child in child_elements:
                    if "href" in child.attrs and child.attrs["href"] != "#":
                        links.append(self.BASE_URL + child.attrs["href"])
                break

        return links

    def get_data(self, links):
        teams = []
        coefficients = [[], [], []]

        cpu_count = mp.cpu_count()

        from itertools import repeat

        pool = mp.Pool(cpu_count)
        results = pool.starmap(get_link_data, zip(links, repeat(self.CHARACTERS)))
        pool.close()

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

    site = CasaPariurilor()
    links = site.get_links()
    data = site.get_data(links)
    print(data)


