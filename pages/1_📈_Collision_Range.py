### Contents of pages/Colision_Range.py ###
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns

st.title("Vehicle collisions")

# Leer dataframe
df = pd.read_csv('NYC.csv')

# Distritos sin NaN
dist = list(df['BOROUGH'].dropna().unique())

selected_dist = st.selectbox(
    "What do want the BOROUGH?",
    dist
)

# Muestra caklendario y permite seleccionar
date_ini = st.date_input(
    "Date Inic: ",
     min_value = datetime.date(2010, 1, 1) )

# Input for user
date_end = st.date_input(
    "Date End: ",
     min_value = datetime.date(2010, 1, 1) )

# Filter data for renge date and distrit
date_ini = pd.to_datetime(date_ini, format="%Y-%m-%d") # Conertir a DateTime
date_end = pd.to_datetime(date_end, format="%Y-%m-%d")

df["DATE"] = pd.to_datetime(df["DATE"] , infer_datetime_format=True)

df_acc = df[(df['BOROUGH']==selected_dist)&(df['DATE']>=date_ini)&(df['DATE']<=date_end)]
df_acc.reset_index(drop = True, inplace = True)

if df_acc.shape[0]>0:
    total = [df_acc[col].sum() for col in ['PERSONS INJURED','PERSONS KILLED','PEDESTRIANS INJURED','PEDESTRIANS KILLED','CYCLISTS INJURED','CYCLISTS KILLED','MOTORISTS INJURED','MOTORISTS KILLED']]

    per_acc = total/sum(total)*100
    per_acc = per_acc.round(2)

    col1,col2 = st.columns(2)

    df_ = pd.DataFrame({'Event':['PER-INJURED','PER-KILLED','PED-INJURED','PED-KILLED','CYC-INJURED','CYC-KILLED','MOT-INJURED','MOT-KILLED'],
	               'Perc': per_acc})

    df_.set_index('Event',inplace=True)

    fig, ax = plt.subplots()

    # declaring exploding pie
    explode = [0.2, 0.2,  0.2,  0.2,  0.2, 0.2, 0.2, 0.2]

    # define Seaborn color palette to use
    sns.set_theme(palette="dark", font="serif", font_scale= 0.5)
  
    # plotting data on chart
    ax.pie(df_['Perc'], labels=df_.index, explode=explode, autopct='%.0f%%')

 
    
    # Add Plot Title
    f_ini = str(date_ini.year)+'/'+str(date_ini.month)
    f_end = str(date_end.year)+'/'+str(date_end.month)
    ax.set_title(f'Percentage of persons INJURED/KILLED in district {selected_dist}',fontsize=11,
             loc='left', pad = 20)
    fig.suptitle(f'On dates {f_ini} - {f_end}', y=1, fontsize=9)

    st.pyplot(fig)

st.button("Re-run")

