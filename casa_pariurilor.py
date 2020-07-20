import requests
from bs4 import BeautifulSoup
from time import sleep
import multiprocessing as mp


CHARACTERS = ["1", "X", "2"]


def func(curr_link):
    page = requests.get(curr_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    pretenders = soup.find_all("div")

    team_names = []
    win = [[], [], []]

    for i in pretenders:
        if "class" in i.attrs and "psk-sport-group" in i.attrs["class"]:
            aux = i.find_all("div")
            x = ""
            y = ""
            for j in aux:
                if "class" in j.attrs and "event-header-team" in j.attrs["class"] and "top" in j.attrs["class"]:
                    x = j.string.strip(' \n')
                if "class" in j.attrs and "event-header-team" in j.attrs["class"] and "bottom" in j.attrs["class"]:
                    y = j.string.strip(' \n')
                    if x and y:
                        team_names.append(x)  # numele echipelor
                        team_names.append(y)

            for it, c in enumerate(CHARACTERS):
                for j in aux:
                    if "data-original-title" in j.attrs and j.attrs[
                        "data-original-title"] == c and "data-pick" in j.attrs and j.attrs["data-pick"] == c:
                        win[it].append(j.string.strip(' \n'))
            break

    return (team_names, win)


if __name__ == '__main__':
    main_link = "https://www.casapariurilor.ro/Sport/Fotbal/51?date=sve"
    main_page = requests.get(main_link)
    main_soup = BeautifulSoup(main_page.content, 'html.parser')

    select_soccer = main_soup.find_all("ul")
    links = []
    for i in select_soccer:
        if "class" in i.attrs and "inner-list" in i.attrs["class"]:
            aux = i.find_all("a")
            for j in aux:
                if "href" in j.attrs and j.attrs["href"] != "#":
                    links.append("https://www.casapariurilor.ro/" + j.attrs["href"])
            break

    team_names = []
    win = [[], [], []]

    cpu_count = mp.cpu_count()

    pool = mp.Pool(cpu_count)
    results = pool.map(func, [link for link in links])
    pool.close()

    for team, w in results:
        for elem in team:
            team_names.append(elem)
        for index in range(3):
            for elem in w[index]:
                win[index].append(elem)

    data = {}
    for i in range(0, len(team_names), 2):
        data[(team_names[i], team_names[i + 1])] = (win[0][i // 2], win[1][i // 2], win[2][i // 2])


    fd = open("output", "w")
    fd.write(str(data))