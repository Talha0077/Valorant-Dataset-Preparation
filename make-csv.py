from bs4 import BeautifulSoup
import pandas as pd
import requests


def update_final_lists(agents, weapons, best_maps, worst_map):
    top_agents_list_final.append(agents)
    top_weapons_list_final.append(weapons)
    top_three_player_maps_final.append(best_maps)
    worst_player_map_final.append(worst_map)


list_of_agents = ['Astra', 'Breach', 'Brimstone', 'Chamber', 'Cypher', 'Jett', 'Fade', 'KAY/O', 'Killjoy', 'Neon', 'Omen', 'Phoenix', 'Raze', 'Reyna', 'Sage', 'Skye', 'Sova', 'Viper', 'Yoru']
list_of_maps = ['Haven', 'Icebox', 'Breeze', 'Fracture', 'Ascent', 'Bind', 'Split', 'Pearl']

main_page = requests.get("https://tracker.gg/valorant/leaderboards/ranked/all/default?page=1&region=global")

main_page_soup = BeautifulSoup(main_page.content, 'html.parser')

leaderboard_table = main_page_soup.find("table", {"class": "trn-table"})

leaderboard_entries = leaderboard_table.find("tbody")

player_list = leaderboard_entries.find_all("td", {"class": "username"})

player_names = []
for player in player_list:
    player_names.append(player.find("span", {"class": "trn-ign__username"}).text.strip())

player_profile_links = []
for player in player_list:
    a_tag = player.find("a")
    link = "https://tracker.gg" + a_tag.get('href') + "/overview?season=all"
    player_profile_links.append(link)


top_agents_list_final = []
top_weapons_list_final = []
top_three_player_maps_final = []
worst_player_map_final = []
rerun_iteration = True
for i, player_profile_link in enumerate(player_profile_links):
    rerun_iteration = True
    top_agents_list = []
    top_weapons_list = []
    top_three_player_maps = []
    worst_player_map = []
    if i == 15:
        break
    while rerun_iteration:
        try:
            print("Gathering data for player", player_profile_link)
            player_profile_page = requests.get(player_profile_link)

            player_profile_page_soup = BeautifulSoup(player_profile_page.content, 'html.parser')

            top_agents = player_profile_page_soup.find_all("div", {"class": "info"})

            for agent in top_agents:
                if agent.text.strip() in list_of_agents:
                    top_agents_list.append(agent.text.strip())

            top_weapons = player_profile_page_soup.find_all("div", {"class": "weapon__name"})

            for weapon in top_weapons:
                top_weapons_list.append(weapon.text.strip())

            top_maps_link = player_profile_page_soup.find("a", {"class": "trn-button trn-button--block"})

            player_maps_link = "https://tracker.gg" + top_maps_link.get('href')

            player_maps_page = requests.get(player_maps_link)

            player_maps_page_soup = BeautifulSoup(player_maps_page.content, 'html.parser')

            players_maps = player_maps_page_soup.find_all('div', {"class": "info"})

            all_maps_list = []
            for map in players_maps:
                if map.text.strip() in list_of_maps:
                    all_maps_list.append(map.text.strip())

            top_three_player_maps = (all_maps_list[0:3])
            worst_player_map = (all_maps_list[-1])
            update_final_lists(top_agents_list, top_weapons_list, top_three_player_maps, worst_player_map)
            rerun_iteration = False
        except:
            print("Error occurred. Retrying...")
            top_agents_list = []
            top_weapons_list = []
            top_three_player_maps = []
            worst_player_map = []
            rerun_iteration = True


print(top_weapons_list_final, len(top_weapons_list_final))
print(top_agents_list_final, len(top_agents_list_final))
print(top_three_player_maps_final, len(top_three_player_maps_final))
print(worst_player_map_final, len(worst_player_map_final))

