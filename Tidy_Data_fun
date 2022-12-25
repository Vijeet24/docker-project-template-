def get_games_data(start:int, end:int, path:str) -> pd.DataFrame:
    """
    Input:
    start: int, formed using for the start of the year.
    end: int, formed using for the end of the year.
    folder_path: 
    COMPLETE!!!
    """

    max_game_ID = 1272
    max_playoff = 420 #original 398 -> Changed to 420 as it seems that normally they play a 4th round in the final game (7), so it's possible to see 2017030417
    g_t = ['02','03']
    data = {}
    
    if end > 2020:
        raise RuntimeError('End year out of API range')
    for t in g_t:
        if t == '02':
            for year in range(start,end + 1):
                for i in range(1,max_game_ID):
                    path_file = f'{path}/{str(year)}/{str(year) + t +str(i).zfill(4)}.json'
                    url='http://statsapi.web.nhl.com/api/v1/game/'+ str(year) + t +str(i).zfill(4)+'/feed/live'
                    response = requests.get(url)
                    if response.status_code != 404:
                        game_response = requests.get(url)
                        #game_content = json.loads(game_response.content)
                        if not os.path.isfile(path_file):
                            data[str(year) + t +str(i).zfill(4)] = game_response.json()
                            os.makedirs(os.path.dirname(path_file), exist_ok=True)
                            with open(path_file, "w+") as f:
                                json.dump(data[str(year) + t +str(i).zfill(4)], f)
                        elif (os.path.isfile(path_file)):
                            with open(path_file) as f:
                                data[str(year) + t +str(i).zfill(4)] = json.load(f)
                            f.close()
                            continue
                        
                    else:
                        print(f'Status code: {response.status_code} at gameID:{str(year) + t +str(i).zfill(4)}, not found')

        else:
             for year in range(start,end + 1):
                for i in range(111,max_playoff):
                    path_file = f'{path}/{str(year)}/{str(year) + t +str(i).zfill(4)}.json'
                    url='http://statsapi.web.nhl.com/api/v1/game/'+ str(year) + t +str(i).zfill(4)+'/feed/live'
                    response = requests.get(url)
                    if response.status_code != 404:
                        game_response = requests.get(url)
                        if not os.path.isfile(path_file):
                            data[str(year) + t +str(i).zfill(4)] = game_response.json()
                            os.makedirs(os.path.dirname(path_file), exist_ok=True)
                            with open(path_file, "w+") as f:
                                json.dump(data[str(year) + t +str(i).zfill(4)], f)
                        else:
                            with open(path_file) as f:
                                data[str(year) + t +str(i).zfill(4)] = json.load(f)
                            f.close()
                            continue
                        
                    else:
                        print(f'Status code: {response.status_code} at gameID:{str(year) + t +str(i).zfill(4)}, not found')


                            
    
    return pd.DataFrame.from_dict(data)
    
    
    
    
    
    
    
    
    def tidy(df) -> pd.DataFrame:
    """
    Clean the json files downloaded with get_data.py function
    df : pd.DataFrame
    Returns
    pd.DataFrame
        pandas DataFrame of the play-by-play data where each row is an play event.
        with column names:
            events_types: events of the type “shots” and “goals”, missed shots or blocked shots for now.
            DONE game_time: game time/period information
            DONE game_id: game ID
            DONE team_info: team information (which team took the shot)
            DONEis_shot: indicator if its a shot or a goal
            DONEcoordinates_x, coordinates_y: the on-ice coordinates
            DONEshooter_name, goalie_name: the shooter and goalie name (don’t worry about assists for now)
            DONEshot_type: shot type
            ****DONEempty_name: if it was on an empty net
            DONEstrength:  whether or not a goal was at even strength, shorthanded, or on the power play.
    """
    event_idx, period_time, period, game_id, team_away_name, team_home_name, is_goal, coordinate_x,\
     coordinate_y, shot_type, strength, shooter_name, goalie_name, empty_net, team_name = ([] for i in range(15))
    for i in range(df.shape[1]):
        allplays_data = df.iloc[:,i]['liveData']['plays']['allPlays']
        for j in range(len(allplays_data)):
            if(allplays_data[j]['result']['eventTypeId'] == "SHOT" or allplays_data[j]['result']['eventTypeId'] == "GOAL"):
                period.append(allplays_data[j]['about']['period'])
                period_time.append(allplays_data[j]['about']['periodTime'])
                game_id.append(df.iloc[:,i].name)
                event_idx.append(allplays_data[j]['about']['eventIdx'])
                team_away_name.append(df.iloc[:,i]['gameData']['teams']['away']['name'])
                team_home_name.append(df.iloc[:,i]['gameData']['teams']['home']['name'])
                team_name.append(allplays_data[j]['team']['name'])
                is_goal.append(allplays_data[j]['result']['eventTypeId']=="GOAL")
                coordinate_x.append(allplays_data[j]['coordinates']['x'] if  'x' in allplays_data[j]['coordinates'] else np.nan)
                coordinate_y.append(allplays_data[j]['coordinates']['y'] if  'y' in allplays_data[j]['coordinates'] else np.nan)
                shot_type.append(allplays_data[j]['result']['secondaryType'] if 'secondaryType' in allplays_data[j]['result'] else np.nan)
                strength.append(allplays_data[j]['result']['strength']['name'] if allplays_data[j]['result']['eventTypeId'] == "GOAL" else np.nan)
                if (allplays_data[j]['players'][z]['playerType'] == "Shooter" or allplays_data[j]['players'][z]['playerType'] =='Scorer' for z in range(len(allplays_data[j]['players']))):
                    shooter_name.append([allplays_data[j]['players'][z]['player']['fullName'] for z in range(len(allplays_data[j]['players']))][0])
                if (allplays_data[j]['players'][z]['playerType']=="Goalie" for z in range(len(allplays_data[j]['players']))):
                    goalie_name.append([allplays_data[j]['players'][z]['player']['fullName'] for z in range(len(allplays_data[j]['players']))][0])
                empty_net.append(True if 'emptyNet' in allplays_data[j]['result'] and allplays_data[j]['result']['emptyNet']==True else False)

    assert(all(len(lists) == len(game_id) for lists in [event_idx, period_time, period, team_away_name, team_home_name, is_goal, coordinate_x,\
     coordinate_y, shot_type, strength, shooter_name, goalie_name, empty_net, team_name]) )

    df_main = pd.DataFrame(np.column_stack([event_idx, period_time, period, game_id, team_away_name, team_home_name, is_goal, coordinate_x,\
     coordinate_y, shot_type, strength, shooter_name, goalie_name, empty_net, team_name]),
                       columns=['event_idx', 'period_time', 'period', 'game_id', 'team_away_name', 'team_home_name','is_goal', 'coordinate_x',
                        'coordinate_y', 'shot_type', 'strength', 'shooter_name','goalie_name', 'empty_net', 'team_name'])

    return df_main
