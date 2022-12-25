import streamlit as st
import pandas as pd
import numpy as np
from serving import ServingClient
from serving import GameClient
import json

st.title("Hockey Visualization App")
sc = ServingClient.ServingClient(ip="127.0.0.1", port=5000)
gc = GameClient.GameClient()

with st.sidebar:
    workspace = st.text_input('Workspace', 'ift-6758-2')
    model = st.text_input('Model', 'xgb-model-5-3-pickle')
    version = st.text_input('Version', '1.0.0')
    if st.button('Get Model'):

        sc.download_registry_model(
            workspace=workspace,
            model=model,
            version=version
        )
        st.write('Downloaded')
    pass


def ping_game_id(game_id):
    with st.container():
        # TODO: Add Game info and predictions
        filepath = gc.get_game(game_id=game_id)
        model_df, last_event_df = gc.ping_game(filepath)

        pass
    with st.container():
        # TODO: Add data used for predictions
        st.subheader("Data used for predictions (and predictions)")
        st.table(model_df)
        pass


with st.container():
    game_id = st.text_input('Game ID', '2022020329')
    if st.button('Ping game'):
        ping_game_id(game_id)
    pass
