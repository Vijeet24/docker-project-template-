from datetime import time
import pandas as pd
import numpy as np
import requests
import json
from ift6758.data.functions import loadstats_pergame
from ift6758.data.tidyData_single import tidyData_single
from ift6758.data.functions import pre_process
import logging
from ift6758.ift6758.client.serving_client import ServingClient

logger = logging.getLogger(__name__)
s = ServingClient()

class GameClient:
    def __init__(self, game_id = 2021020329, G_home = 0,G_away = 0, last_Idx = -1):
        #store the games processed and their last_Idx,xg,teamnames
        self.game_dic = {game_id:(G_home, G_away, last_Idx)}
        # any other potential initialization

    def ping_game(self, game_id):
        d=get_games_data(2016,2022,'/models')
        df=pd.DataFrame.from_dict(d[game_id])
        df2=tidy(df)
        return df2
