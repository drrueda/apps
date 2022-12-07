### Contents of pages/Colision_Range.py ###
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

st.title("Vehicle collisions")

# Leer dataframe
df = pd.read_csv('NYC.csv')

# Los Factores y los eventos
factor = ['VEHICLE 1 FACTOR','VEHICLE 2 FACTOR', 'VEHICLE 3 FACTOR', 'VEHICLE 4 FACTOR', 'VEHICLE 5 FACTOR']
event = ['PERSONS INJURED','PEDESTRIANS INJURED','CYCLISTS INJURED','MOTORISTS INJURED']

# Factores unicos
uniques = []
for f in factor:
    uniq = list(df[f].dropna().unique())
    uniq.remove('UNSPECIFIED')
    for u in uniq:
        if u not in uniques:
            uniques.append(u)

# Seleccionamos los ventos principales
df['Event'] = np.nan
for index,row in df.iterrows():
    for f in factor:
        if row[f] not in ['UNSPECIFIED',np.nan]:
            df.loc[index,'Event'] = row[f]
            break

# Filtramos por los eventos eliminando los NaN
df_ = df[~df['Event'].isna()]
df_.reset_index(drop=True,inplace = True)

col1,col2 = st.columns(2)

# Obtenemos el total de ocurrencias por evento y factor
df_factor = df_.groupby(['Event'])[event].sum()

# Obtenemos el numero de ocurrencias de cada factor
df_factor['counts'] = df_.groupby(['Event']).size()

# Ordenmaos por numero de ocurrencias de cada factor y ordenamos de mayor a menor 
df_factor = df_factor.reset_index().sort_values(by='counts',ascending = False).reset_index(drop = True)

# Nos quedamos con los 5 primeros factores mas frecuentes
df_factor = df_factor.iloc[0:5]

# El grafico
fig, ax = plt.subplots()

n = len(df_factor.index)
x = np.arange(n)
width = 0.2

ax.bar(x - width,df_factor[event[0]],width=width, label=event[0])
ax.bar(x,df_factor[event[1]],width=width, label=event[1])
ax.bar(x+width,df_factor[event[2]],width=width, label=event[2])
ax.bar(x+width*2,df_factor[event[3]],width=width, label=event[3])
#ax.bar(x+width*3,df_factor[event[4]],width=width, label=event[4])

plt.xticks(x,df_factor['Event'],rotation = 90 )
plt.legend(loc='best')

ax.set_title(f'Main five factors',fontsize=12,
             loc='left', pad = 20)
fig.suptitle(f'Numbers of persons INJURED', y=1, fontsize=10)

st.pyplot(fig)

#st.title(f'Percentage of accidents in district {selected_dist} on dates {str(date_ini.year)} - {str(date_end)}')
#st.bar_chart(df_)

