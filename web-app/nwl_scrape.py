from bs4 import BeautifulSoup
import requests
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=RuntimeWarning)

# maybe we scrape other statistics, and average them out based on home/away, last 10 games, and so on

prefix_rightleft_stats = 'https://scorebook.northwoodsleague.com/reports/vsleftright/13/'
# some of these keys should be fixed
nwl_id_dict = {
      'Jacks':'60',
      'Growlers':'62',
      'Kingfish':'63',
      'Jackrabbits':'73',
      'Rivets':'66',
      'Spitters': '74',
      'Spiders': '70',
      'Rockers':'61',
      'Chinooks': '64',
      'Mallards': '65',
      'Rafters': '67',
      'Woodchucks': '68',
      'Huskies':'51',
      'Express':'52',
      'Loggers':'53',
      'Bucks':'58',
      'Puppies':'83',
      'Larks':'50',
      'Moondogs':'54',
      'Honkers':'55',
      'Rox':'56',
      'Stingers':'59'
      }

def ScrapeNWL(team):
    data = []
    for key, value in nwl_id_dict.items():
        if key == team:
            lst = BeautifulSoup(requests.get(prefix_rightleft_stats + value + '?format=csv').text, features = 'lxml').text.replace('%', '').split('\n')
            batters_vs_rhp = lst[lst.index('INDIVIDUAL BATTING STATS VS RIGHT HANDED PITCHERS') + 2: lst.index('INDIVIDUAL BATTING STATS VS LEFT HANDED PITCHERS') - 6]
            batters_vs_lhp = lst[lst.index('INDIVIDUAL BATTING STATS VS LEFT HANDED PITCHERS') + 2: lst.index('INDIVIDUAL PITCHING STATS VS RIGHT HANDED BATTERS') - 6]
            pitchers_vs_rhh = lst[lst.index('INDIVIDUAL PITCHING STATS VS RIGHT HANDED BATTERS') + 2: lst.index('INDIVIDUAL PITCHING STATS VS LEFT HANDED BATTERS') - 6]
            pitchers_vs_lhh = lst[lst.index('INDIVIDUAL PITCHING STATS VS LEFT HANDED BATTERS') + 2: lst.index('-------------------------------------------------------') - 8]
            hit_cols = [row.split(',') for row in batters_vs_lhp][0]
            pit_cols = [row.split(',') for row in pitchers_vs_lhh][0]
            hit_cols[1] = 'HAND'
            hit_cols[0] = 'STATUS'
            pit_cols[1] = 'HAND'
            pit_cols[0] = 'STATUS'
            vrhp = pd.DataFrame([row.split(',') for row in batters_vs_rhp], columns = hit_cols)
            vlhp = pd.DataFrame([row.split(',') for row in batters_vs_lhp], columns = hit_cols)
            vrhh = pd.DataFrame([row.split(',') for row in pitchers_vs_rhh], columns = pit_cols)
            vlhh = pd.DataFrame([row.split(',') for row in pitchers_vs_lhh], columns = pit_cols)
            data.append([vrhp, vlhp, vrhh, vlhh])

    if len(data) <= 0:
      raise ValueError(f'\nCHECK SPELLING, COULD NOT FIND "{team}".')
      
    return data