import streamlit as st
import pandas as pd
import plotly.express as px

# ===== Load Data =====
@st.cache_data
def load_data():
    return pd.read_csv("dashboard_df.xls")

dashboard_df = load_data()

# ===== Genre Columns =====
genre_cols = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary',
              'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery',
              'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

# ===== Sidebar Filters =====
st.sidebar.title("Filter Movies")
year_options = ['All'] + sorted(dashboard_df['year'].dropna().astype(int).unique().tolist())
genre_options = ['All'] + genre_cols
tag_options = sorted(dashboard_df['tag'].dropna().unique())

year = st.sidebar.selectbox("Year", year_options)
genre = st.sidebar.selectbox("Genre", genre_options)
tags = st.sidebar.multiselect("Tags (For Tag Tab)", tag_options)

# ===== Filter Function =====
def filter_movies(year, genre):
    df = dashboard_df.copy()
    if year != 'All':
        df = df[df['year'] == int(year)]
    if genre != 'All' and genre in df.columns:
        df = df[df[genre] == 1]
    return df

# ===== Title =====
st.markdown("<h1 style='text-align: center; color: gold;'>🎬 Movie Dashboard</h1>", unsafe_allow_html=True)

# ===== Tabs =====
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Top Movies", "Trending Now", "Average Rating Over Years", "Genre Popularity", "Movies by Tags"
])

# ===== 1. Top Movies Tab =====
with tab1:
    df = filter_movies(year, genre)
    if df.empty:
        st.warning("No movies found with current filters.")
    else:
        top = df.groupby('title')['rating_count'].sum().reset_index().sort_values('rating_count', ascending=False).head(6)
        fig = px.bar(top, x='rating_count', y='title', orientation='h', color_discrete_sequence=['#FFD700'])
        fig.update_layout(
            title="Top Movies by Rating Count", title_x=0.5,
            plot_bgcolor='black', paper_bgcolor='black',
            font_color='yellow'
        )
        st.plotly_chart(fig, use_container_width=True)

# ===== 2. Trending Now Tab =====
with tab2:
    recent_year = dashboard_df['year'].max() - 5
    trending = dashboard_df[dashboard_df['year'] >= recent_year]
    trending = trending.groupby('title')['rating_count'].sum().reset_index().sort_values('rating_count', ascending=False).head(10)
    fig = px.bar(trending, x='rating_count', y='title', orientation='h', color_discrete_sequence=['#FFD700'])
    fig.update_layout(title="Trending Movies (Last 5 Years)", title_x=0.5, plot_bgcolor='black', paper_bgcolor='black', font_color='yellow')
    st.plotly_chart(fig, use_container_width=True)

# ===== 3. Average Rating Over Years Tab =====
with tab3:
    df = dashboard_df.copy()
    if genre != 'All' and genre in df.columns:
        df = df[df[genre] == 1]
    trend = df.groupby('year').agg(avg_rating=('rating', 'mean')).reset_index()
    fig = px.line(trend, x='year', y='avg_rating', markers=True, color_discrete_sequence=['#FFD700'])
    fig.update_layout(title="Average Rating Over Years", title_x=0.5, plot_bgcolor='black', paper_bgcolor='black', font_color='yellow')
    st.plotly_chart(fig, use_container_width=True)

# ===== 4. Genre Popularity Tab =====
with tab4:
    df = dashboard_df.copy()
    if year != 'All':
        df = df[df['year'] == int(year)]
    genre_counts = {g: df[df[g] == 1]['rating_count'].sum() for g in genre_cols}
    genre_df = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Rating Count']).sort_values(by='Rating Count', ascending=False)
    fig = px.bar(genre_df, x='Rating Count', y='Genre', orientation='h', color_discrete_sequence=['#FFD700'])
    fig.update_layout(title="Genre Popularity", title_x=0.5, plot_bgcolor='black', paper_bgcolor='black', font_color='yellow')
    st.plotly_chart(fig, use_container_width=True)

# ===== 5. Movies by Tags Tab =====
with tab5:
    if not tags:
        st.info("Please select at least one tag.")
    else:
        filtered_tags_df = dashboard_df[dashboard_df['tag'].isin(tags)]
        if filtered_tags_df.empty:
            st.warning("No movies found for selected tag(s).")
        else:
            counts = filtered_tags_df.groupby('title')['rating_count'].sum().reset_index().sort_values('rating_count', ascending=False).head(10)
            fig = px.bar(counts, x='rating_count', y='title', orientation='h', color_discrete_sequence=['#FFD700'])
            fig.update_layout(title="Movies Matching Selected Tags", title_x=0.5, plot_bgcolor='black', paper_bgcolor='black', font_color='yellow')
            st.plotly_chart(fig, use_container_width=True)
