import folium
import pandas as pd
import plotly.express as px
from dash import html


# create a map with disaster markers and their names for the last 90 days
def create_map(cursor):
    cursor.execute("""SELECT e.title as title, el.latitude as latitude, el.longitude as longitude FROM event_locations el 
    JOIN events e ON e.id =el.event_id 
    JOIN categories c ON c.id=e.category_id
    WHERE el.event_date >= CURDATE() - INTERVAL 90 DAY;""")

    events = cursor.fetchall()

    m = folium.Map(location=[20, 0], zoom_start=2)

    for event in events:
        folium.Marker(
            location=[event[1], event[2]],
            popup=event[0],
            icon=folium.Icon(color="red")
        ).add_to(m)

    m.save("map.html")
    # return map as iframe, content read from 'map.html' to display in the app
    return html.Iframe(srcDoc=open("map.html", "r").read(), width="100%", height="500")


# create a bar chart showing the number of events per month
def create_bar_diagram(conn):
    # select dates starting from 2023 because there is too little information before that
    df = pd.read_sql("""SELECT DATE_FORMAT(el.event_date, '%Y-%m') AS period, COUNT(DISTINCT e.id) AS count
                          FROM event_locations el
                          JOIN events e ON e.id = el.event_id
                          WHERE el.event_date >= '2023-01-01'
                          GROUP BY period
                          ORDER BY period;""", conn)

    fig = px.bar(df, x="period", y="count", text_auto=True)
    fig.update_layout(xaxis=dict(
        tickformat="%Y-%m",
        tickmode="linear",
        tickvals=df["period"],
        tickangle=-45,
        dtick="M1"))  # add label for every month

    return fig


# create a pie chart showing the distribution of events by season
def create_seasons_chart(conn):
    # assign each event a season based on date
    df = pd.read_sql("""SELECT COUNT(DISTINCT e.id) AS count,
        CASE
            WHEN MONTH(el.event_date) IN (12, 1, 2) THEN 'Winter'
            WHEN MONTH(el.event_date) IN (3, 4, 5) THEN 'Spring'
            WHEN MONTH(el.event_date) IN (6, 7, 8) THEN 'Summer'
            ELSE 'Fall'
        END AS season
        FROM event_locations el
        JOIN events e ON e.id = el.event_id
        GROUP BY season;""", conn)
    fig = px.pie(df, values="count", names='season')
    return fig


# create a pie chart showing the distribution of events by regions
def create_regions_chart(conn):
    # assign each event a region based on latitude and longitude
    df = pd.read_sql("""SELECT COUNT(DISTINCT el.event_id) as number,
        CASE
            WHEN el.latitude BETWEEN 36 AND 71 AND el.longitude BETWEEN -25 AND 40 THEN 'Europe'
            WHEN el.latitude BETWEEN -60 AND 80 AND el.longitude BETWEEN -170 AND -35 THEN 
                CASE 
                    WHEN el.latitude > 0 THEN 'North America'
                    ELSE 'South America'
                END
            WHEN el.latitude BETWEEN -45 AND -10 AND el.longitude BETWEEN 112 AND 155 THEN 'Australia'
            WHEN el.latitude BETWEEN -90 AND -60 THEN 'Antarctica'
            WHEN el.latitude BETWEEN 10 AND 80 AND el.longitude BETWEEN 60 AND 180 THEN 'Asia'
            WHEN el.latitude BETWEEN -35 AND 37 AND el.longitude BETWEEN -17 AND 51 THEN 'Africa'
            ELSE 'Other'
        END AS continent
    FROM event_locations el
    GROUP BY continent;
    """, conn)
    fig = px.pie(df, values="number", names="continent")
    return fig
