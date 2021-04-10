# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import streamlit as st

# %% [markdown]
# ## Import and clean data

# %%
# Import and clean variable metadata
metadata = pd.read_csv('qol-data/csvFiles/metadata.csv')
metadata = metadata.drop(0)
metadata = metadata.iloc[:, 0:5]
metadata = metadata.dropna()


# %%
characterRaw = pd.read_csv('qol-data/csvFiles/character.csv', header=1).dropna(thresh=10)
characterRaw = characterRaw[characterRaw.NPA.notnull()]
characterRaw.NPA = characterRaw.NPA.astype(int)
characterRaw


# %%
economyRaw = pd.read_csv('qol-data/csvFiles/economy.csv', header=1).dropna(thresh=10)
economyRaw = economyRaw[economyRaw.NPA.notnull()]
economyRaw.NPA = economyRaw.NPA.astype(int)
economyRaw.info()


# %%
educationRaw = pd.read_csv('qol-data/csvFiles/education.csv',header=1).dropna(thresh=10)
educationRaw = educationRaw[educationRaw.NPA.notnull()]
educationRaw.NPA = educationRaw.NPA.astype(int)


# %%
engagementRaw = pd.read_csv('qol-data/csvFiles/engagement.csv',header=1).dropna(thresh=10)
engagementRaw = engagementRaw[engagementRaw.NPA.notnull()]
engagementRaw.NPA = engagementRaw.NPA.astype(int)


# %%
environmentRaw = pd.read_csv('qol-data/csvFiles/environment.csv',header=1).dropna(thresh=10)
environmentRaw = environmentRaw[environmentRaw.NPA.notnull()]
environmentRaw.NPA = environmentRaw.NPA.astype(int)


# %%
healthRaw = pd.read_csv('qol-data/csvFiles/health.csv',header=1).dropna(thresh=10)
healthRaw = healthRaw[healthRaw.NPA.notnull()]
healthRaw.NPA = healthRaw.NPA.astype(int)


# %%
housingRaw = pd.read_csv('qol-data/csvFiles/housing.csv',header=1).dropna(thresh=10)
housingRaw = housingRaw[housingRaw.NPA.notnull()]
housingRaw.NPA = housingRaw.NPA.astype(int)


# %%
safetyRaw = pd.read_csv('qol-data/csvFiles/safety.csv',header=1).dropna(thresh=10)
safetyRaw = safetyRaw[safetyRaw.NPA.notnull()]
safetyRaw.NPA = safetyRaw.NPA.astype(int)


# %%
transportationRaw = pd.read_csv('qol-data/csvFiles/transportation.csv',header=1).dropna(thresh=10)
transportationRaw = transportationRaw[transportationRaw.NPA.notnull()]
transportationRaw.NPA = transportationRaw.NPA.astype(int)


# %%
economyRaw.Household_Income_2018 = economyRaw.Household_Income_2018.str.replace(',','').replace('+','')


# %%
for each in economyRaw.Household_Income_2018:
    if not each.isnumeric():
        print(each.isnumeric())
        print(each)


# %%
economyRaw


# %%
selected = pd.read_csv("./selectedNPA.csv")
selected['order'] = selected.index
selected


# %%
filtered = economyRaw[economyRaw.NPA.isin(selected["NPA"])]
merged = pd.merge(selected,filtered,left_on="NPA", right_on="NPA",how="inner")
merged
print(selected.NPA.to_list())

merged["Household_Income_2018"] = merged["Household_Income_2018"].astype(float)

# %%

fig = px.bar(merged,x="Public_Nutrition_Assistance_2018",y="order",orientation="h",labels=dict(Public_Nutrition_Assistance_2018="FNS Percentage (2018)",order="NPA"))
fig.update_yaxes(autorange="reversed",ticktext=selected.NPA.to_list(),tickvals=selected.order.to_list())

st.plotly_chart(fig)

fig2 = px.bar(merged,x="Household_Income_2018",y="order",orientation="h",
    labels=dict(Household_Income_2018="Household Income (2018)",order="NPA"))
fig2.update_yaxes(autorange="reversed",ticktext=selected.NPA.tolist(),tickvals=selected.order.to_list())
st.plotly_chart(fig2)