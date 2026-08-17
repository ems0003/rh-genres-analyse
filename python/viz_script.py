import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Configuration
sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "sans-serif"

# Création d'une palette personnalisée (Rose pâle, Mauve, Turquoise, etc.)
# Tu peux ajuster les codes couleurs selon tes envies exactes !
custom_palette = ["#FFB6C1", "#DDA0DD", "#40E0D0", "#FFC0CB", "#BA55D3", "#AFEEEE"]

# Chargement du fichier unique
df = pd.read_csv("./data/cleaned_chomage.csv")

# -------------------------------------------------------------------------
# GRAPH 1 : Quels sont les 10 pays ayant le taux de chômage le plus élevé 
# pour les femmes de 30 ans et plus sur la période 2015 - 2024 ?
# -------------------------------------------------------------------------
df_q1 = df[
    (df["SEX"].isin(['F', 'Femme', 'Female'])) & 
    (df["AGE"].isin(['30-54', '30-64', '30-74'])) & 
    (df["ANNEE"].between(2015, 2024))
]
df_q1_plot = df_q1.groupby("ISO")["TAUX_CHOMAGE"].mean().reset_index()
df_q1_plot = df_q1_plot.sort_values("TAUX_CHOMAGE", ascending=False).head(10)

plt.figure(figsize=(10, 5))
# Utilisation d'une palette turquoise/mauve dégradée
sns.barplot(data=df_q1_plot, x="TAUX_CHOMAGE", y="ISO", palette="crest", hue="ISO")
plt.title("Top 10 des pays - Taux de chômage moyen (Femmes 30+)", fontsize=12)
plt.show()

# -------------------------------------------------------------------------
# GRAPH 2 : L'augmentation du chômage est-elle due aux hommes de moins de 
# 30 ans sur toute la période (2015 - 2024) ?
# -------------------------------------------------------------------------
df_q2 = df[
    (df["AGE"].isin(['15-19', '20-24', '25-29'])) & 
    (df["ANNEE"].isin([2015, 2024]))
]
df_q2_pivot = df_q2.groupby(['SEX', 'AGE', 'ANNEE'])['TAUX_CHOMAGE'].mean().unstack()
df_q2_pivot = df_q2_pivot.rename(columns={2015: 'TAUX_2015', 2024: 'TAUX_2024'}).reset_index()

df_q2_melted = pd.melt(df_q2_pivot, id_vars=['SEX', 'AGE'], value_vars=['taux_2015' if 'taux_2015' in df_q2_pivot.columns else 'TAUX_2015', 'TAUX_2024'])

plt.figure(figsize=(10, 5))
# Palette personnalisée rose/turquoise pour les groupes (ex: Hommes/Femmes)
sns.barplot(data=df_q2_melted, x='AGE', y='value', hue='SEX', palette=["#40E0D0", "#FFB6C1"])
plt.title("Chômage des jeunes : 2015 vs 2024")
plt.show()

# -------------------------------------------------------------------------
# GRAPH 3 : Quels sont les pays avec le plus faible taux de
# chômage global (comparaison 2015 vs 2024) ?
# -------------------------------------------------------------------------
min_2015 = df[df['ANNEE'] == 2015].groupby('ISO')['TAUX_CHOMAGE'].mean().nsmallest(1).reset_index()
min_2015['ANNEE_REF'] = 2015
min_2024 = df[df['ANNEE'] == 2024].groupby('ISO')['TAUX_CHOMAGE'].mean().nsmallest(1).reset_index()
min_2024['ANNEE_REF'] = 2024

df_q3 = pd.concat([min_2015, min_2024])

plt.figure(figsize=(6, 4))
sns.barplot(data=df_q3, x='ANNEE_REF', y='TAUX_CHOMAGE', hue='ISO', palette=["#DDA0DD", "#40E0D0"])
plt.title("Pays avec le taux le plus bas (2015 vs 2024)")
plt.show()

# -------------------------------------------------------------------------
# GRAPH 4 : Quel est le taux médian de chômage en 2024 
# (Hommes vs Femmes, tout âge confondu) ?
# -------------------------------------------------------------------------
df_q6 = df[df['ANNEE'] == 2024].groupby('SEX')['TAUX_CHOMAGE'].median().reset_index()

plt.figure(figsize=(7, 4))
# Rose pâle et Mauve pour la parité hommes/femmes
sns.barplot(data=df_q6, x='SEX', y='TAUX_CHOMAGE', hue='SEX', palette=["#FFB6C1", "#DDA0DD"])
plt.title("Taux médian de chômage en 2024 par sexe")
plt.show()