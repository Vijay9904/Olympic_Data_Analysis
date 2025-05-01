import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')
df=preprocessor.preprocess(df,region_df)
st.sidebar.title("olympics Analysis")
st.sidebar.image('https://cdn.wallpapersafari.com/0/72/S307o5.jpg')
user_name=st.sidebar.radio(
    'select an option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete wise Analysis')
)
#st.dataframe(df)
if user_name == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select country", country)

    medaltally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country =='Overall':
        st.title("Overall Tally")
    if selected_year !='Overall' and selected_country =='Overall':
        st.title("Medal tally in"+ str(selected_year)+  "Olympics")
    if selected_year =='Overall' and selected_country !='Overall':
        st.title(selected_country +" Overall performance")
    if selected_year !='Ovreall' and selected_country!='Overall':
        st.title(selected_country +"performance in " + str(selected_year)+ "Olympics")
    st.table(medaltally)


if user_name == 'Overall Analysis':
    editions =df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports =df['Sport'].unique().shape[0]
    events =df['Event'].unique().shape[0]
    athletes =df['Name'].unique().shape[0]
    nations =df['region'].unique().shape[0]
    st.title("TOP Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
         st.header("Editions")
         st.title(editions)
    with col2:
         st.header("HOSTS")
         st.title(cities)
    with col3:
         st.header("SPORTS")
         st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
         st.header("Events")
         st.title(events)
    with col2:
         st.header("Nations")
         st.title(nations)
    with col3:
         st.header("Athletes")
         st.title(athletes)


    # Assuming df is already defined somewhere
    nations_over_time = helper.data_over_time(df,'region')

    # Plotting the data for regions over time
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participation Nations Over The Years")
    st.plotly_chart(fig)
    events_over_time = helper.data_over_time(df, 'Event')

    # Plotting the data for regions over time
    fig = px.line( events_over_time, x="Edition", y="Event")
    st.title("Events Over The Years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')

    # Plotting the data for regions over time
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.title("Athletes Over The Years")
    st.plotly_chart(fig)

    st.title("No of Events over time(Every Sport)")

    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    Ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc="count").fillna(0).astype('int'),annot=True)
    st.pyplot(fig)
    st.title("Most Successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select  a sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_name == 'Country-Wise Analysis':

    st.sidebar.title("Country Wise Analysis")
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox('select a country',country_list)
    country_df=helper.year_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title( selected_country + "Medal tally Over The Years")
    st.plotly_chart(fig)

    st.title(selected_country + "Excels in the following sports")
    pt = helper.country_event_headmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    Ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("TOP 10 Athletes of "+selected_country)

    top10_df= helper.most_successful(df,selected_country)
    st.table(top10_df)

if user_name == 'Athlete wise Analysis':
   athlete_df = df.drop_duplicates(subset=['Name', 'region'])

   x1 = athlete_df['Age'].dropna()
   x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
   x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
   x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

   fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Brozen Medalist'],
                            show_hist=False, show_rug=False)

   st.title("Distribution of Age")
   st.plotly_chart(fig)

   x = []
   name = []
   famous_sports = [
       'Basketball', 'Judo', 'Football', 'Tug-of-war', 'Athletics', 'Swimming',
       'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions', 'Handball',
       'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing', 'Fencing',
       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis',
       'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming',
       'Table Tennis', 'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens',
       'Beach volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey'
   ]

   for sport in famous_sports:
       temp_df = athlete_df[athlete_df['Sport'] == sport]  # Updated column name from 'sport' to 'Sport'
       x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
       name.append(sport)
   filtered_x = [age_data for age_data in x if len(age_data) > 0]
   filtered_name = [sport for i, sport in enumerate(name) if len(x[i]) > 0]

   # Create the distplot with filtered data
   fig = ff.create_distplot(filtered_x, filtered_name, show_hist=False, show_rug=False)
   st.title("Distribution of Age wrt sports(GOLD Medalist)")
   st.plotly_chart(fig)

   sport_list = df['Sport'].unique().tolist()
   sport_list.sort()
   sport_list.insert(0, 'Overall')

   st.title("Height VS Weight")
   selected_sport = st.selectbox('Select  a sport', sport_list)
   temp_df=helper.weight_v_height(df,selected_sport)
   fig,ax=plt.subplots()
   Ax=sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=100)
   st.plotly_chart(fig)

   st.title("Men VS Women Participation Over the Years")
   final=helper.men_vs_women(df)
   fig = px.line(final, x="Year", y=["Male", "Female"])
   st.plotly_chart(fig)


    # Now for events over time


