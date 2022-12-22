import itertools
import streamlit as st

'''
TO DO:
 - give situational lineups the option of saving as the most recent (probably to txt)
   and be able to use old lineups so we do not have to manually set it up every single time
'''

def OptLineup(team_roster, opposing_pitcher, half_inning_func):
        num_sims = int(st.text_input('\nNUMBER OF SIMULATIONS PER LINEUP: '))
        combos = list(itertools.combinations(team_roster, 9))
        st.text(f"\nTESTING ALL {len(combos):,} POSSIBLE LINEUP COMBINATIONS ({num_sims * len(combos):,} total baseball games)...\n")
        lineup_scores = []
        my_bar = st.progress(0)
        for combo in combos:
                team1Score = 0
                for j in range(num_sims):
                    next_lineup1_list = [0]
                    results = []
                    for i in range(9):
                        next_in_line1 = next_lineup1_list[-1]
                        runs, new_lineup_index, half_inning_sequence  = half_inning_func(combo, next_in_line1, opposing_pitcher, vis = 'n')
                        next_lineup1_list.append(new_lineup_index)
                        results.append(half_inning_sequence)
                        team1Score += runs
                lineup_scores.append([team1Score, combo])

        best_lineup = sorted(lineup_scores, key = lambda x: x[0], reverse = True)
        st.text('\n - - TOP 10 LINEUPS - -')
        for i in range(10):
            for player in best_lineup[i][1]:
                player.rate_stats()
            st.text(f'\nScored {best_lineup[i][0] / num_sims:.2f} runs per game in {num_sims} games versus {opposing_pitcher.Name}\n\n')
