import streamlit as st
import pandas as pd
import plotly.express as px

# === Load your data ===
dashboard_df = pd.read_csv('final_dashboard_df.xls') 

# === Genre columns ===
genre_cols = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary',
              'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery',
              'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

# === Sidebar Filters ===
st.sidebar.title("Filters")
year_options = ['All'] + sorted(dashboard_df['year'].dropna().astype(int).unique().tolist())
genre_options = ['All'] + genre_cols
tag_options = sorted(dashboard_df['tag'].dropna().unique())

selected_year = st.sidebar.selectbox("Select Year", year_options)
selected_genre = st.sidebar.selectbox("Select Genre", genre_options)
selected_tags = st.sidebar.multiselect("Select Tags (Only for 'Movies by Tags')", tag_options)

# === Helper: Filter based on Year and Genre ===
def filter_df(df, year, genre):
    if year != 'All':
        df = df[df['year'] == int(year)]
    if genre != 'All':
        df = df[df[genre] == 1]
    return df

# === Plot Style Helper ===
def update_plot_style(fig, title):
    fig.update_layout(
        title=dict(text=title, font=dict(color='#FFD700', size=22), x=0.5),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='#FFD700'),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color='#FFD700', size=14),
            title_font=dict(color='#FFD700', size=16),
            title_standoff=15
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color='#FFD700', size=14),
            title_font=dict(color='#FFD700', size=16),
            title_standoff=15
        ),
        legend=dict(font=dict(color='#FFD700', size=14))
    )
    return fig

# === Top Movies ===
def plot_top_movies():
    df = filter_df(dashboard_df.copy(), selected_year, selected_genre)
    if df.empty:
        st.warning("No data found for selected filters.")
        return
    top = df.groupby('title')['rating_count'].sum().reset_index().sort_values('rating_count', ascending=False).head(6)
    fig = px.bar(top, x='rating_count', y='title', orientation='h', color_discrete_sequence=['#FFD700'])
    fig = update_plot_style(fig, "Top Movies by Rating Count")
    st.plotly_chart(fig, use_container_width=True)

# === Trending Now ===
def plot_trending():
    recent_year = dashboard_df['year'].max() - 5
    trending = dashboard_df[dashboard_df['year'] >= recent_year]
    trending = trending.groupby('title')['rating_count'].sum().reset_index().sort_values('rating_count', ascending=False).head(10)
    fig = px.bar(trending, x='rating_count', y='title', orientation='h', color_discrete_sequence=['#FFD700'])
    fig = update_plot_style(fig, "Trending Movies")
    st.plotly_chart(fig, use_container_width=True)

# === Average Rating Over Time ===
def plot_avg_rating():
    df = dashboard_df.copy()
    if selected_genre != 'All':
        df = df[df[selected_genre] == 1]
    trend = df.groupby('year')['rating'].mean().reset_index()
    fig = px.line(trend, x='year', y='rating', markers=True, color_discrete_sequence=['#FFD700'])
    fig = update_plot_style(fig, "Average Rating Over Years")
    st.plotly_chart(fig, use_container_width=True)

# === Genre Popularity ===
def plot_genre_popularity():
    df = dashboard_df.copy()
    if selected_year != 'All':
        df = df[df['year'] == int(selected_year)]
    genre_counts = {g: df[df[g] == 1]['rating_count'].sum() for g in genre_cols}
    genre_df = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Rating Count']).sort_values(by='Rating Count', ascending=False)
    fig = px.bar(genre_df, x='Rating Count', y='Genre', orientation='h', color_discrete_sequence=['#FFD700'])
    fig = update_plot_style(fig, "Genre Popularity")
    st.plotly_chart(fig, use_container_width=True)

# === Movies by Tags (Independent) ===
def plot_by_tags():
    if not selected_tags:
        st.info("Select at least one tag to view results.")
        return
    tag_df = dashboard_df[dashboard_df['tag'].isin(selected_tags)]
    if tag_df.empty:
        st.warning("No data for selected tag(s).")
        return
    counts = tag_df.groupby('title')['rating_count'].sum().reset_index().sort_values('rating_count', ascending=False).head(10)
    fig = px.bar(counts, x='rating_count', y='title', orientation='h', color_discrete_sequence=['#FFD700'])
    fig = update_plot_style(fig, "Movies by Selected Tags")
    st.plotly_chart(fig, use_container_width=True)


# === Monthly Trends ===
def plot_monthly_trends():
#    if 'month' not in dashboard_df.columns:
#        st.warning("Month column not found in dataset.")
#        return
    month_df = dashboard_df.groupby('month')['rating'].count().reset_index(name='rating_count')
    fig = px.line(month_df, x='month', y='rating_count', markers=True, color_discrete_sequence=['#FFD700'])
    fig = update_plot_style(fig, "Monthly Rating Count")
    st.plotly_chart(fig, use_container_width=True)

# === Weekly Trends ===
def plot_weekly_trends():
#    if 'day_of_week' not in dashboard_df.columns:
#        st.warning("Day of week column not found in dataset.")
#        return
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_df = dashboard_df.groupby('day_of_week')['rating'].count().reindex(weekday_order).reset_index(name='rating_count')
    fig = px.bar(day_df, x='day_of_week', y='rating_count', color_discrete_sequence=['#FFD700'])
    fig = update_plot_style(fig, "Weekly Rating Count")
    st.plotly_chart(fig, use_container_width=True)

# === Tabs ===
tab = st.selectbox("Select View", [
    "Top Movies", 
    "Trending Now", 
    "Average Rating Over Years", 
    "Genre Popularity", 
    "Movies by Tags", 
    "Monthly Trends", 
    "Weekly Trends"
])

# === Route Tabs to Functions ===
if tab == "Top Movies":
    plot_top_movies()
elif tab == "Trending Now":
    plot_trending()
elif tab == "Average Rating Over Years":
    plot_avg_rating()
elif tab == "Genre Popularity":
    plot_genre_popularity()
elif tab == "Movies by Tags":
    plot_by_tags()
elif tab == "Monthly Trends":
    plot_monthly_trends()
elif tab == "Weekly Trends":
    plot_weekly_trends()
