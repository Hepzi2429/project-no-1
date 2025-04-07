import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px 
import time
from streamlit_option_menu import option_menu 

# ANDHRA
lists_A=[]
df_A=pd.read_csv("df_AN.csv")
for i,r in df_A.iterrows():  
    lists_A.append(r["Route_name"])  

#KERALA
lists_K=[]
df_K=pd.read_csv("df_ker.csv")
for i,r in df_K.iterrows():
    lists_K.append(r['Route_name'])

#Telungana bus
lists_TL=[]
df_TL=pd.read_csv("df_tel.csv")
for i,r in df_TL.iterrows():  
    lists_TL.append(r["routes"])  

#goa bus
lists_G=[]
df_G=pd.read_csv("df_g.csv")
for i,r in df_G.iterrows():
    lists_G.append(r['Route_name'])

#assam bus
lists_AS=[]
df_ASS=pd.read_csv("df_ass.csv")
for i,r in df_ASS.iterrows():
    lists_AS.append(r['routes'])

#uttar pradesh bus
lists_UP=[]
df_UP=pd.read_csv("df_utp.csv")
for i,r in df_UP.iterrows():
    lists_UP.append(r['routes'])    

#north bengal bus
lists_NB=[]
df_NB=pd.read_csv("df_NB.csv")
for i,r in df_NB.iterrows():
    lists_NB.append(r['routes'])

#jammu kashmir
lists_JMK=[]
df_JMK=pd.read_csv("df_JMK.csv")
for i,r in df_JMK.iterrows():
    lists_JMK.append(r["routes"])

#west bengal 
lists_HR=[]
df_HR=pd.read_csv("df_HR.csv")
for i,r in df_HR.iterrows():
    lists_HR.append(r['Route_name'])

#bihar
lists_B=[]
df_BHR=pd.read_csv("df_BHR.csv")
for i,r in df_BHR.iterrows():
    lists_B.append(r["routes"])



#Settings Streamlit Page


# Set layout
st.set_page_config(layout="wide")

# Navbar setup using option_menu
selected_option = option_menu(
    menu_title=None,  # No big menu title, clean topbar
    options=["Home", "📍States And Routes"],
    icons=["house", "map"],
    orientation="horizontal",
    menu_icon="bus",
    default_index=0,
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "crimson", "font-size": "20px"},
        "nav-link": {
            "font-size": "18px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "#e50914", "color": "white"},
    }
)

# === Home Page ===
if selected_option == "Home":
    st.image("E:/redbusproject/redbus logo/redBus-Logo.jpg", width=200)

    st.markdown("<h1 style='color: crimson;'>Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit</h1>", unsafe_allow_html=True)

    st.markdown("## 🚌 Welcome to **Digital Bus Routes & Bookings**")

    st.markdown("---")
    st.markdown("### 🔸 **:red[Domain:]** Transportation")

    st.markdown("### 🔸 **:red[Objective:]**")
    st.markdown("""
    The **Redbus Data Scraping and Filtering with Streamlit Application** aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data.

    Using **Selenium** for web scraping, this project automates the extraction of detailed information from Redbus – including routes, schedules, price, and seat availability.

    By streamlining data collection and offering tools for data-driven decisions, it helps improve operational efficiency and strategic planning in transportation.
    """)

    st.markdown("### 🔸 **:blue[Overview:]**")
    
    with st.expander("🔍 Selenium"):
        st.markdown("""
        Selenium is a popular open-source tool for automating web browsers. It allows control over browser actions, making it ideal for:
        - Automated Testing
        - Web Scraping
        - Browser Automation
        """)

    with st.expander("📊 Pandas"):
        st.markdown("""
        Pandas is a powerful data analysis and manipulation library. It provides data structures and functions to handle and analyze structured data like tables and time series.
        """)

    with st.expander("🗄️ MySQL"):
        st.markdown("""
        MySQL is an open-source relational database system. It uses SQL for managing and querying data effectively.
        """)

    with st.expander("🌐 Streamlit"):
        st.markdown("""
        Streamlit is a Python framework for creating interactive web apps. It's widely used by data scientists to build dashboards and visualize data effortlessly.
        """)

    st.markdown("### 🛠️ **:violet[Skill-Take:]**")
    st.markdown("`Python`, `Selenium`, `Pandas`, `MySQL`, `Streamlit`")

    st.markdown("---")
    st.markdown("### 👩‍💻 **:blue[Developed by:] :red[Hepzibah P]**")

# === States and Routes Page ===
elif selected_option == "📍States And Routes":
    st.title("📍 Explore States and Bus Routes")
    


if selected_option == '📍States And Routes':
    st.markdown("---")

    # State selection
    S = st.selectbox("🧭 Select a State", [
        "Andhra Pradesh", "Kerala", "Telangana", "Goa", "Assam",
        "Uttar Pradesh", "North Bengal", "Jammu Kashmir", "Haryana", "Bihar"
    ])

    col1, col2 = st.columns(2)

    with col1:
        select_type = st.radio("🛏️ Choose Bus Type", ["All Types", "AC Sleeper", "Non AC Sleeper", "AC Semi Sleeper",
            "Non AC Semi Sleeper", "Sleeper", "Semi Sleeper", "Seater", "Volvo", "Others"])
    with col2:
        select_fare = st.radio("💸 Choose Fare Range", ["50-1000", "1000-2000", "2000 and above"])

    TIME = st.time_input("🕐 Select Preferred Departure Time")

    # === Andhra Pradesh Route and Filters Section ===
    # Main function for querying bus data
    def type_and_fare(bustype, fare_range, route_name):
        conn = mysql.connector.connect(
            host="127.0.0.1", port=3306,
            user="root", password="Hepzi@2429", database="redbus_project"
        )
        my_cursor = conn.cursor()

        if fare_range == "50-1000":
            fare_min, fare_max = 50, 1000
        elif fare_range == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000

        if bustype == "sleeper":
            bustype_condition = "LOWER(bustype) LIKE '%sleeper%'"
        elif bustype == "semi-sleeper":
            bustype_condition = "LOWER(bustype) LIKE '%semi sleeper%'"
        elif bustype == "ac":
            bustype_condition = "LOWER(bustype) LIKE '%ac%'"
        elif bustype == "non-ac":
            bustype_condition = "LOWER(bustype) LIKE '%non ac%'"
        elif bustype == "ac sleeper":
            bustype_condition = "LOWER(bustype) LIKE '%ac sleeper%'"
        elif bustype == "non-ac sleeper":
            bustype_condition = "LOWER(bustype) LIKE '%non ac sleeper%'"
        else:
            bustype_condition = "1=1"  # no filter

        sqlquery = f'''
            SELECT * FROM busdetail 
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = "{route_name}"
            AND {bustype_condition}
            AND departure_time >= '{TIME}'
            ORDER BY price DESC, departure_time DESC
        '''
        my_cursor.execute(sqlquery)
        out = my_cursor.fetchall()
        conn.close()

        df = pd.DataFrame(out, columns=[
            "id", "busname", "route_name", "bustype", "departure_time",
            "total_duration", "reaching_time", "star_rating", "price",
            "seats_available", "route_link"
        ])
        return df

    # State-specific route selection and data display
    if S == "Andhra Pradesh":
        st.success("🏖️ Viewing Routes for Andhra Pradesh")
        AP = st.selectbox("🛤️ Available Routes", lists_A)
        df_result = type_and_fare(select_type, select_fare, AP)

    elif S == "Kerala":
        st.success("🏖️ Viewing Routes for Kerala")
        K = st.selectbox("🛤️ Available Routes", lists_K)
        df_result = type_and_fare(select_type, select_fare, K)

    elif S == "Telangana":
        st.success("🏖️ Viewing Routes for Telangana")
        TL = st.selectbox("🛤️ Available Routes", lists_TL)
        df_result = type_and_fare(select_type, select_fare, TL)

    elif S == "Goa":
        st.success("🏖️ Viewing Routes for Goa")
        G = st.selectbox("🛤️ Available Routes", lists_G)
        df_result = type_and_fare(select_type, select_fare, G)

    elif S == "Assam":
        st.success("🏖️ Viewing Routes for Assam")
        AS = st.selectbox("🛤️ Available Routes", lists_AS)
        df_result = type_and_fare(select_type, select_fare, AS)

    elif S == "Uttar Pradesh":
        st.success("🏖️ Viewing Routes for Uttar Pradesh")
        UP = st.selectbox("🛤️ Available Routes", lists_UP)
        df_result = type_and_fare(select_type, select_fare, UP)

    elif S == "North Bengal":
        st.success("🏖️ Viewing Routes for North Bengal")
        NB = st.selectbox("🛤️ Available Routes", lists_NB)
        df_result = type_and_fare(select_type, select_fare, NB)

    elif S == "Jammu Kashmir":
        st.success("🏔️ Viewing Routes for Jammu & Kashmir")
        JMK = st.selectbox("🛤️ Available Routes", lists_JMK)
        df_result = type_and_fare(select_type, select_fare, JMK)

    elif S == "Haryana":
        st.success("🏖️ Viewing Routes for Haryana")
        HR = st.selectbox("🛤️ Available Routes", lists_HR)
        df_result = type_and_fare(select_type, select_fare, HR)

    elif S == "Bihar":
        st.success("🏖️ Viewing Routes for Bihar")
        B = st.selectbox("🛤️ Available Routes", lists_B)
        df_result = type_and_fare(select_type, select_fare, B)

    if not df_result.empty:
        st.markdown("### 🚌 Available Buses")
        st.dataframe(df_result, use_container_width=True)
    else:
        st.warning("No buses found for the selected filters.")