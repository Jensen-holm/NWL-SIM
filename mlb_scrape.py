import scraping_functions

''' URL's used in the funcion '''
default_url = 'https://baseball-reference.com'
league_encyclopedia_url = default_url + '/register/league.cgi'
mlb_start_url = default_url + '/leagues/'

# this is only if data is being pulled from sports reference
# so rn just MLB
def ScrapeSR(sport, league, team1, team2, level):

    team1_name = team1[5:]
    team2_name = team2[5:]
    yr1 = team1[:5]
    yr2 = team2[:5]

    if level == 'mlb':
        # find year links (we need to index these lists)
        yr_link1 = default_url + scraping_functions.find_link(mlb_start_url, yr1)[0]
        yr_link2 = default_url + scraping_functions.find_link(mlb_start_url, yr2)[0]

        # find team links (not sure I am indexing this right)
        team_link1 = scraping_functions.find_link(yr_link1, team1_name)[0]
        team_link2 = scraping_functions.find_link(yr_link2, team2_name)[0]

    else:
        # if its not MLB or Northwoods league (do this later)
        league_link = scraping_functions.find_link(league_encyclopedia_url, level)

    return
