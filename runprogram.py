from pip import main

def install(mname):
    main(["install", mname])

#install("requests")
#install("pandas")
#install("numpy")
#install("Pillow")
#install("IPython")
#install("Flask")
#install("BeautifulSoup4")
#install("urllib")


import requests
import json
import pandas as pd
import numpy as np
from io import BytesIO
from PIL import Image
from IPython.core.display import HTML
from flask import Flask, render_template, request
import urllib.request
from bs4 import BeautifulSoup

app = Flask(__name__)

perksversion = "https://ddragon.leagueoflegends.com/api/versions.json"
pv = requests.get(perksversion)
pvdata = pv.json()
version = pvdata[0]
name = ''
apikey = "RGAPI-e89cdf7e-bb01-49c0-8353-93a026ac392a"
startcount = 0
lolname = ''
tagline = ''


def get_result(table:dict, targets:list) -> list[dict]:
  result = list()
  for target in targets:
    if target in table:
      result.append(table[target])
    else:
      print(f"{target} not in table")
  return result


@app.route('/')
def home():

  presentversion = "ver {}".format(version)

  return render_template('home.html', **locals())

@app.route('/summoner', methods=['POST', 'GET'])
def summonersearch():
  global name
  global startcount
  global apikey
  global lolname
  global tagline

  startcount = 0

  if request.method == 'POST':
    apivalue = request.form['apikey']
    apikey = str(apivalue)

  if request.method == 'GET':
    value = request.args['name']
    name = str(value)

  if '-' in name:
    lolname = name[:name.find('-')]
    tagline = name[name.find('-')+1:]
    lolIdUrl = 'https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{}/{}?api_key={}'.format(lolname,tagline,apikey)
    lolIdUrlinfo = requests.get(lolIdUrl)
    lolIdData = lolIdUrlinfo.json()
  else:
    IdUrl = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'.format(name,apikey)
    IdUrlinfo = requests.get(IdUrl)
    IdData = IdUrlinfo.json()
    lolIdData = [0,1]


  if len(IdData) == 1 or len(lolIdData) == 1:
    return render_template('error.html', **locals())
  else:
    Champurl = "https://ddragon.leagueoflegends.com/cdn/{}/data/ko_KR/champion.json".format(version)
    ChampUrlinfo = requests.get(Champurl)
    Champdata = ChampUrlinfo.json()

    ChampList = []

    champkeylist = list(Champdata['data'].keys())
    for i in range(len(champkeylist)):
      ChampList.append(Champdata['data'][champkeylist[i]])

    id_as_key_champ = dict()
    for each in ChampList:
      id_as_key_champ[each['key']] = each

    RANKTYPE_TABLE = {
      'RANKED_SOLO_5x5': '개인/2인랭크',
      'RANKED_FLEX_SR': '자유랭크',
      'CHERRY' : '아레나'
    }

    if '-' in name:
      puuid = lolIdData['puuid']
      IdUrl = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{}?api_key={}'.format(puuid,apikey)
      IdUrlinfo = requests.get(IdUrl)
      IdData = IdUrlinfo.json()
      id = IdData['id']
      name = IdData['name']
    else:
      puuid = IdData['puuid']
      id = IdData['id']
      lolIdUrl = 'https://asia.api.riotgames.com/riot/account/v1/accounts/by-puuid/{}?api_key={}'.format(puuid,apikey)
      lolIdUrlinfo = requests.get(lolIdUrl)
      lolIdData = lolIdUrlinfo.json()
      lolname = lolIdData['gameName']
      tagline = lolIdData['tagLine']

    IdInfoUrl = 'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{}?api_key={}'.format(id, apikey)
    IdInfoinfo = requests.get(IdInfoUrl)
    IdInfoData = IdInfoinfo.json()

    if len(IdInfoData) == 0:
      winrate = '승률 0%'
      wininfo = '0승 0패'
      SummonerRank = 'Unranked'
      SummonerLP = '0 LP'
      profileIconId = IdData['profileIconId']
      SummonerIcon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/profileicon/{}.png'.format(version, profileIconId)
      SummonerName = lolname
      Summonertag = tagline
      tierimg = 'https://cdn.dak.gg/lol/images/tier-emblem/2022/provisional.png'
    else:
      iddata = IdInfoData[0]
      queueType = iddata['queueType']
      RankType =  RANKTYPE_TABLE[queueType]
      if RankType == '아레나':
        iddata = IdInfoData[1]
        queueType = iddata['queueType']
        RankType =  RANKTYPE_TABLE[queueType]
      wr = iddata['wins'] / (iddata['wins'] + iddata['losses']) *100
      winrate = '승률 {:.1f}%'.format(wr)
      wininfo = '{}승 {}패'.format(iddata['wins'],iddata['losses'])
      SummonerRank = '{} {}'.format(iddata['tier'],iddata['rank'])
      SummonerLP = '{} LP'.format(iddata['leaguePoints'])
      profileIconId = IdData['profileIconId']
      SummonerIcon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/profileicon/{}.png'.format(version, profileIconId)
      SummonerName = lolname
      Summonertag = tagline

      if iddata['tier'] == 'PLATINUM':
        tierimg = 'https://cdn.dak.gg/lol/images/tier-emblem/2022/platinum.png'
      elif iddata['tier'] == 'GOLD':
        tierimg = 'https://cdn.dak.gg/lol/images/tier-emblem/2022/gold.png'
      elif iddata['tier'] == 'SILVER':
        tierimg = 'https://cdn.dak.gg/lol/images/tier-emblem/2022/silver.png'
      elif iddata['tier'] == 'DIAMOND':
        tierimg = 'https://cdn.dak.gg/lol/images/tier-emblem/2022/diamond.png'
      elif iddata['tier'] == 'BRONZE':
        tierimg = 'https://cdn.dak.gg/lol/images/tier-emblem/2022/bronze.png'
      elif iddata['tier'] == 'IRON':
        tierimg = 'https://cdn.dak.gg/lol/images/tier-emblem/2022/iron.png'
      elif iddata['tier'] == 'EMERALD':
        tierimg = 'https://cdn.dak.gg/lol/images/tier-emblem/2022/emerald.png'
      elif iddata['tier'] == 'MASTER':
        tierimg = 'https://cdn.dak.gg/lol/images/tier-emblem/2022/master.png'
      elif iddata['tier'] == 'GRANDMASTER':
        tierimg = 'https://cdn.dak.gg/lol/images/tier-emblem/2022/grandmaster.png'
      elif iddata['tier'] == 'CHALLENGER':
        tierimg = 'https://cdn.dak.gg/lol/images/tier-emblem/2022/challenger.png'

    MasteryUrl = 'https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{}/top?count=20&api_key={}'.format(puuid,apikey)
    Masteryinfo = requests.get(MasteryUrl)
    MasteryData = Masteryinfo.json()

    mdata = []
    for i in range(3):
      mdata.append(str(MasteryData[i]['championId']))

    Favoritechamp = get_result(id_as_key_champ, mdata)

    champ1img = 'https://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png'.format(version, Favoritechamp[0]['id'])
    champ2img = 'https://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png'.format(version, Favoritechamp[1]['id'])
    champ3img = 'https://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png'.format(version, Favoritechamp[2]['id'])

    champ1name = Favoritechamp[0]['name']
    champ1level = '숙련도 {}레벨'.format(MasteryData[0]['championLevel'])
    champ1points = '{}점'.format(MasteryData[0]['championPoints'])

    champ2name = Favoritechamp[1]['name']
    champ2level = '숙련도 {}레벨'.format(MasteryData[1]['championLevel'])
    champ2points = '{}점'.format(MasteryData[1]['championPoints'])

    champ3name = Favoritechamp[2]['name']
    champ3level = '숙련도 {}레벨'.format(MasteryData[2]['championLevel'])
    champ3points = '{}점'.format(MasteryData[2]['championPoints'])

    m2data = []
    for i in range(len(MasteryData)):
      m2data.append(str(MasteryData[i]['championId']))

    m2champ = get_result(id_as_key_champ, m2data)

    tagslist = []
    for i in range(len(m2champ)):
      for j in range(len(m2champ[i]['tags'])):
        tagslist.append(m2champ[i]['tags'][j])

    Marksmancount = 0
    Magecount = 0
    Assassincount = 0
    Fightercount = 0
    Supportcount = 0
    Tankcount = 0

    for i in range(len(tagslist)):
      if tagslist[i] == 'Marksman':
        Marksmancount += 1
      elif tagslist[i] == 'Assassin':
        Assassincount += 1
      elif tagslist[i] == 'Mage':
        Magecount += 1
      elif tagslist[i] == 'Fighter':
        Fightercount += 1
      elif tagslist[i] == 'Support':
        Supportcount += 1
      elif tagslist[i] == 'Tank':
        Tankcount += 1

    Marksmanrate = '{:.1f}%'.format(Marksmancount/len(tagslist)*100)
    Magerate = '{:.1f}%'.format(Magecount/len(tagslist)*100)
    Assassinrate = '{:.1f}%'.format(Assassincount/len(tagslist)*100)
    Fighterrate = '{:.1f}%'.format(Fightercount/len(tagslist)*100)
    Supportrate = '{:.1f}%'.format(Supportcount/len(tagslist)*100)
    Tankrate = '{:.1f}%'.format(Tankcount/len(tagslist)*100)



    RankerUrl = "https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/CHALLENGER/I?page=1&api_key={}".format(apikey)
    RankerInfo = requests.get(RankerUrl)
    RankerData = RankerInfo.json()

    Ranker1name = RankerData[0]['summonerName']
    Ranker1tier = RankerData[0]['tier']
    Ranker1winrate = '{:.1f} %'.format(RankerData[0]['wins'] / (RankerData[0]['wins'] + RankerData[0]['losses']) *100)
    Ranker1LP = RankerData[0]['leaguePoints']

    Ranker2name = RankerData[1]['summonerName']
    Ranker2tier = RankerData[1]['tier']
    Ranker2winrate = '{:.1f} %'.format(RankerData[1]['wins'] / (RankerData[1]['wins'] + RankerData[1]['losses']) *100)
    Ranker2LP = RankerData[1]['leaguePoints']

    Ranker3name = RankerData[2]['summonerName']
    Ranker3tier = RankerData[2]['tier']
    Ranker3winrate = '{:.1f} %'.format(RankerData[2]['wins'] / (RankerData[2]['wins'] + RankerData[2]['losses']) *100)
    Ranker3LP = RankerData[2]['leaguePoints']

    Ranker4name = RankerData[3]['summonerName']
    Ranker4tier = RankerData[3]['tier']
    Ranker4winrate = '{:.1f} %'.format(RankerData[3]['wins'] / (RankerData[3]['wins'] + RankerData[3]['losses']) *100)
    Ranker4LP = RankerData[3]['leaguePoints']

    Ranker5name = RankerData[4]['summonerName']
    Ranker5tier = RankerData[4]['tier']
    Ranker5winrate = '{:.1f} %'.format(RankerData[4]['wins'] / (RankerData[4]['wins'] + RankerData[4]['losses']) *100)
    Ranker5LP = RankerData[4]['leaguePoints']

    return render_template('summonersearch.html', **locals())


@app.route('/json', methods=['POST', 'GET'])
def give_json():
  global startcount
  endcount = 5
  if request.method == 'GET':
    value = request.args['morecount']
    startcount += int(value)

  perksversion = "https://ddragon.leagueoflegends.com/api/versions.json"
  pv = requests.get(perksversion)
  pvdata = pv.json()

  version = pvdata[0]

  luneinfo = 'https://ddragon.leagueoflegends.com/cdn/{}/data/ko_KR/runesReforged.json'.format(version)
  linfo = requests.get(luneinfo)
  lunedata = linfo.json()

  dominate = list()
  inspire = list()
  detail = list()
  resolution = list()
  magic = list()
  for i in range(len(lunedata[0]['slots'])):
    dominate += lunedata[0]['slots'][i]['runes']
  for i in range(len(lunedata[1]['slots'])):
    inspire += lunedata[1]['slots'][i]['runes']
  for i in range(len(lunedata[2]['slots'])):
    detail += lunedata[2]['slots'][i]['runes']
  for i in range(len(lunedata[3]['slots'])):
    resolution += lunedata[3]['slots'][i]['runes']
  for i in range(len(lunedata[4]['slots'])):
    magic += lunedata[4]['slots'][i]['runes']

  lune = dominate + inspire + detail + resolution + magic

  id_as_key_lune = dict()
  for each in lune:
    id_as_key_lune[each['id']] = each

  Champurl = "https://ddragon.leagueoflegends.com/cdn/{}/data/ko_KR/champion.json".format(version)
  ChampUrlinfo = requests.get(Champurl)
  Champdata = ChampUrlinfo.json()

  ChampList = []

  champkeylist = list(Champdata['data'].keys())
  for i in range(len(champkeylist)):
    ChampList.append(Champdata['data'][champkeylist[i]])

  id_as_key_champ = dict()
  for each in ChampList:
    id_as_key_champ[each['key']] = each


  spellinfo = 'https://ddragon.leagueoflegends.com/cdn/{}/data/ko_KR/summoner.json'.format(version)
  sinfo = requests.get(spellinfo)
  spelldata = sinfo.json()

  spellList = []

  spellkeylist = list(spelldata['data'].keys())
  for i in range(len(spellkeylist)):
    spellList.append(spelldata['data'][spellkeylist[i]])


  id_as_key_spell = dict()
  for each in spellList:
    id_as_key_spell[each['key']] = each

  RANKTYPE_TABLE = {
    'RANKED_SOLO_5x5': '개인/2인랭크',
    'RANKED_FLEX_SR': '자유랭크',
    'CHERRY' : '아레나'
  }

  LUNESTYLE_TABLE = {
    8100: '7200_Domination',
    8400: '7204_Resolve',
    8000: '7201_Precision',
    8200: '7202_Sorcery',
    8300: '7203_Whimsy',
  }

  RESULT_TABLE = {
      1: '승리',
      0: '패배'
  }

  QUEUE_TABLE = {
      420 : '솔랭',
      430 : '일반게임',
      440 : '자유랭크',
      490 : '일반게임',
      450 : '무작위 총력전',
      1700 : '아레나'
  }

  IdUrl = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'.format(name,apikey)
  IdUrlinfo = requests.get(IdUrl)
  IdData = IdUrlinfo.json()
  puuid = IdData['puuid']
  id = IdData['id']


  MatchUrl = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?start={}&count={}&api_key={}'.format(puuid, startcount, endcount, apikey)
  Matchinfo = requests.get(MatchUrl)
  MatchData = Matchinfo.json()

  RecordList = []
  for i in range(len(MatchData)):
    RecordList.append('https://asia.api.riotgames.com/lol/match/v5/matches/{}?api_key={}'.format(MatchData[i], apikey))

  RecordinfoList = [[0 for k in range(20)] for l in range(len(RecordList))]
  wincount = 0
  losscount = 0
  nonecount = 0
  for i in range(len(RecordList)):
    Recordinfo = requests.get(RecordList[i])
    RecordData = Recordinfo.json()
    MyInfo = RecordData['info']['participants']
    Metadata = RecordData['metadata']['participants']
    MyRecordData = MyInfo[Metadata.index(puuid)]
    Myperks = MyRecordData['perks']
    MyQueue = RecordData['info']['queueId']
    QueueType = QUEUE_TABLE[MyQueue]
    
    if QueueType == '아레나':
      championName = MyRecordData['championName']
      championIcon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png'.format(version, championName)

      individualPosition = 'None'

      SpellList = []
      SpellList.append(str(MyRecordData['summoner1Id']))
      SpellList.append(str(MyRecordData['summoner2Id']))

      Spell = get_result(id_as_key_spell, SpellList)
      Spell1icon='https://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}.png'.format(version, Spell[0]['id'])
      Spell2icon='https://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}.png'.format(version, Spell[1]['id'])

      MainLuneicon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/spell/Summoner_UltBookPlaceholder.png'.format(version)
      SubLuneicon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/spell/Summoner_UltBookPlaceholder.png'.format(version)

      TotalMinion = MyRecordData['totalMinionsKilled'] + MyRecordData['neutralMinionsKilled']

      Kda = summonerwininfo = '{} / {} / {}'.format(MyRecordData['kills'],MyRecordData['deaths'],MyRecordData['assists'])

      if MyRecordData['deaths'] == 0:
        GPA = 'Perfect'
      else:
        GPA = round((MyRecordData['kills']+MyRecordData['assists'])/MyRecordData['deaths'],1)

      if MyRecordData['item0'] == 0:
        MyRecordData['item0'] = 7050
      if MyRecordData['item1'] == 0:
        MyRecordData['item1'] = 7050
      if MyRecordData['item2'] == 0:
        MyRecordData['item2'] = 7050
      if MyRecordData['item3'] == 0:
        MyRecordData['item3'] = 7050
      if MyRecordData['item4'] == 0:
        MyRecordData['item4'] = 7050
      if MyRecordData['item5'] == 0:
        MyRecordData['item5'] = 7050

      Item1icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item0'])
      Item2icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item1'])
      Item3icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item2'])
      Item4icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item3'])
      Item5icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item4'])
      Item6icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item5'])
      Item7icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item6'])

      nonecount += 1

      Result = RESULT_TABLE[MyRecordData['win']*1]

      Level = MyRecordData['champLevel']

      time = RecordData['info']['gameDuration']
      second = time%60
      minute = (time//60)%60

      playtime = '{}:{}'.format(minute, second)

      TeamList = []
      Teamchamp = []

      for m in range(len(MyInfo)):
        Teamchamp.append('https://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png'.format(version, MyInfo[m]['championName']))
        TeamList.append(MyInfo[m]['summonerName'])


      RecordinfoList[i][0] = championIcon
      RecordinfoList[i][1] = MainLuneicon
      RecordinfoList[i][2] = SubLuneicon
      RecordinfoList[i][3] = Spell1icon
      RecordinfoList[i][4] = Spell2icon
      RecordinfoList[i][5] = TotalMinion
      RecordinfoList[i][6] = Kda
      RecordinfoList[i][7] = Item1icon
      RecordinfoList[i][8] = Item2icon
      RecordinfoList[i][9] = Item3icon
      RecordinfoList[i][10] = Item4icon
      RecordinfoList[i][11] = Item5icon
      RecordinfoList[i][12] = Item6icon
      RecordinfoList[i][13] = Item7icon
      RecordinfoList[i][14] = Result
      RecordinfoList[i][15] = QueueType
      RecordinfoList[i][16] = individualPosition
      RecordinfoList[i][17] = GPA
      RecordinfoList[i][18] = Level
      RecordinfoList[i][19] = playtime

      for n in range(len(Teamchamp)):
        RecordinfoList[i].append(Teamchamp[n])
      RecordinfoList[i].append('https://ddragon.leagueoflegends.com/cdn/{}/img/spell/Summoner_UltBookPlaceholder.png'.format(version))
      RecordinfoList[i].append('https://ddragon.leagueoflegends.com/cdn/{}/img/spell/Summoner_UltBookPlaceholder.png'.format(version))

      for b in range(len(Teamchamp)):
        RecordinfoList[i].append(TeamList[b])
      RecordinfoList[i].append('None')
      RecordinfoList[i].append('None')
      
      RecordinfoList[i].append('transition-color flex w-full flex-none flex-col border-l-8 bg-opacity-10 duration-300 dark:bg-opacity-[0.15] desktop:h-30 desktop:w-[95%] desktop:border-l-4 desktop:py-3 desktop:pl-4 desktop:pr-4 border-ui-bl-base dark:border-psbl-deep bg-ui-bl-base dark:bg-psbl-deep')
      RecordinfoList[i].append('text-xs font-bold uppercase desktop:text-sm text-ui-bl-base dark:text-dark-ui-bl-base')
    else:
      championName = MyRecordData['championName']
      championIcon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png'.format(version, championName)

      individualPosition = MyRecordData['individualPosition']

      Mainlunestyle = Myperks['styles'][0]['style']
      Sublunestyle = Myperks['styles'][1]['style']

      MainLunestyle = LUNESTYLE_TABLE[Mainlunestyle]
      SubLunestyle = LUNESTYLE_TABLE[Sublunestyle]

      MainLuneinfo = Myperks['styles'][0]['selections'][0]['perk']

      Mainluneinfo = []
      Subluneinfo = []
      for k in range(4):
        Mainluneinfo.append(Myperks['styles'][0]['selections'][k]['perk'])
      for j in range(2):
        Subluneinfo.append(Myperks['styles'][1]['selections'][j]['perk'])

      MainLune = get_result(id_as_key_lune, Mainluneinfo)
      MainLuneicon = 'https://ddragon.leagueoflegends.com/cdn/img/{}'.format(MainLune[0]['icon'])

      SubLune = get_result(id_as_key_lune, Subluneinfo)
      SubLuneicon = 'https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/{}.png'.format(SubLunestyle)

      SpellList = []
      SpellList.append(str(MyRecordData['summoner1Id']))
      SpellList.append(str(MyRecordData['summoner2Id']))

      Spell = get_result(id_as_key_spell, SpellList)
      Spell1icon='https://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}.png'.format(version, Spell[0]['id'])
      Spell2icon='https://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}.png'.format(version, Spell[1]['id'])

      TotalMinion = MyRecordData['totalMinionsKilled'] + MyRecordData['neutralMinionsKilled']

      Kda = summonerwininfo = '{} / {} / {}'.format(MyRecordData['kills'],MyRecordData['deaths'],MyRecordData['assists'])

      if MyRecordData['deaths'] == 0:
        GPA = 'Perfect'
      else:
        GPA = round((MyRecordData['kills']+MyRecordData['assists'])/MyRecordData['deaths'],1)

      if MyRecordData['item0'] == 0:
        MyRecordData['item0'] = 7050
      if MyRecordData['item1'] == 0:
        MyRecordData['item1'] = 7050
      if MyRecordData['item2'] == 0:
        MyRecordData['item2'] = 7050
      if MyRecordData['item3'] == 0:
        MyRecordData['item3'] = 7050
      if MyRecordData['item4'] == 0:
        MyRecordData['item4'] = 7050
      if MyRecordData['item5'] == 0:
        MyRecordData['item5'] = 7050

      Item1icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item0'])
      Item2icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item1'])
      Item3icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item2'])
      Item4icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item3'])
      Item5icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item4'])
      Item6icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item5'])
      Item7icon = 'https://ddragon.leagueoflegends.com/cdn/{}/img/item/{}.png'.format(version, MyRecordData['item6'])

      if MyRecordData['win']*1 == 1:
        wincount += 1
      else:
        losscount += 1

      Result = RESULT_TABLE[MyRecordData['win']*1]

      Level = MyRecordData['champLevel']

      time = RecordData['info']['gameDuration']
      second = time%60
      minute = (time//60)%60

      playtime = '{}:{}'.format(minute, second)

      TeamList = []
      Teamchamp = []

      for m in range(len(MyInfo)):
        Teamchamp.append('https://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png'.format(version, MyInfo[m]['championName']))
        TeamList.append(MyInfo[m]['summonerName'])


      RecordinfoList[i][0] = championIcon
      RecordinfoList[i][1] = MainLuneicon
      RecordinfoList[i][2] = SubLuneicon
      RecordinfoList[i][3] = Spell1icon
      RecordinfoList[i][4] = Spell2icon
      RecordinfoList[i][5] = TotalMinion
      RecordinfoList[i][6] = Kda
      RecordinfoList[i][7] = Item1icon
      RecordinfoList[i][8] = Item2icon
      RecordinfoList[i][9] = Item3icon
      RecordinfoList[i][10] = Item4icon
      RecordinfoList[i][11] = Item5icon
      RecordinfoList[i][12] = Item6icon
      RecordinfoList[i][13] = Item7icon
      RecordinfoList[i][14] = Result
      RecordinfoList[i][15] = QueueType
      RecordinfoList[i][16] = individualPosition
      RecordinfoList[i][17] = GPA
      RecordinfoList[i][18] = Level
      RecordinfoList[i][19] = playtime

      for n in range(len(Teamchamp)):
        RecordinfoList[i].append(Teamchamp[n])

      for b in range(len(Teamchamp)):
        RecordinfoList[i].append(TeamList[b])

      if Result == '승리':
        RecordinfoList[i].append('transition-color flex w-full flex-none flex-col border-l-8 bg-opacity-10 duration-300 dark:bg-opacity-[0.15] desktop:h-30 desktop:w-[95%] desktop:border-l-4 desktop:py-3 desktop:pl-4 desktop:pr-4 border-ui-bl-base dark:border-psbl-deep bg-ui-bl-base dark:bg-psbl-deep')
        RecordinfoList[i].append('text-xs font-bold uppercase desktop:text-sm text-ui-bl-base dark:text-dark-ui-bl-base')
      else:
        RecordinfoList[i].append('transition-color flex w-full flex-none flex-col border-l-8 bg-opacity-10 duration-300 dark:bg-opacity-[0.15] desktop:h-30 desktop:w-[95%] desktop:border-l-4 desktop:py-3 desktop:pl-4 desktop:pr-4 border-ui-rd-base dark:border-dark-ui-rd-base bg-psrd-light dark:bg-dark-ui-rd-base')
        RecordinfoList[i].append('text-xs font-bold uppercase desktop:text-sm text-ui-rd-base dark:text-dark-ui-rd-base')

  return json.dumps(RecordinfoList)

@app.route('/rotationjson')
def give_rotationjson():
  global version

  rotationurl = "https://kr.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={}".format(apikey)
  rotationinfo = requests.get(rotationurl)
  rotationdata = rotationinfo.json()

  RotationData = []
  for i in range(len(rotationdata['freeChampionIds'])):
    RotationData.append(str(rotationdata['freeChampionIds'][i]))

  Champurl = "https://ddragon.leagueoflegends.com/cdn/{}/data/ko_KR/champion.json".format(version)
  ChampUrlinfo = requests.get(Champurl)
  Champdata = ChampUrlinfo.json()

  ChampList = []

  champkeylist = list(Champdata['data'].keys())
  for i in range(len(champkeylist)):
    ChampList.append(Champdata['data'][champkeylist[i]])

  id_as_key_champ = dict()
  for each in ChampList:
    id_as_key_champ[each['key']] = each

  RotationChamp = get_result(id_as_key_champ, RotationData)

  RotationinfoList = [[0 for k in range(8)] for l in range(len(RotationChamp))]
  for i in range(len(RotationChamp)):
    Championimage = 'https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}_0.jpg'.format(RotationChamp[i]['id'])
    RotationinfoList[i][0] = RotationChamp[i]['name']
    RotationinfoList[i][1] = RotationChamp[i]['title']
    RotationinfoList[i][2] = Championimage
    RotationinfoList[i][3] = RotationChamp[i]['stats']['hp']
    RotationinfoList[i][4] = RotationChamp[i]['stats']['mp']
    RotationinfoList[i][5] = RotationChamp[i]['stats']['armor']
    RotationinfoList[i][6] = RotationChamp[i]['stats']['spellblock']
    RotationinfoList[i][7] = RotationChamp[i]['info']['difficulty']
    if len(RotationChamp[i]['tags'])==2:
      RotationinfoList[i].append(RotationChamp[i]['tags'][0])
      RotationinfoList[i].append(RotationChamp[i]['tags'][1])
    else:
      RotationinfoList[i].append(RotationChamp[i]['tags'][0])
      RotationinfoList[i].append('None')
    RotationinfoList[i].append(RotationChamp[i]['blurb'])


  return json.dumps(RotationinfoList)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
