import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
import uuid

# Data Frame creation

mydb = psycopg2.connect(
    host="localhost",
    user="postgres",  # Correct parameter is 'user'
    port="5432",
    database="phonepe",
    password="1234"
)
cursor = mydb.cursor()

#agg_ins

cursor.execute("Select * From aggregated_insurance")
mydb.commit()
Table1=cursor.fetchall()
Agg_ins=pd.DataFrame(Table1, columns=("States","Years","Quarter", "Transaction_type",
                                        "Transaction_count", "Transaction_amount"))

#agg_tran
cursor.execute("Select * From aggregated_transaction")
mydb.commit()
Table2=cursor.fetchall()
Agg_tran=pd.DataFrame(Table2, columns=("States","Years","Quarter", "Transaction_type",
                                        "Transaction_count", "Transaction_amount"))

#agg_user
cursor.execute("Select * From aggregated_user")
mydb.commit()
Table3=cursor.fetchall()
Agg_user=pd.DataFrame(Table3, columns=("States","Years","Quarter", "Brands",
                                        "Transaction_count", "Percentage"))

#map_ins
cursor.execute("Select * From map_insurance")
mydb.commit()
Table4=cursor.fetchall()
map_ins=pd.DataFrame(Table4, columns=("States","Years","Quarter", "Districts",
                                        "Transaction_count", "Transaction_amount"))

#map_tran
cursor.execute("Select * From map_transaction")
mydb.commit()
Table5=cursor.fetchall()
map_tran=pd.DataFrame(Table5, columns=("States","Years","Quarter", "Districts",
                                        "Transaction_count", "Transaction_amount"))

#map_user
cursor.execute("Select * From map_user")
mydb.commit()
Table6=cursor.fetchall()
map_user=pd.DataFrame(Table6, columns=("States","Years","Quarter", "Districts",
                                        "RegisterUser", "AppOpens"))

#top_ins
cursor.execute("Select * From top_insurance")
mydb.commit()
Table7=cursor.fetchall()
top_ins=pd.DataFrame(Table7, columns=("States","Years","Quarter", "Pincodes",
                                        "Transaction_count", "Transaction_amount"))

#top_tran
cursor.execute("Select * From top_transaction")
mydb.commit()
Table8=cursor.fetchall()
top_tran=pd.DataFrame(Table8, columns=("States","Years","Quarter", "Pincodes",
                                        "Transaction_count", "Transaction_amount"))

#top_user
cursor.execute("Select * From top_user")
mydb.commit()
Table9=cursor.fetchall()
top_user=pd.DataFrame(Table9, columns=("States","Years","Quarter", "Pincodes",
                                        "RegisteredUsers"))

def Transaction_amount_count_Y(df,year,context="default"):
    TACY=df[df["Years"]==year]
    TACY.reset_index(drop=True,inplace=True)
    TACYG=TACY.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    TACYG.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(TACYG, x="States",y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount, key=f"{context}_amount_{year}_{uuid.uuid4().hex}")

    with col2:
        fig_count=px.bar(TACYG, x="States",y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count, key=f"{context}_count_{year}_{uuid.uuid4().hex}")

    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(TACYG, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(TACYG["Transaction_amount"].min(), TACYG["Transaction_amount"].max()),
                                hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1, key=f"{context}_map_amount_{year}_{uuid.uuid4().hex}")
    with col2:
        fig_india_2=px.choropleth(TACYG, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(TACYG["Transaction_count"].min(), TACYG["Transaction_count"].max()),
                                hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2, key=f"{context}_map_count_{year}_{uuid.uuid4().hex}")
        return TACY

def Transaction_amount_count_Y_Q(df,quarter):
    import uuid  # For unique key generation
    unique_id = str(uuid.uuid4())
    TACY=df[df["Quarter"]==quarter]
    TACY.reset_index(drop=True,inplace=True)
    TACYG=TACY.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    TACYG.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(TACYG, x="States",y="Transaction_amount", title=f"{TACY['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount,key=f"fig_amount_{quarter}_{unique_id}")

    with col2:
        fig_count=px.bar(TACYG, x="States",y="Transaction_count", title=f"{TACY['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count,key=f"fig_count_{quarter}_{unique_id}")
    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(TACYG, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(TACYG["Transaction_amount"].min(), TACYG["Transaction_amount"].max()),
                                hover_name="States",title=f"{TACY['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1,key=f"fig_india_1_{quarter}_{unique_id}")
    with col2:
        fig_india_2=px.choropleth(TACYG, geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(TACYG["Transaction_count"].min(), TACYG["Transaction_count"].max()),
                                hover_name="States",title=f"{TACY['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2,key=f"fig_india_2_{quarter}_{unique_id}")
    return TACY

def agg_tran_type(df, state):
    TACY = df[df["States"] == state]
    TACY.reset_index(drop=True, inplace=True)

    TACYG = TACY.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    TACYG.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame=TACYG, names="Transaction_type", values="Transaction_amount", width=600,
                            title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.5)
        # Generate a unique key for the first pie chart
        #unique_key_1 = f"{state}_{context}_amount_pie_{uuid.uuid4()}"
        st.plotly_chart(fig_pie_1)#, key=unique_key_1)

    with col2:
        fig_pie_2 = px.pie(data_frame=TACYG, names="Transaction_type", values="Transaction_count", width=600, 
                           title=f"{state.upper()} TRANSACTION COUNT",hole=0.5)
        # Generate a unique key for the second pie chart
        #unique_key_2 = f"{state}_{context}_count_pie_{uuid.uuid4()}"
        st.plotly_chart(fig_pie_2)#, key=unique_key_2)

#Aggregated user

def agg_user_plot1(df, year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True, inplace=True)
    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1= px.bar(aguyg, x= "Brands", y= "Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width=800, color_discrete_sequence=px.colors.sequential.haline,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#AGG_USER_ANALYSIS

def agg_user_plot2(df, quarter):
    aguyq=df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1= px.bar(aguyqg, x= "Brands", y= "Transaction_count", title= f"{quarter} QUARTER - BRANDS AND TRANSACTION COUNT",
                    width=800, color_discrete_sequence=px.colors.sequential.Magenta_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    return aguyq

def agg_user_plot3(df,state):
    auyqs=df[df["States"]==state]
    auyqs.reset_index(drop=True,inplace=True)

    fig_line_1= px.line(auyqs,x="Brands",y="Transaction_count",hover_data="Percentage",
                        title=f"{state.upper()} - BRANDS, TRANSACTION COUNT, PERCENTAGE", width=1000, markers=True)
    st.plotly_chart(fig_line_1)
    
#map_ins_district

def map_ins_districts(df, state):
    TACY = df[df["States"] == state]
    TACY.reset_index(drop=True, inplace=True)

    TACYG = TACY.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    TACYG.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(
            data_frame=TACYG,
            x="Transaction_amount",
            y="Districts",
            orientation="h",
            height=600,
            title=f"{state.upper()} DISTRICT, AMOUNT",
            color_discrete_sequence=px.colors.sequential.Aggrnyl,
        )
        st.plotly_chart(fig_bar_1)#, key=f"{state}_{context}_amount_chart")
    with col2:
        fig_bar_2 = px.bar(
            data_frame=TACYG,
            x="Transaction_count",
            y="Districts",
            orientation="h",
            height=600,
            title=f"{state.upper()} DISTRICT, COUNT",
            color_discrete_sequence=px.colors.sequential.Bluered_r,
        )
        st.plotly_chart(fig_bar_2)#, key=f"{state}_{context}_count_chart")


def map_tran_districts(df, state):
    TACY = df[df["States"] == state]
    TACY.reset_index(drop=True, inplace=True)

    TACYG = TACY.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    TACYG.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_bar_1= px.bar(
            data_frame=TACYG,
            x="Transaction_amount",
            y="Districts",
            orientation="h",
            height=600,
            title=f"{state} STATES, DISTRICT, TRANSACTION AMOUNT",
            color_discrete_sequence=px.colors.sequential.Aggrnyl,
        )
        # Generate a unique key by combining state, chart type, and UUID
        #unique_key_1 = f"{state}_amount_chart_{uuid.uuid4()}"
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2= px.bar(
            data_frame=TACYG,
            x="Transaction_count",
            y="Districts",
            orientation="h",
            height=600,
            title=f"{state} STATES, DISTRICT, TRANSACTION COUNT",
            color_discrete_sequence=px.colors.sequential.Bluered_r,
        )
        # Generate a unique key by combining state, chart type, and UUID
        #unique_key_2 = f"{state}_count_chart_{uuid.uuid4()}"
        st.plotly_chart(fig_bar_2)

# map_user_plot_1
def map_user_plot_1(df,year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop=True, inplace=True)
    muyg=muy.groupby("States")[["RegisterUser","AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1= px.line(muyg,x="States",y=["RegisterUser","AppOpens"],
                        title=f"{year} REGISTER USER, APPOPENS", width=1000, height=800, markers=True)
    st.plotly_chart(fig_line_1)
    return muy

# map_user_plot_2
def map_user_plot_2(df,quarter):
    muyq=df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True, inplace=True)

    muygq=muyq.groupby("States")[["RegisterUser","AppOpens"]].sum()
    muygq.reset_index(inplace=True)

    fig_line_1= px.line(muygq,x="States",y=["RegisterUser","AppOpens"],
                        title=f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTER USER, APPOPENS", width=1000, height=800, markers=True,
                        color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)
    return muyq

#map_user_plot_3

def map_user_plot_3(df,states):
    muyqs=df[df["States"]==states]
    muyqs.reset_index(drop=True, inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_map_user_bar_1=px.bar(muyqs, x="RegisterUser", y="Districts", orientation="h",
                                title= f"{states.upper()} REGISTERED USER", height=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2=px.bar(muyqs, x="AppOpens", y="Districts", orientation="h",
                                title= f"{states.upper()} APP OPENS", height=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_2)

#top_ins_plot1

def top_ins_plot1(df,state):
    tiy=df[df["States"]==state]
    tiy.reset_index(drop=True, inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_top_ins_bar_1=px.bar(tiy, x="Quarter", y="Transaction_amount", hover_data="Pincodes",
                                    title= "TRANSACTION AMOUNT", height=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_top_ins_bar_1)

    with col2:
        fig_top_ins_bar_2=px.bar(tiy, x="Quarter", y="Transaction_count", hover_data="Pincodes",
                                    title= "TRANSACTION COUNT", height=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_top_ins_bar_2)

def top_user_plot_1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True, inplace=True)
    tuyg=pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1=px.bar(tuyg,x="States",y="RegisteredUsers",color="Quarter",width=1000, height=800,
                        color_discrete_sequence=px.colors.sequential.Burgyl,hover_name="States",
                        title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy

#top_user_plot_2
def top_user_plot_2(df,states):
    tuys=df[df["States"]=="Andaman & Nicobar"]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2= px.bar(tuys,x="Quarter", y="RegisteredUsers", title="REGISTERED USER, PINCODES, QUARTER",
                        width=1000,height=800,color="RegisteredUsers",hover_data="Pincodes",
                        color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)

#top chart

def top_chart_transaction_amount(table_name): 
    mydb = psycopg2.connect(
        host="localhost",
        user="postgres",  # Correct parameter is 'user'
        port="5432",
        database="phonepe",
        password="1234"
    )
    cursor = mydb.cursor()

    query1=f"""SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;"""

    cursor.execute(query1)
    table1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table1,columns=("states","transaction_amount"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(df_1, x="states",y="transaction_amount", title= "TOP 10 OF TRANSACTION AMOUNT",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=500)
        st.plotly_chart(fig_amount)

    query2=f"""SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount
                LIMIT 10;"""

    cursor.execute(query2)
    table2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=("states","transaction_amount"))

    with col2:
        fig_amount2=px.bar(df_2, x="states",y="transaction_amount", title= "LAST 10 OF TRANSACTION AMOUNT",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=500)
        st.plotly_chart(fig_amount2)

    query3=f"""SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;"""

    cursor.execute(query3)
    table3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=("states","transaction_amount"))

    fig_amount3=px.bar(df_3, y="states",x="transaction_amount", title= "AVERAGE OF TRANSACTION AMOUNT",hover_name="states",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=800,width=1000)
    st.plotly_chart(fig_amount3)

def top_chart_transaction_count(table_name): 
    mydb = psycopg2.connect(
        host="localhost",
        user="postgres",  # Correct parameter is 'user'
        port="5432",
        database="phonepe",
        password="1234"
    )
    cursor = mydb.cursor()

    query1=f"""SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;"""

    cursor.execute(query1)
    table1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table1,columns=("states","transaction_count"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df_1, x="states",y="transaction_count", title= "TOP 10 OF TRANSACTION COUNT",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)

    query2=f"""SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;"""

    cursor.execute(query2)
    table2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=("states","transaction_count"))

    with col2:
        fig_amount2=px.bar(df_2, x="states",y="transaction_count", title= "LAST 10 OF TRANSACTION COUNT",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount2)

    query3=f"""SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;"""

    cursor.execute(query3)
    table3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=("states","transaction_count"))

    fig_amount3=px.bar(df_3, y="states",x="transaction_count", title= "AVERAGE OF TRANSACTION COUNT",hover_name="states",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(fig_amount3)

def top_chart_registereduser(table_name, state): 
    mydb = psycopg2.connect(
        host="localhost",
        user="postgres",  # Correct parameter is 'user'
        port="5432",
        database="phonepe",
        password="1234"
    )
    cursor = mydb.cursor()

    query1=f"""SELECT districts, SUM(registeruser) AS registeruser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registeruser DESC
                LIMIT 10;"""

    cursor.execute(query1)
    table1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table1,columns=("districts","registeruser"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df_1, x="districts",y="registeruser", title= "TOP 10 OF REGISTERED USER",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)

    query2=f"""SELECT districts, SUM(registeruser) AS registeruser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registeruser
                LIMIT 10;"""

    cursor.execute(query2)
    table2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=("districts","registeruser"))

    with col2:
        fig_amount2=px.bar(df_2, x="districts",y="registeruser", title= "LAST 10 OF REGISTERED USER",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount2)

    query3=f"""SELECT districts, AVG(registeruser) AS registeruser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registeruser;"""

    cursor.execute(query3)
    table3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=("districts","registeruser"))

    fig_amount3=px.bar(df_3, y="districts",x="registeruser", title= "AVERAGE OF REGISTERED USER",hover_name="districts",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(fig_amount3)

def top_chart_appopens(table_name, state): 
    mydb = psycopg2.connect(
        host="localhost",
        user="postgres",  # Correct parameter is 'user'
        port="5432",
        database="phonepe",
        password="1234"
    )
    cursor = mydb.cursor()

    query1=f"""SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;"""

    cursor.execute(query1)
    table1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table1,columns=("districts","appopens"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df_1, x="districts",y="appopens", title= "TOP 10 OF APPOPENS",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)

    query2=f"""SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;"""

    cursor.execute(query2)
    table2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=("districts","appopens"))

    with col2:
        fig_amount2=px.bar(df_2, x="districts",y="appopens", title= "LAST 10 OF APPOPENS",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount2)

    query3=f"""SELECT districts, AVG(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens;"""

    cursor.execute(query3)
    table3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=("districts","appopens"))

    fig_amount3=px.bar(df_3, y="districts",x="appopens", title= "AVERAGE OF APPOPENS",hover_name="districts",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(fig_amount3)

def top_chart_registeredusers(table_name): 
    mydb = psycopg2.connect(
        host="localhost",
        user="postgres",  # Correct parameter is 'user'
        port="5432",
        database="phonepe",
        password="1234"
    )
    cursor = mydb.cursor()

    query1=f"""SELECT states, SUM(registeredusers) AS registetedusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registetedusers DESC
                LIMIT 10;"""

    cursor.execute(query1)
    table1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table1,columns=("states","registerusers"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(df_1, x="states",y="registerusers", title= "TOP 10 OF REGISTERED USERS",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)

    query2=f"""SELECT states, SUM(registeredusers) AS registetedusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registetedusers
                LIMIT 10;"""

    cursor.execute(query2)
    table2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=("states","registerusers"))

    with col2:
        fig_amount2=px.bar(df_2, x="states",y="registerusers", title= "LAST 10 OF REGISTERED USERS",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount2)

    query3=f"""SELECT states, AVG(registeredusers) AS registetedusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registetedusers;"""

    cursor.execute(query3)
    table3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=("states","registerusers"))

    fig_amount3=px.bar(df_3, y="states",x="registerusers", title= "AVERAGE OF REGISTERED USERS",hover_name="states",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(fig_amount3)

#streamlit part
#st.set_page_config(layout="wide")

st.title("PHONEPE DATA VISUALIZATION")

with st.sidebar:
    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select=="HOME":
    
    col1,col2=st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("Phonepe is an Indian digital payments and financial technology company")
        st.write("*****FEATURES****")
        st.write("*****CREDIT AND DEBIT CARD LINKING****")
        st.write("*****BANK BALANCE CHECK****")
        st.write("*****MONEY STORAGE****")
        st.write("*****PIN AUTHORIZATION****")
elif select == "DATA EXPLORATION":

    tab1,tab2,tab3=st.tabs(["AGGREGATED ANALYSIS","MAP ANALYSIS", "TOP ANALYSIS"])
    
    with tab1:
        method=st.radio("SELECT THE METHOD",["AGGREGATED INSURANCE","AGGREGATED TRANSACTION","AGGREGATED USER"])

        if method== "AGGREGATED INSURANCE":

            col1,col2=st.columns(2)
            with col1:
                years=st.slider("SELECT THE YEAR",Agg_ins["Years"].min(),Agg_ins["Years"].max(),Agg_ins["Years"].min())
            tac_Y=Transaction_amount_count_Y(Agg_ins,years)
            col1,col2=st.columns(2)
            with col1:            
                quarters=st.slider("SELECT THE Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y,quarters)

        elif method== "AGGREGATED TRANSACTION":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("SELECT THE YEAR",Agg_tran["Years"].min(),Agg_tran["Years"].max(),Agg_tran["Years"].min())
            agg_tran_tac_Y=Transaction_amount_count_Y(Agg_tran,years)
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("SELECT THE STATE",agg_tran_tac_Y["States"].unique())

            agg_tran_type(agg_tran_tac_Y, states)

            col1,col2=st.columns(2)
            with col1:            
                quarters=st.slider("SELECT THE Quarter",agg_tran_tac_Y["Quarter"].min(),agg_tran_tac_Y["Quarter"].max(),agg_tran_tac_Y["Quarter"].min())
            agg_tran_tac_Y_Q= Transaction_amount_count_Y_Q(agg_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("SELECT THE STATE_Ty",agg_tran_tac_Y_Q["States"].unique())

            agg_tran_type(agg_tran_tac_Y_Q, states)

        elif method== "AGGREGATED USER":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("SELECT THE YEAR",Agg_user["Years"].min(),Agg_user["Years"].max(),Agg_user["Years"].min())
            agg_user_year=agg_user_plot1(Agg_user, years)

            col1,col2=st.columns(2)
            with col1:            
                quarters=st.slider("SELECT THE Quarter",agg_user_year["Quarter"].min(),agg_user_year["Quarter"].max(),agg_user_year["Quarter"].min())
            agg_tran_tac_Y_Q= agg_user_plot2(agg_user_year,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("SELECT THE STATE",agg_tran_tac_Y_Q["States"].unique())

            agg_user_plot3(agg_tran_tac_Y_Q,states)

    with tab2:
        method2=st.radio("SELECT THE METHOD",["MAP INSURANCE","MAP TRANSACTION","MAP USER"])

        if method2== "MAP INSURANCE":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("SELECT THE YEAR", map_ins["Years"].min(), map_ins["Years"].max(), map_ins["Years"].min(),key="year_slider_map")
            map_ins_tac_Y = Transaction_amount_count_Y(map_ins, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATE(MAP)", map_ins_tac_Y["States"].unique(),key="state_select_map")

            map_ins_districts(map_ins_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("SELECT THE Quarter", map_ins_tac_Y["Quarter"].min(), map_ins_tac_Y["Quarter"].max(),
                                    map_ins_tac_Y["Quarter"].min(),key="quarter_slider_map")
            map_ins_tac_Y_Q = Transaction_amount_count_Y_Q(map_ins_tac_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATE_Ty", map_ins_tac_Y_Q["States"].unique(),key="state_select_ty")

            map_ins_districts(map_ins_tac_Y_Q, states)


        elif method2== "MAP TRANSACTION":

            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("SELECT THE YEAR_mi", map_tran["Years"].min(), map_tran["Years"].max(), map_tran["Years"].min())
            map_tran_tac_Y = Transaction_amount_count_Y(map_tran, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("SELECT THE STATE_mi", map_tran_tac_Y["States"].unique())

            map_tran_districts(map_tran_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("SELECT THE Quarter_mt", map_tran_tac_Y["Quarter"].min(), map_tran_tac_Y["Quarter"].max(), 
                                     map_tran_tac_Y["Quarter"].min())
            map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:

                states = st.selectbox("SELECT THE STATE_MP", map_tran_tac_Y_Q["States"].unique())

            map_tran_districts(map_tran_tac_Y_Q, states)

        elif method2== "MAP USER":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("SELECT THE YEAR_mu", map_user["Years"].min(), map_user["Years"].max(), map_user["Years"].min())
            map_user_Y = map_user_plot_1(map_user, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("SELECT THE Quarter_mu", map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(),
                                    map_user_Y["Quarter"].min())
            map_user_Y_Q = map_user_plot_2(map_user_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:

                states = st.selectbox("SELECT THE STATE_mu", map_user_Y_Q["States"].unique())

            map_user_plot_3(map_user_Y_Q, states)
            
    with tab3:
        method3=st.radio("SELECT THE METHOD",["TOP INSURANCE","TOP TRANSACTION","TOP USER"])

        if method3== "TOP INSURANCE":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("SELECT THE YEAR_ti", top_ins["Years"].min(), top_ins["Years"].max(), top_ins["Years"].min())
            top_ins_tac_Y = Transaction_amount_count_Y(top_ins, years)

            col1, col2 = st.columns(2)
            with col1:

                states = st.selectbox("SELECT THE STATE_ti", top_ins_tac_Y["States"].unique())

            top_ins_plot1(top_ins_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("SELECT THE Quarter_mu", top_ins_tac_Y["Quarter"].min(), top_ins_tac_Y["Quarter"].max(),
                                    top_ins_tac_Y["Quarter"].min())
            top_ins_tac_Y_Q = Transaction_amount_count_Y_Q(top_ins_tac_Y, quarters)

        elif method3== "TOP TRANSACTION":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("SELECT THE YEAR_tt", top_tran["Years"].min(), top_tran["Years"].max(), top_tran["Years"].min())
            top_tran_tac_Y = Transaction_amount_count_Y(top_tran, years)

            col1, col2 = st.columns(2)
            with col1:

                states = st.selectbox("SELECT THE STATE_tt", top_tran_tac_Y["States"].unique())

            top_ins_plot1(top_tran_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("SELECT THE Quarter_tt", top_tran_tac_Y["Quarter"].min(), top_tran_tac_Y["Quarter"].max(),
                                    top_tran_tac_Y["Quarter"].min())
            top_ins_tac_Y_Q = Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)

        elif method3== "TOP USER":
             
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("SELECT THE YEAR_tu", top_user["Years"].min(), top_user["Years"].max(), top_user["Years"].min())
            top_user_Y = top_user_plot_1(top_user, years)

            col1, col2 = st.columns(2)
            with col1:

                states = st.selectbox("SELECT THE STATE_tt", top_user_Y["States"].unique())

            top_user_plot_2(top_user_Y, states)

elif select == "TOP CHARTS":
    
    question= st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                  "2. Transaction Amount and Count of Map Insurance",
                                                  "3. Transaction Amount and Count of Top Insurance",
                                                  "4. Transaction Amount and Count of Aggregated Transaction",
                                                  "5. Transaction Amount and Count of Map Transaction",
                                                  "6. Transaction Amount and Count of Top Transaction",
                                                  "7. Transaction Count of Aggregated User",
                                                  "8. Registered User of Map User",
                                                  "9. App Opens of Map User",
                                                  "10. Registered Users of Top User"
                                                  ])
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif question == "2. Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question == "6. Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":
    
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question == "8. Registered User of Map User":
        
        states=st.selectbox("Select the State",map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registereduser("map_user", states)

    elif question == "9. App Opens of Map User":
        
        states=st.selectbox("Select the State",map_user["States"].unique())
        st.subheader("APP OPENS")
        top_chart_appopens("map_user", states)

    elif question == "10. Registered Users of Top User":
        
        st.subheader("REGISTERED USERS")
        top_chart_registeredusers("top_user")