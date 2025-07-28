# Erin Courtemanche
# CS 230-4
# Data: Nuclear Explosions
# URL: https://nuclear-data-murvjqljvhfxu4srwebz5g.streamlit.app/
# Description: This code aims to provide a user-friendly website where its visitors can learn about various aspects of historical nuclear explosions.


# Imports
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk
from fontTools.cu2qu import curve_to_quadratic
from matplotlib.pyplot import legend
from matplotlib import patheffects
from streamlit_folium import st_folium
import folium
import os
import seaborn as sns

st.set_page_config(
    page_title="Nuclear Explosions",
    page_icon=":radioactive:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Read in dataset
df_nuclear = pd.read_csv("https://drive.google.com/uc?export=download&id=1xPnkdcZ-9tyhyNDxORT1s5Di3uc78JJm")
#python -m streamlit run "C:\Users\eacou\OneDrive - Bentley University\[1] Portfolio\Nuclear_Website\nuclearWebsite.py"

# ----------------------------------Clean dataset-------------------------------------------
# Rename column headers [DA1]
df_nuclear.rename(columns={"WEAPON SOURCE COUNTRY": "Source Country"}, inplace=True)
df_nuclear.rename(columns={"WEAPON DEPLOYMENT LOCATION": "Deployment Location"}, inplace=True)
df_nuclear.rename(columns={"Data.Source": "Data Source"}, inplace=True)
df_nuclear.rename(columns={"Location.Cordinates.Latitude": "Latitude"}, inplace=True)
df_nuclear.rename(columns={"Location.Cordinates.Longitude": "Longitude"}, inplace=True)
df_nuclear.rename(columns={"Data.Magnitude.Body": "Body Magnitude"}, inplace=True)
df_nuclear.rename(columns={"Data.Magnitude.Surface": "Surface Magnitude"}, inplace=True)
df_nuclear.rename(columns={"Location.Cordinates.Depth": "Depth"}, inplace=True)
df_nuclear.rename(columns={"Data.Yeild.Lower": "Lower Yield"}, inplace=True)
df_nuclear.rename(columns={"Data.Yeild.Upper": "Upper Yield"}, inplace=True)
df_nuclear.rename(columns={"Data.Purpose": "Purpose"}, inplace=True)
df_nuclear.rename(columns={"Data.Name": "Name"}, inplace=True)
df_nuclear.rename(columns={"Data.Type": "Deployment Method"}, inplace=True)
df_nuclear.rename(columns={"Date.Day": "Day"}, inplace=True)
df_nuclear.rename(columns={"Date.Month": "Month"}, inplace=True)
df_nuclear.rename(columns={"Date.Year": "Year"}, inplace=True)


def custom_theme():
    st.markdown("""
    <style>
        .stApp {
            background-color: #802626;
            color: #E0E0E0;
        }

        section[data-testid="stSidebar"] {
            background-color: #AA3232;
        }

        div[data-testid="stVerticalBlock"] {
            background-color: #2A0C0C;
            padding: 1rem;
            border-radius: 6px;
        }

        .stButton>button {
            background-color: #FF4B4B;
            color: white;
        }

        .stButton>button:hover {
            background-color: #551919;
        }

           h1, h2, h3, h4, h5, h6, p, span, div {
               color: #E0E0E0 !important;
               font-family: 'Courier New', Courier, 'IBM Plex Mono', monospace !important;
        }

        div[data-baseweb="select"] > div {
            background-color: #802626 !important;
            color: black !important;
        }

        /* Dropdown menu */
        div[data-baseweb="select"] [role="listbox"] {
            background-color: #802626 !important;
            color: black !important;
        }

        /* Option text */
        div[data-baseweb="select"] [role="option"] {
            color: black !important;
        }

        /* Option hover effect */
        div[data-baseweb="select"] [role="option"]:hover {
            background-color: #A03333 !important;
            color: white !important;
        }

        /* Selected value */
        div[data-baseweb="select"] div[role="combobox"] span {
            color: black !important;
        }

    </style>
    """, unsafe_allow_html=True)


def centered_chart(fig):
    left_col, center_col, right_col = st.columns([1, 14, 1])  # Adjust widths to center
    with center_col:
        with st.container():
            st.markdown("""
                    <div style='
                        background-color: #2A0C0C;
                        padding: 1rem;
                        border-radius: 6px;
                        text-align: center;
                    '>
                """, unsafe_allow_html=True)
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)


# Function to find yield (kt) according to deployment method within a year range
def yearly_yield(year_range=None, deploy_method=None, graph_type=None):
    # [ST1]
    # Creates a double-sided slider to select year range
    if year_range is None:
        year_range = st.slider("Select the range of years you want to explore",
                               min_value=int(df_nuclear["Year"].min()),
                               max_value=int(df_nuclear["Year"].max()),
                               value=(1945, 1998))

    top_ten_methods = df_nuclear["Deployment Method"].value_counts().nlargest(10).index.tolist()

    # [ST2]
    # Creates a bubble selection for deployment method
    if deploy_method is None:
        deploy_method = st.radio("Select the deployment method you are interested in",
                                 sorted(top_ten_methods))
    # [ST3]
    # Allows the user to select the type of graph they want displayed
    if graph_type is None:
        graph_type = st.selectbox("Select the chart type you want", ["Line", "Bar", "Scatter"])

    # [DA5]
    # Filters data points to only be within the year range given and of the selected deployment method
    Q1_filter = df_nuclear[
        (df_nuclear["Year"] >= year_range[0]) &
        (df_nuclear["Year"] <= year_range[1]) &
        (df_nuclear["Deployment Method"] == deploy_method)
        ]

    # if statements to display the selected chart type
    if not Q1_filter.empty:
        # [DA7]
        # groups all valid data points by the same year together and displays their upper yield value
        yield_by_year = Q1_filter.groupby("Year")["Upper Yield"].mean().reset_index()
        # [Chart 1]

        fig, Q1_Graph = plt.subplots(figsize=(16, 6))
        if graph_type == "Line":
            Q1_Graph.plot(yield_by_year["Year"], yield_by_year["Upper Yield"], marker='o')
        elif graph_type == "Bar":
            Q1_Graph.bar(yield_by_year["Year"], yield_by_year["Upper Yield"])
        elif graph_type == "Scatter":
            Q1_Graph.scatter(yield_by_year["Year"], yield_by_year["Upper Yield"])

        # Formating for graphs
        Q1_Graph.set_title("Average Upper Yield by Year for Selected Deployment Method")
        Q1_Graph.set_xlabel("Year")
        Q1_Graph.set_ylabel("Average Upper Yield (kt)")
        Q1_Graph.grid(True)

        plt.tight_layout()
        centered_chart(fig)

        # [PY2]
        return year_range, deploy_method, graph_type


# Function to determine the locations of nuclear explosions
def location_data(df, rounding_precision=3):
    try:  # [PY3]
        # [PY4]
        # Replaces longitudes and latitudes with their rounded counterparts
        df = df.copy()
        df['lat_rounded'] = df['Latitude'].round(rounding_precision)
        df['lon_rounded'] = df['Longitude'].round(rounding_precision)

        # Group Longitudes and Latitudes
        location_counts = df.groupby(['lat_rounded', 'lon_rounded']).agg(
            Names=('Name', lambda x: ', '.join(x)),
            Latitude=('Latitude', 'first'),
            Longitude=('Longitude', 'first')
        ).reset_index()

        location_counts.rename(columns={
            'lat_rounded': 'lat',
            'lon_rounded': 'lon',
        }, inplace=True)

        # [DA9]
        # Creates new column "Names"
        location_counts['Count'] = location_counts['Names'].apply(lambda x: len(x.split(',')))

        return location_counts

    except Exception as e:
        st.error(f"Error processing data: {e}")
        return pd.DataFrame(), {}


# Function that creates an interactive map showing the most common deployment locations
def deployment_location(df, rounding_precision=3, country_focus=None):
    # [PY5]
    # Dictionary of all deployment locations sorted by their country
    locations_by_country = {
        "United States": [
            "Alamogordo", "Amchitka Ak", "Carlsbad Nm", "C. Nevada", "Fallon Nv",
            "Mellis Nv", "Nellis Nv", "Nts", "Rifle Co", "Semipalatinsk",
            "Malden Is", "Nellis Nv", "Monteb Austr", "Farmingt Nm", "Offuswcoast"
        ],
        "Russia": [
            "Arkhan Russ", "Astrak Russ", "Azgir", "Azgir Kazakh", "Bashki Russ",
            "Bashkir Russ", "Kalmyk Russ", "Kemero Russ", "Kharan", "Komi Russ",
            "Krasno Russ", "Mtr Russ", "Murm Russ", "N2 Russ", "Perm Russ",
            "Pokhran", "Reggane Alg", "Orenbg Russ", "Stavro Russ", "Tuymen Russ",
            "Tyumen Russ", "Ural Russ", "Irkuts Russ", "Jakuts Ruse", "Jakuts Russ",
            "Htr Russ", "Nz Russ", "S. Atlantic", "S.Atlantic", "Tyumen Russ",
            "W Kazakh", "W Mururoa", "Wsw Mururoa"
        ],
        "Kazakhstan": [
            "Azgie Kazakh", "Azgir Kazakh", "Mangy Kazakh", "Semi Kazakh", "Kazakhstan"
        ],
        "France (French Polynesia)": [
            "Fangataufa", "Fangataufaa", "Mururoa", "Mururoa", "W Mururoa", "Wsw Mururoa"
        ],
        "Pakistan": [
            "Chagai", "Kharan"
        ],
        "Japan": [
            "Hiroshima", "Nagasaki"
        ],
        "Marshall Islands": [
            "Bikini", "Enewetak"
        ],
        "Algeria": [
            "Reggane Alg", "In Ecker Alg"
        ],
        "Australia": [
            "Emu Austr", "Marali Austr", "Monteb Austr"
        ],
        "Turkmenistan": [
            "Mary Turkmen"
        ],
        "Uzbekistan": [
            "Pamuk Uzbek"
        ],
        "China": [
            "Lop Nor"
        ],
        "India": [
            "Pokhran"
        ],
        "Ukraine": [
            "Ukraine", "Ukeaine"
        ],
        "United Kingdom": [
            "Pacific"
        ],
        "Kiribati": [
            "Christmas Is"
        ]
    }

    # Centers map on selected country
    if country_focus:
        filtered_locations = locations_by_country.get(country_focus, [])
        # [DA4]
        df_filtered = df[df['Deployment Location'].isin(filtered_locations)]
        if df_filtered.empty:
            st.warning(f"No data found for '{country_focus}'. Showing all data.")
            df_filtered = df
    else:
        df_filtered = df

    location_counts = location_data(df_filtered)

    # Specifies starting parameters for the map
    map_center = [df_filtered['Latitude'].mean(), df_filtered['Longitude'].mean()]
    map_folium = folium.Map(location=map_center, zoom_start=4)

    # [DA8]
    # Creates the data points to go on the map
    for _, row in location_counts.iterrows():
        names_list = row['Names'].split(',')
        names_display = ','.join(names_list[:3])
        if len(names_list) > 3:
            names_display += ', ...'

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=min(max(row['Count'] * 0.3, 3), 30),
            color='orange',
            fill=True,
            fill_opacity=0.6,
            tooltip=f"{row['Count']} explosion(s): {names_display}",
        ).add_to(map_folium)

    # [Folium1]
    return map_folium


# Function that creates a pie chart showing the most common reasons for nuclear explosions
def plot_purpose_distribution():
    purpose_counts = df_nuclear["Purpose"].value_counts()

    # only shows the top 4 reasons plus an others category
    top_purposes = purpose_counts.head(4)
    other_count = purpose_counts[4:].sum()
    if other_count > 0:
        top_purposes['Other'] = other_count

    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, texts, autotexts = ax.pie(
        top_purposes,
        labels=None,
        autopct=lambda p: f'{p:.1f}%' if p >= 2 else '',
        startangle=90,
        colors=["#FF4B4B", "#551919", "#802626", "#AA3232", "#D43F3F"],
        wedgeprops={'edgecolor': "#000000", 'linewidth': 1},
        textprops={'color': 'black', 'fontsize': 15}
    )

    ax.set_title("Top 5 Nuclear Explosion Purposes", fontweight='bold', fontsize=25, pad=15)

    ax.legend(
        wedges,
        [f"{label} ({count})" for label, count in zip(top_purposes.index, top_purposes)],
        title="Purposes",
        title_fontsize=16,
        loc="center left",
        bbox_to_anchor=(1.05, 0.5),
        prop={'size': 12, 'family': 'sans-serif'},
        frameon=True,
        framealpha=0.9,
    )

    plt.tight_layout()
    centered_chart(fig)

    selected_purpose = st.selectbox("Filter table by deployment purpose",
                                    options=["All"] + list(top_purposes.index))

    if selected_purpose == "Other":
        filtered_df = df_nuclear[df_nuclear["Purpose"].isin(purpose_counts.index[4:])]
    elif selected_purpose != "All":
        filtered_df = df_nuclear[df_nuclear["Purpose"] == selected_purpose]
    else:
        filtered_df = df_nuclear

    title_template("📋 Full Dataset of Nuclear Explosions 📋")

    left, center, right = st.columns([1, 6, 1])
    with center:
        st.dataframe(filtered_df, use_container_width=True)


# Function that looks at what deployment methods were used the most in each decade
def method_comparison_year():
    top_10_methods = df_nuclear["Deployment Method"].value_counts().nlargest(10).index

    filtered_df = df_nuclear[df_nuclear["Deployment Method"].isin(top_10_methods)]

    # Specifies that decades are every 10 years and creates a stacked bar graph pivot table to display this
    methods_by_decade = filtered_df.assign(
        Decade=(df_nuclear['Year'] // 10) * 10
    ).pivot_table(
        index='Decade',
        columns='Deployment Method',
        values='Name',
        aggfunc='count',
        fill_value=0
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    methods_by_decade.plot.bar(
        stacked=True,
        ax=ax,
        edgecolor='black',
        linewidth=0.5
    )

    ax.set_title("Nuclear Test Methods by Decade", fontsize=15)
    ax.set_xlabel("Decade", fontsize=12)
    ax.set_ylabel("Number of Tests", fontsize=12)
    ax.legend(title='Method', bbox_to_anchor=(1.05, 1))
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

    plt.tight_layout()
    centered_chart(fig)


# Reload locations_by_country outside the original function's scope
if 'Deployment Location' in df_nuclear.columns:
    locations_by_country = {
        "United States": [
            "Alamogordo", "Amchitka Ak", "Carlsbad Nm", "C. Nevada", "Fallon Nv",
            "Mellis Nv", "Nellis Nv", "Nts", "Rifle Co", "Semipalatinsk",
            "Malden Is", "Nellis Nv", "Monteb Austr", "Farmingt Nm"
        ],
        "Russia": [
            "Arkhan Russ", "Astrak Russ", "Azgir", "Azgir Kazakh", "Bashki Russ",
            "Bashkir Russ", "Kalmyk Russ", "Kemero Russ", "Kharan", "Komi Russ",
            "Krasno Russ", "Mtr Russ", "Murm Russ", "N2 Russ", "Perm Russ",
            "Pokhran", "Reggane Alg", "Orenbg Russ", "Stavro Russ", "Tuymen Russ",
            "Tyumen Russ", "Ural Russ", "Irkuts Russ", "Jakuts Ruse", "Jakuts Russ",
            "Htr Russ", "Nz Russ", "S. Atlantic", "S.Atlantic", "Tyumen Russ",
            "W Kazakh", "W Mururoa", "Wsw Mururoa"
        ],
        "Kazakhstan": [
            "Azgie Kazakh", "Azgir Kazakh", "Mangy Kazakh", "Semi Kazakh", "Kazakhstan"
        ],
        "France (French Polynesia)": [
            "Fangataufa", "Fangataufaa", "Mururoa", "Mururoa", "W Mururoa", "Wsw Mururoa"
        ],
        "Pakistan": [
            "Chagai", "Kharan"
        ],
        "Japan": [
            "Hiroshima", "Nagasaki"
        ],
        "Marshall Islands": [
            "Bikini", "Enewetak"
        ],
        "Algeria": [
            "Reggane Alg", "In Ecker Alg"
        ],
        "Australia": [
            "Emu Austr", "Marali Austr", "Monteb Austr"
        ],
        "Turkmenistan": [
            "Mary Turkmen"
        ],
        "Uzbekistan": [
            "Pamuk Uzbek"
        ],
        "China": [
            "Lop Nor"
        ],
        "India": [
            "Pokhran"
        ],
        "Ukraine": [
            "Ukraine", "Ukeaine"
        ],
        "United Kingdom": [
            "Pacific"
        ],
        "Kiribati": [
            "Christmas Is"
        ],
        "Germany": [
            "Offuswcoast"
        ]
    }
else:
    st.error("The dataset does not contain a 'Deployment Location' column.")


# Function that creates a reusuable template for any titles
def title_template(text, font_size=35, color="#F5A522", center=True):
    align = 'center' if center else 'left'
    st.markdown(f"""
    <h2 style = 'text-align: {align};
        color: {color};
        font-size: {font_size}px;
        margin-botton: 15px;'>
        {text}
        </h2>
        """, unsafe_allow_html=True)


custom_theme()

# [ST4]
# Page navigation and format
st.sidebar.title("Navigation")
page_select = st.sidebar.radio("Go to",
                               ["Yield and Method Across Decades", "Deployment Locations", "Deployment Purpose"])
st.sidebar.markdown("-----")
st.sidebar.markdown("Nuclear Explosions Dashboard")
st.sidebar.info("Explore data on nuclear explosions like never before!"
                " Learn about the yields (kt) of different deployment types"
                " throughout the years, the most frequent nuclear explosions sites,"
                " and the most common purposes for nuclear explosions.")
st.sidebar.markdown("-----")

# Loads the appropriate function depending on the selected page
if page_select == "Yield and Method Across Decades":
    title_template("☢️ Yield (kt) by Year and Deployment Method ☢️")
    yearly_yield()
    st.markdown("-----")
    title_template("💣 Deployment Method by Decade 💣")
    method_comparison_year()
elif page_select == "Deployment Locations":
    title_template("🌍 Most Used Deployment Locations 🌍")

    selected_country = st.selectbox("Filter by Country", options=list(locations_by_country.keys()),
                                    key="country_focus_select")

    map_folium = deployment_location(df_nuclear, country_focus=selected_country)

    st.markdown("""
        <style>
            div[data-testid="stVerticalBlock"] > div:has(.folium-map) + div {
                display: none !important;
            }

            iframe {
                display: block;
                width: 100%;
                height: 400px;
            }

            st.Element {
                margin-bottom: 0rem !important;
                padding-bottom: 0rem !important;
            } 

            .parent-container {
                line-height: 0;
            }

            .parent-container {
                padding: 0;
                margin: 0;
            }

            .clearfix::after {
                content: "";
                display: table;
                clear: both;
            }
        <style>
    """, unsafe_allow_html=True)

    st_folium(map_folium, width=1200, height=450, returned_objects=[])

elif page_select == "Deployment Purpose":
    title_template("🧪 Most Common Deployment Purposes 🧪")
    plot_purpose_distribution()
    st.sidebar.markdown("### Purpose Code Definitions")
    purpose_legend = {
        "Wr": "Weapons Research",
        "We": "Weapons Evaluation",
        "Pne": "Peaceful Nuclear Explosion",
        "Se": "Safety Evaluation",
        "Other": "Transportation tests, military exercises, mining purposes, etc.",
    }
    for code, meaning in purpose_legend.items():
        st.sidebar.markdown(f"**{code}**: {meaning}")



