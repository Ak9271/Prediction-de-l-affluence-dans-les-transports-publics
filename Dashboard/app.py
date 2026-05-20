import streamlit as st
import pandas as pd
import os
import numpy as np
import math
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

st.set_page_config(
    page_title="Dashboard Affluence | Transports Publics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: #f4f5f7;
}

#MainMenu, footer { visibility: hidden; }

/* ── Main header ── */
.main-header {
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}
.app-title {
    font-size: 2.8rem; font-weight: 800; letter-spacing: -0.02em;
    color: #222222;
    margin: 0;
}
.app-title span {
    background: linear-gradient(135deg, #7d206f, #eb1925);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.app-subtitle { color: #666666; font-size: 1rem; margin-top: 0.4rem; font-weight: 500; }
.live-badge {
    display: inline-flex; align-items: center; gap: 0.45rem;
    background: rgba(125,32,111,0.08); border: 1px solid rgba(125,32,111,0.2);
    color: #7d206f; font-size: 0.75rem; font-weight: 700;
    padding: 5px 14px; border-radius: 20px; margin-top: 0.9rem;
}
.live-dot {
    width: 7px; height: 7px; background: #7d206f; border-radius: 50%;
    animation: blink 1.5s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.25} }

/* ── KPI Cards ── */
.kpi-card {
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 12px;
    padding: 1.5rem 1rem 1.2rem 1rem;
    text-align: center;
    position: relative;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    height: 100%;
    box-shadow: 0 4px 15px rgba(0,0,0,0.02);
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(0,0,0,0.08); }
.kpi-accent {
    height: 4px;
    background: linear-gradient(90deg, #7d206f, #eb1925);
    border-radius: 12px 12px 0 0;
    position: absolute; top: 0; left: 0; right: 0;
}
.kpi-icon { font-size: 1.8rem; display: block; margin-bottom: 0.4rem; }
.kpi-value {
    font-size: 1.9rem; font-weight: 800; line-height: 1.1; margin: 0.2rem 0;
    color: #222222;
}
.kpi-label {
    font-size: 0.7rem; color: #777777;
    text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700;
    margin-top: 0.3rem;
}

/* ── Section headers ── */
.section-title {
    font-size: 1.35rem; font-weight: 800; color: #111111;
    margin: 0.5rem 0 0.2rem 0;
}
.section-sub { color: #555555; font-size: 0.85rem; margin-bottom: 1rem; font-weight: 500; }

/* ── Filter bar ── */
.filter-bar {
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}

/* ── Alert critique ── */
.alert-crit {
    background: #fff0f0;
    border: 1px solid #ffcccc;
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    margin-bottom: 0.6rem;
    color: #c21758;
    font-weight: 600;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    padding: 4px 6px; border-radius: 12px;
    border: 1px solid rgba(0,0,0,0.08);
    gap: 4px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px; color: #666666;
    font-weight: 600; font-size: 0.9rem;
    padding: 9px 20px;
    transition: all 0.2s;
    border: 1px solid transparent;
}
.stTabs [aria-selected="true"] {
    background: #fdf5f7 !important;
    color: #b01678 !important;
    border-color: #f7e0eb !important;
}

/* ── Streamlit metric override ── */
[data-testid="stMetricValue"] { color: #222222 !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { color: #777777 !important; font-weight: 700 !important; }

/* ── Custom scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(0,0,0,0.02); }
::-webkit-scrollbar-thumb { background: rgba(125,32,111,0.4); border-radius: 4px; }

/* ── Divider ── */
hr { border-color: rgba(0,0,0,0.08) !important; margin: 1.2rem 0 !important; }

/* ── OVERRIDES COMPOSANTS NATIFS (Fonds dégradés SNCF) ── */
:root {
    --sncf-gradient: linear-gradient(135deg, rgba(125,32,111,0.85), rgba(176,22,120,0.85), rgba(194,23,88,0.85), rgba(218,29,51,0.85), rgba(235,25,37,0.85));
}

/* Expander (Filtres dynamiques) */
[data-testid="stExpander"] details {
    background: var(--sncf-gradient) !important;
    border-radius: 10px;
    border: none;
}
[data-testid="stExpander"] summary, [data-testid="stExpander"] p, [data-testid="stExpander"] label {
    color: #ffffff !important;
}

/* Multiselect - fond de la boîte */
[data-baseweb="select"] > div {
    background: var(--sncf-gradient) !important;
    border: none !important;
}
/* Labels au-dessus des filtres */
.stMultiSelect label p {
    color: #222222 !important;
    font-weight: 700;
}

/* Multiselect - Tags (Ligne A, Lundi, etc.) */
span[data-baseweb="tag"] {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: none !important;
}
span[data-baseweb="tag"] span {
    color: #000000 !important;
}
span[data-baseweb="tag"] svg {
    fill: #000000 !important;
}

/* DataFrame (Tableau détaillé) */
[data-testid="stDataFrame"] > div > div > div {
    background: var(--sncf-gradient) !important;
}
[data-testid="stDataFrame"] table {
    background: transparent !important;
    color: #ffffff !important;
}
[data-testid="stDataFrame"] th, [data-testid="stDataFrame"] td {
    background: transparent !important;
    color: #ffffff !important;
    border-color: rgba(255,255,255,0.2) !important;
}

/* Boutons (ex: Exporter en CSV) */
.stButton button, .stDownloadButton button {
    background: var(--sncf-gradient) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
.stButton button:hover, .stDownloadButton button:hover {
    opacity: 0.9;
    color: #ffffff !important;
}

/* Menu déroulant (Popover) fond et listes */
[data-baseweb="popover"] > div,
ul[role="listbox"],
li[role="option"] {
    background-color: #ffffff !important;
    color: #222222 !important;
}
li[role="option"]:hover, li[role="option"][aria-selected="true"] {
    background-color: #f9eef2 !important;
    color: #eb1925 !important;
}
</style>
""", unsafe_allow_html=True)

JOURS_NOMS   = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
MOIS_NOMS    = ["Jan","Fév","Mar","Avr","Mai","Juin","Juil","Août","Sep","Oct","Nov","Déc"]
LIGNE_COLORS = {
    "RER A": "#E3051C",
    "RER B": "#5291CE",
    "RER C": "#FFCE00",
    "RER D": "#00814F",
    "RER E": "#C04191",
}
LIGNE_FILL_COLORS = {
    "RER A": "rgba(227, 5, 28, 1)",
    "RER B": "rgba(82, 145, 206, 1)",
    "RER C": "rgba(255, 206, 0, 1)",
    "RER D": "rgba(0, 129, 79, 1)",
    "RER E": "rgba(192, 65, 145, 1)",
}

BASE  = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.join(BASE, "..")
ml_dir = os.path.join(ROOT, "Resultats-Machine Learning")
CSV_PATH = os.path.join(ml_dir, "Donnees normalisation", "donnees_IA_finales.csv.gz")

@st.cache_data(show_spinner="Chargement des données historiques…")
def load_actual_data():
    df_raw = pd.read_csv(CSV_PATH, sep=';', usecols=[
        'LIBELLE_ARRET', 'CODE_STIF_RES', 'Heure', 'Jour_Semaine', 'CAT_JOUR', 'TRNC_HORR_60', 'Pourcentage_validations'
    ])
    #Données pour savoir quelle ligne correspond à quel code réseau
    RESEAU_MAP = {
        '801': 'RER A', '802': 'RER B', '803': 'RER C', '804': 'RER D', '805': 'RER E',
        '850': 'Transilien P', '851': 'Transilien R', '852': 'Transilien N',
        '853': 'Transilien H/K', '854': 'Transilien J/L',
        '800': 'Tram 11-13', '110': 'Métro', '822': 'Tram 14', 
        '760': 'Métro 14 EXT GPE', '761': 'Métro 14 EXT GPE', '762': 'Métro 14 EXT GPE',
    }
    df_raw['CODE_STIF_RES'] = df_raw['CODE_STIF_RES'].astype(str).str.replace('.0', '', regex=False)
    df_raw['ligne'] = df_raw['CODE_STIF_RES'].map(RESEAU_MAP).fillna("Réseau inconnu")
    
    #Moyenne des affluences/arrêts 
    df_agg = df_raw.groupby(['LIBELLE_ARRET', 'ligne', 'Heure', 'Jour_Semaine', 'CAT_JOUR', 'TRNC_HORR_60'], as_index=False)['Pourcentage_validations'].mean()
    
    records = []
    for _, row in df_agg.iterrows():
        j = int(row['Jour_Semaine'])
        records.append({
            "arret":       row['LIBELLE_ARRET'],
            "ligne":       row['ligne'],
            "heure":       int(row['Heure']),
            "tranche":     row['TRNC_HORR_60'],
            "jour_idx":    j,
            "jour":        JOURS_NOMS[j] if j < len(JOURS_NOMS) else str(j),
            "est_weekend": int(j in [5, 6]),
            "type_jour":   row['CAT_JOUR'],
            "prediction":  float(row['Pourcentage_validations']) * 10,
        })
        
    return pd.DataFrame(records)

df = load_actual_data()

def interpreter_affluence(v):
    if v < 25:    return "🟢 Très faible", "Peu de passagers attendus",    "af-green"
    elif v < 55:  return "🟡 Faible",      "Affluence réduite",            "af-yellow"
    elif v < 95: return "🟠 Moyen",       "Affluence normale",            "af-orange"
    elif v < 140: return "🔴 Élevé",       "Beaucoup de passagers",        "af-red"
    else:         return "🔴 Très élevé",  "Affluence exceptionnelle",     "af-dark"

def obtenir_libelle_jour(code):
    mapping = {
        "JOHV":   "Jour ouvré (Lundi-Vendredi)",
        "SAHV":   "Samedi",
        "DIJFP":  "Dimanche / Férié",
    }
    return mapping.get(code, f"{code}")

def plotly_light_layout(fig, height=380, title=""):
    fig.update_layout(
        height=height,
        plot_bgcolor="#ffffff",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#444444", family="Inter"),
        title=dict(text=title, font=dict(size=14, color="#111111", family="Inter", weight="bold")),
        legend=dict(bgcolor="rgba(255,255,255,0.8)", bordercolor="rgba(0,0,0,0.1)", borderwidth=1,
                    font=dict(color="#444444")),
        margin=dict(l=20, r=20, t=42 if title else 18, b=20),
        xaxis=dict(gridcolor="rgba(0,0,0,0.05)", linecolor="rgba(0,0,0,0.1)",
                   tickfont=dict(color="#666666")),
        yaxis=dict(gridcolor="rgba(0,0,0,0.05)", linecolor="rgba(0,0,0,0.1)",
                   tickfont=dict(color="#666666")),
    )
    return fig

st.markdown(f"""
<div class="main-header">
    <div class="app-title">Dashboard <span>Affluence</span></div>
    <div class="app-subtitle">Transports Publics — Prédictions par réseau de neurones MLP</div>
    <div class="live-badge">
        <span class="live-dot"></span>
        Système actif · {datetime.now().strftime("%d/%m/%Y %H:%M")}
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs([
    "Vue d'ensemble",
    "Analyse Historique",
])

with tab1:
    st.markdown('<div class="section-title">Vue d\'ensemble</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Tableau de bord global — toutes lignes et arrêts confondus</div>', unsafe_allow_html=True)

    #KPI Cards
    avg_all      = df["prediction"].mean()
    max_all      = df["prediction"].max()
    top_ligne    = df.groupby("ligne")["prediction"].mean().idxmax()
    top_arret    = df.groupby("arret")["prediction"].mean().idxmax()
    heure_pointe = int(df.groupby("heure")["prediction"].mean().idxmax())

    kpis = [
        (f"{len(df):,}",        "Predictions generees"),
        (f"{avg_all:.1f}",      "Affluence moyenne"),
        (f"{max_all:.0f}",      "Pic d'affluence"),
        (top_ligne,             "Ligne la + chargee"),
        (f"{heure_pointe}h",    "Heure de pointe"),
    ]
    cols = st.columns(5)
    for col, (val, lbl) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-accent"></div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    #Graphiques
    col1, col2 = st.columns(2)

    with col1:
        hour_data = df.groupby(["heure", "ligne"])["prediction"].mean().reset_index()
        fig = px.line(
            hour_data, x="heure", y="prediction", color="ligne",
            color_discrete_map=LIGNE_COLORS, markers=True,
            labels={"heure": "Heure", "prediction": "Affluence moy.", "ligne": "Ligne"}
        )
        fig.update_traces(line=dict(width=2.5), marker=dict(size=5))
        plotly_light_layout(fig, 360, "Affluence par heure — toutes lignes")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col2:
        ligne_data = (df.groupby("ligne")["prediction"].mean()
                      .reset_index().sort_values("prediction", ascending=False))
        fig = px.bar(
            ligne_data, x="ligne", y="prediction",
            color="ligne", color_discrete_map=LIGNE_COLORS,
            labels={"ligne": "Ligne", "prediction": "Affluence moyenne"},
            text="prediction"
        )
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside",
                          marker_line_width=0, textfont=dict(color="rgba(255,255,255,0.8)"))
        plotly_light_layout(fig, 360, "Affluence moyenne par ligne")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    #Alertes
    st.markdown("#### Alertes — Créneaux à forte affluence")
    high = df[df["prediction"] > 150]
    if not high.empty:
        top_alerts = (high.groupby(["ligne", "tranche", "jour"])["prediction"]
                      .mean().nlargest(5).reset_index())
        for _, row in top_alerts.iterrows():
            st.markdown(f"""
            <div class="alert-crit">
                <strong>{row['ligne']}</strong> — {row['tranche']} le <strong>{row['jour']}</strong> :
                affluence estimée à <strong>{row['prediction']:.0f} passagers</strong>
            </div>""", unsafe_allow_html=True)
    else:
        st.success("Aucune alerte critique détectée sur les créneaux analysés.")


with tab2:
    st.markdown('<div class="section-title">Analyse Historique</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Explorez les prédictions par ligne, horaire, jour et type d\'événement</div>', unsafe_allow_html=True)

    #Filtres
    with st.expander("Filtres dynamiques", expanded=True):
        fc1, fc2, fc3, fc4 = st.columns(4)
        with fc1:
            f_lignes = st.multiselect(
                "Ligne(s)",
                options=sorted(df["ligne"].unique()),
                default=sorted(df["ligne"].unique()),
                key="h_lignes"
            )
        with fc2:
            f_jours = st.multiselect(
                "Jour(s)",
                options=JOURS_NOMS,
                default=JOURS_NOMS,
                key="h_jours"
            )
        with fc3:
            h_min, h_max = st.select_slider(
                "Plage horaire",
                options=list(range(6, 23)),
                value=(6, 22),
                format_func=lambda x: f"{x:02d}h",
                key="h_horaire"
            )
        with fc4:
            f_types = st.multiselect(
                "Type de jour",
                options=list(df["type_jour"].unique()),
                default=list(df["type_jour"].unique()),
                format_func=obtenir_libelle_jour,
                key="h_types"
            )

    #Filtres 
    fdf = df[
        df["ligne"].isin(f_lignes) &
        df["jour"].isin(f_jours) &
        df["heure"].between(h_min, h_max) &
        df["type_jour"].isin(f_types)
    ]

    niveau_count = (fdf["prediction"]
                    .apply(lambda v: interpreter_affluence(v)[0])
                    .value_counts())

    c_res1, c_res2, c_res3, c_res4 = st.columns(4)
    c_res1.metric("Résultats filtrés", f"{len(fdf):,}")
    c_res2.metric("Affluence moy.",    f"{fdf['prediction'].mean():.1f}" if not fdf.empty else "—")
    c_res3.metric("Max",               f"{fdf['prediction'].max():.0f}"  if not fdf.empty else "—")
    c_res4.metric("Min",               f"{fdf['prediction'].min():.0f}"  if not fdf.empty else "—")

    if fdf.empty:
        st.info("ℹAucun résultat pour la combinaison de filtres choisie.")
    else:
        st.divider()

        #Graphiques
        col1, col2 = st.columns(2)

        with col1:
            hd = fdf.groupby(["heure", "ligne"])["prediction"].mean().reset_index()
            fig = px.line(
                hd, x="heure", y="prediction", color="ligne",
                color_discrete_map=LIGNE_COLORS, markers=True,
                labels={"heure": "Heure", "prediction": "Affluence moy.", "ligne": "Ligne"}
            )
            fig.update_traces(line=dict(width=2.2), marker=dict(size=5))
            plotly_light_layout(fig, 360, "Évolution par heure")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        with col2:
            td = fdf.groupby(["tranche", "ligne"])["prediction"].mean().reset_index()
            fig = px.bar(
                td, x="tranche", y="prediction", color="ligne",
                barmode="group", color_discrete_map=LIGNE_COLORS,
                labels={"tranche": "Tranche", "prediction": "Affluence moy.", "ligne": "Ligne"}
            )
            fig.update_traces(marker_line_width=0)
            plotly_light_layout(fig, 360, "Affluence par tranche horaire")
            fig.update_xaxes(tickangle=-30)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        #Tableau
        st.markdown("#### Tableau détaillé")

        tbl = (fdf.groupby(["ligne", "jour", "tranche"])["prediction"]
               .mean().reset_index()
               .sort_values("prediction", ascending=False)
               .rename(columns={
                   "ligne": "Ligne", "jour": "Jour",
                   "tranche": "Tranche", "prediction": "Affluence moy."
               }))
        tbl["Affluence moy."] = tbl["Affluence moy."].round(1)
        tbl["Niveau"]         = tbl["Affluence moy."].apply(lambda v: interpreter_affluence(v)[0])

        st.dataframe(
            tbl, use_container_width=True, hide_index=True,
            column_config={
                "Affluence moy.": st.column_config.NumberColumn(format="%.1f 👥"),
                "Niveau":         st.column_config.TextColumn(width="medium"),
            }
        )

        csv_data = tbl.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Exporter en CSV",
            csv_data, "affluence_filtree.csv", "text/csv",
            use_container_width=False
        )


st.markdown(f"""
<div style='text-align:center; color:rgba(255,255,255,0.18); font-size:0.78rem;
            padding: 2rem 0 1rem 0; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 2rem;'>
        Dashboard Affluence &nbsp;·&nbsp; Transports Publics &nbsp;·&nbsp;
    YBoost B2 — 2025/2026 &nbsp;·&nbsp; {datetime.now().strftime("%d/%m/%Y %H:%M")}
</div>
""", unsafe_allow_html=True)

