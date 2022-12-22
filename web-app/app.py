import streamlit as st
from nwl_scrape import nwl_id_dict
from nwl_scrape import ScrapeNWL
from objects import NWLTeam
import NWL_functions
from statistics import median, mode
import features
from streamlit_option_menu import option_menu

st.title('Northwoods League Simulation Analysis')

game_scores = []
other_stats = []
extra_inning_games = 0

def Othergame(team1, team2, lineup1, lineup2, pitcher1, pitcher2):

        team1Score = 0
        team2Score = 0
        next_lineup1_list = [0]
        next_lineup2_list = [0]
        results = []

        for i in range(9):
                next_in_line1 = next_lineup1_list[-1]
                runs, new_lineup_index, half_inning_sequence  = NWL_functions.half_inningOther(lineup1, next_in_line1, pitcher2)
                next_lineup1_list.append(new_lineup_index)
                results.append(half_inning_sequence)
                team1Score += runs

                next_in_line2 = next_lineup2_list[-1]
                runs, new_lineup_index, half_inning_sequence = NWL_functions.half_inningOther(lineup2, next_in_line2, pitcher1)
                next_lineup2_list.append(new_lineup_index)
                results.append(half_inning_sequence)
                team2Score += runs

        innings = 9

        # extra innnings
        if team1Score == team2Score:
                while team1Score == team2Score:

                    runs1, new_lineup_index, half_inning_sequence1 = NWL_functions.half_inningOther(lineup1, next_in_line1, pitcher2)
                    next_lineup1_list.append(new_lineup_index)
                    team1Score += runs1

                    runs2, new_lineup_index, half_inning_sequence2 = NWL_functions.half_inningOther(lineup2, next_in_line2, pitcher1)
                    next_lineup2_list.append(new_lineup_index)
                    team2Score += runs2

                    results.append([[half_inning_sequence1], [half_inning_sequence2]])
                    innings += 1

        # determine winner
        if team1Score > team2Score:
            team1.wins += 1
            team2.losses += 1
        elif team1Score < team2Score:
            team1.losses += 1
            team2.wins += 1
            # find the longest game, and most probable scores for each team using this info below
        game_scores.append([team1Score, team2Score, innings])
        other_stats.append(results)

def Simulation(team1, team2, game_func, num_sims):

            # cycle through bullpens as well eventually
                games = 0
                pitcher_index1 = 0
                pitcher_index2 = 0
                for i in range(num_sims // 2):
                    game_func(team1, team2, team1.lineup, team2.lineup, team1.rotation[pitcher_index1], team2.rotation[pitcher_index2])
                    pitcher_index1 += 1
                    pitcher_index2 += 1
                    games += 1

                    if pitcher_index1 == len(team1.rotation):
                        pitcher_index1 = 0
                    if pitcher_index2 == len(team2.rotation):
                        pitcher_index2 = 0

                pitcher_index1 = 0
                pitcher_index2 = 0
                for i in range(num_sims // 2):
                    game_func(team2, team1, team2.lineup, team1.lineup, team2.rotation[pitcher_index2], team1.rotation[pitcher_index1])
                    pitcher_index1 += 1
                    pitcher_index2 += 1
                    games += 1

                    if pitcher_index1 == len(team1.rotation):
                        pitcher_index1 = 0
                    if pitcher_index2 == len(team2.rotation):
                        pitcher_index2 = 0

def Summary(team1, team2):
        st.header('\n\n\n\n- - - - - - - - - - RESULTS - - - - - - - - - -\n\n\n\n')

        st.text(f'\n\n\n-- {team1.team_name} lineup statistics --\n')
        for player in team1.lineup:
            player.rate_stats()

        st.text(f'\n\n\n-- {team1.team_name} rotation statistics --\n')
        for pitcher in team1.rotation:
            pitcher.rate_stats()

        st.text(f'\n\n\n-- {team2.team_name} lineup statistics --\n')
        for player in team2.lineup:
            player.rate_stats()

        st.text(f'\n\n\n-- {team2.team_name} rotation statistics --\n')
        for pitcher in team2.pitchers:
            pitcher.rate_stats()

        st.text('\n\n\n\n - - - WIN PROBABILITY - - -\n')

        st.text(f'{team1.team_name} record: {team1.wins} - {team1.losses}')
        st.text(f'{team2.team_name} record: {team2.wins} - {team2.losses}')

        st.text(f'\n{team1.team_name}: {(team1.wins / (team1.losses + team1.wins)) * 100:.2f}%')
        st.text(f'{team2.team_name}: {(team2.wins / (team2.losses + team2.wins)) * 100:.2f}%')

        mode1 = mode([x[0] for x in game_scores])
        mode2 = mode([x[1] for x in game_scores])
        st.text(f'\nRuns per game for the {team1.team_name}: {sum([x[0] for x in game_scores]) / (team1.wins + team1.losses):.2f}')
        st.text(f'Runs per game for the {team2.team_name}: {sum([x[1] for x in game_scores]) / (team2.wins + team2.losses):.2f}')
        st.text(f'\nMedian Score for the {team1.team_name}: {median([x[0] for x in game_scores])} ')
        st.text(f'Median Score for the {team2.team_name}: {median([x[1] for x in game_scores])}')
        st.text(f'\nMost common score for the {team1.team_name}: {mode([x[0] for x in game_scores])} ({([x[0] for x in game_scores].count(mode1) / len(game_scores)) * 100:.2f}%)')
        st.text(f'Most common score for the {team2.team_name}: {mode([x[1] for x in game_scores])} ({([x[1] for x in game_scores].count(mode2)) / len(game_scores) * 100:.2f}%)')
        st.text(f'\nProbability of the {team1.team_name} shutting out the {team2.team_name}: {([x[1] for x in game_scores].count(0) / len(game_scores)) * 100:.2f}%')
        st.text(f'Probability of the {team2.team_name} shutting out the {team1.team_name}: {([x[0] for x in game_scores].count(0) / len(game_scores)) * 100:.2f}%')
        st.text(f'\nLongest game (currently no extra innings rule): {max([x[2] for x in game_scores])} innings\n')

team_names = [key for key in nwl_id_dict.keys()]

# take in user input
team1_name = st.selectbox('Select Team 1', (team_names))
team2_name = st.selectbox('Select Team 2', (team_names)) # not sure if this reverse will work
lineup_settings = st.selectbox('Lineup Settings (ignore if doing lineup optimizer)', ('Manual', 'Automatic'))
number_sims = st.slider('Number of Simulations (if doing the lineup optimizer, 100 is reccommended)', min_value = 2, max_value = 5000)

init_sim_button = st.button('Initialize Simulation')

if init_sim_button:
    # then we scrape the data and input the user input into the functions
    data1 = ScrapeNWL(team1_name)
    data2 = ScrapeNWL(team2_name)

    team1 = NWLTeam('nwl', lineup_settings, team1_name, data1[0][0], data1[0][1], data1[0][2], data1[0][3])
    team2 = NWLTeam('nwl', lineup_settings, team2_name, data2[0][0], data2[0][1], data2[0][2], data2[0][3])

    Simulation(team1, team2, Othergame, number_sims)
    Summary(team1, team2)
