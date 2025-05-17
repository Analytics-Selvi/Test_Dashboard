
import streamlit as st
import pandas as pd
import plotly.express as px

dashboard_df = pd.read_csv("dashboard_df.xls")

# ===== Full genre list =====
genre_cols = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary',
              'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery',
              'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

# ===== Sidebar Filters =====
st.sidebar.title("Filters")

year_options = ['All'] + sorted(dashboard_df['year'].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", year_options)

genre_options = ['All'] + genre_cols
selected_genre = st.sidebar.selectbox("Select Genre", genre_options)

tag_options = sorted(dashboard_df['tag'].dropna().unique())
selected_tags = st.sidebar.multiselect("Select Tags (multiple)", tag_options)

# ===== Filter function for all plots except tags plot =====
def filter_movies(df, year, genre):
    if year != 'All':
        df = df[df['year'] == year]
    if genre != 'All' and genre in df.columns:
        df = df[df[genre] == 1]
    return df

filtered_df = filter_movies(dashboard_df, selected_year, selected_genre)

# ===== Style function for plots =====
def style_plot(fig, title):
    fig.update_layout(
        title=title,
        title_font_size=26,
        title_font_color='yellow',
        title_x=0.5,
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='yellow', size=14),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        margin=dict(l=40, r=40, t=60, b=40),
        hoverlabel=dict(bgcolor="black", font_size=14, font_color="yellow"),
    )
    fig.update_xaxes(title_font=dict(size=18, color='yellow', family='Arial, sans-serif'))
    fig.update_yaxes(title_font=dict(size=18, color='yellow', family='Arial, sans-serif'))
    return fig

# ===== Title =====
st.markdown("<h1 style='text-align:center; color:yellow;'>Movie Dashboard</h1>", unsafe_allow_html=True)

# ===== 1. Top Movies by Rating Count (ignores tag filter) =====
st.subheader("Top Movies by Rating Count")
if filtered_df.empty:
    st.warning("No movies found with current filters.")
else:
    top_movies = filtered_df.groupby('title')['rating_count'].sum().reset_index().sort_values('rating_count', ascending=False).head(6)
    fig1 = px.bar(top_movies, x='rating_count', y='title', orientation='h', color_discrete_sequence=['#FFD700'])
    fig1 = style_plot(fig1, "Top Movies by Rating Count")
    st.plotly_chart(fig1, use_container_width=True)

# ===== 2. Trending Movies (Last 5 Years) (ignores tag filter) =====
st.subheader("Trending Movies (Last 5 Years)")
recent_year = dashboard_df['year'].max() - 5
trending = dashboard_df[dashboard_df['year'] >= recent_year]
trending_top = trending.groupby('title')['rating_count'].sum().reset_index().sort_values('rating_count', ascending=False).head(10)
fig2 = px.bar(trending_top, x='rating_count', y='title', orientation='h', color_discrete_sequence=['#FFD700'])
fig2 = style_plot(fig2, "Trending Movies (Last 5 Years)")
st.plotly_chart(fig2, use_container_width=True)

# ===== 3. Average Rating Over Years (ignores tag filter) =====
st.subheader("Average Rating Over Years")
avg_rating_df = dashboard_df.copy()
if selected_genre != 'All' and selected_genre in avg_rating_df.columns:
    avg_rating_df = avg_rating_df[avg_rating_df[selected_genre] == 1]
trend = avg_rating_df.groupby('year').agg(avg_rating=('rating', 'mean')).reset_index()
fig3 = px.line(trend, x='year', y='avg_rating', markers=True, color_discrete_sequence=['#FFD700'])
fig3 = style_plot(fig3, "Average Rating Over Years")
st.plotly_chart(fig3, use_container_width=True)

# ===== 4. Genre Popularity (ignores tag filter) =====
st.subheader("Genre Popularity")
genre_df = dashboard_df.copy()
if selected_year != 'All':
    genre_df = genre_df[genre_df['year'] == selected_year]
genre_counts = {g: genre_df[genre_df[g] == 1]['rating_count'].sum() for g in genre_cols}
genre_pop_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Rating Count']).sort_values('Rating Count', ascending=False)
fig4 = px.bar(genre_pop_df, x='Rating Count', y='Genre', orientation='h', color_discrete_sequence=['#FFD700'])
fig4 = style_plot(fig4, "Genre Popularity")
st.plotly_chart(fig4, use_container_width=True)

# ===== 5. Movies by Tags (affected by tags filter only) =====
st.subheader("Movies by Tags")
if not selected_tags:
    st.info("Select at least one tag to filter movies by tags.")
else:
    tags_df = dashboard_df[dashboard_df['tag'].isin(selected_tags)]
    if tags_df.empty:
        st.warning("No movies found for the selected tag(s).")
    else:
        tag_counts = tags_df.groupby('title')['rating_count'].sum().reset_index().sort_values('rating_count', ascending=False).head(10)
        fig5 = px.bar(tag_counts, x='rating_count', y='title', orientation='h', color_discrete_sequence=['#FFD700'])
        fig5 = style_plot(fig5, "Movies Matching Selected Tags")
        st.plotly_chart(fig5, use_container_width=True)
