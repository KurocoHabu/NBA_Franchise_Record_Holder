import streamlit as st
import pandas as pd

import warnings
warnings.filterwarnings('ignore')


def player_im_merge(df, label):
    player_im = pd.read_csv("data/player_imageURL.csv")
    tmp = df.merge(player_im[["playerName", "image_url"]], left_on=label, right_on="playerName")
    tmp.insert(1, "player_image", tmp["image_url"])
    tmp = tmp.drop("image_url", axis=1)
    tmp = tmp.dropna(how="all", axis=1)


    return tmp


def _stats_calc(df, col, label, top_n, widget_id):
    if label == "PlusMinus-Worst":
        label = "PlusMinus"
        header = "+/- Worst"
    elif label == "PlusMinus-Best":
        label = "PlusMinus"
        header = "+/- Best"
    elif label == "SP":
        header = "MP"
    else:
        header = label
    
    total = df.groupby(["Player"]).agg({label:"sum"}).reset_index()
    image_merge = player_im_merge(total, "Player")
    if label == "PlusMinus-Worst":
        image_merge = image_merge[["player_image", "Player", label]].astype({label: int}).sort_values(label, ascending=True).rename(columns={label: "+/-"}).head(top_n)
    elif label == "PlusMinus-Best":
        image_merge = image_merge[["player_image", "Player", label]].astype({label: int}).sort_values(label, ascending=False).rename(columns={label: "+/-"}).head(top_n)
    elif label == "SP":
        image_merge["MP"] = round(image_merge["SP"] /60).astype(int)
        image_merge = image_merge[["player_image", "Player", "MP"]].astype({"MP": int}).sort_values("MP", ascending=False).head(top_n)
    else:
        image_merge = image_merge[["player_image", "Player", label]].astype({label: int}).sort_values(label, ascending=False).head(top_n)

    with col:        
        st.header(header)
        st.data_editor(image_merge,
                        column_config={
                            "player_image": st.column_config.ImageColumn("image"),
                            "Player": "Player",
                            label : label,                         
                            },
                        key=widget_id,
                        hide_index=True)



def _stats_summary(df, teamabb, top_n=5):  
    widget_id = (id for id in range(24))
      
    if teamabb != "AllTeams":
        df = df[df["teamabb"]==teamabb]
    
    col1, col2, col3, col4 = st.columns(4)
    
    for col, label in zip([col1, col2, col3, col4], ["GP", "GS", "Win", "Lose"]):        
        _stats_calc(df=df, col=col, label=label, top_n=top_n, widget_id=next(widget_id))
        
    col1, col2, col3, col4 = st.columns(4)
    
    for col, label in zip([col1, col2, col3, col4], ["SP", "PTS", "TRB", "AST"]):        
        _stats_calc(df=df, col=col, label=label, top_n=top_n, widget_id=next(widget_id))
        
    col1, col2, col3, col4 = st.columns(4)
    
    for col, label in zip([col1, col2, col3, col4], ["FG", "2P", "3P", "FT"]):        
        _stats_calc(df=df, col=col, label=label, top_n=top_n, widget_id=next(widget_id))
    
    col1, col2, col3, col4 = st.columns(4)
    
    for col, label in zip([col1, col2, col3, col4], ["PlusMinus-Best", "STL", "BLK", "TOV"]):    
        _stats_calc(df=df, col=col, label=label, top_n=top_n, widget_id=next(widget_id))
    
    col1, col2, col3, col4 = st.columns(4)
    
    for col, label in zip([col1, col2, col3, col4], ["PlusMinus-Worst", 'DD', 'TD', 'DD+TD']):    
        _stats_calc(df=df, col=col, label=label, top_n=top_n, widget_id=next(widget_id))
    
    col1, col2, col3, col4 = st.columns(4)
    
    for col, label in zip([col1, col2, col3, col4], ["30+PTS", "40+PTS", "50+PTS", "25P-5R-5A"]):    
        _stats_calc(df=df, col=col, label=label, top_n=top_n, widget_id=next(widget_id))
    
        
        
        
def main():
    st.set_page_config(
        page_title="NBA Every Franchise Leader Board",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    st.title("NBA Every Franchise Leader Board")
        
    bs = pd.read_csv("./data/NBA_Franchise_Record_Holder.csv")
    
    teams = ['ATL', 'BOS', 'BRK', 'CHA', 'CHI', 'CLE',
             'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 
             'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 
             'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 
             'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
    
    team = st.sidebar.selectbox(
        "チームを選択してください",
        teams,
        # "LAL"
    )
    
    if team == "AllTeams":
        st.image('./data/TeamImage/NBA.jpg')
    else:
        st.image('./data/TeamImage/' + team + '.png')
    
    gametype = st.sidebar.selectbox(
        "レギュラーシーズンかプレイオフか",
        ["Regular", "Playoff", "Final", "Allgames"]
    )
    
    if gametype == "Regular":
        df = bs[bs["isRegular"]==1]
    elif gametype == "Playoff":
        df = bs[bs["isPlayoff"]==1]
    elif gametype == "Final":
        df = bs[bs["isFinal"]==1]
    else:
        df = bs
    
    
    top_n = st.sidebar.slider(
        "選手の表示数を選択してください",
        1, 10, 5
    )
    
    _stats_summary(df, teamabb=team, top_n=top_n)
    
    


    
if __name__ == "__main__":
    main()
