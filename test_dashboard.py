
import streamlit as st
import pandas as pd
import plotly.express as px


dashboard_df = pd.read_csv("dashboard_df.xls")
# ===== Genre columns (adjust based on your dataset) =====
genre_cols = ['Action', 'Comedy', 'Drama']

# ===== Sidebar Filters =====
st.sidebar.title("Filters")

year_options = ['All'] + sorted(dashboard_df['year'].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", year_options)

genre_options = ['All'] + genre_cols
selected_genre = st.sidebar.selectbox("Select Genre", genre_options)

tag_options = sorted(dashboard_df['tag'].dropna().unique())
selected_tags = st.sidebar.multiselect("Select Tags (multiple)", tag_options)

# ===== Filter function =====
def filter_movies(df, year, genre, tags):
    if year != 'All':
        df = df[df['year'] == year]
    if genre != 'All' and genre in df.columns:
        df = df[df[genre] == 1]
    if tags:
        df = df[df['tag'].isin(tags)]
    return df

filtered_df = filter_movies(dashboard_df, selected_year, selected_genre, selected_tags)

st.markdown("<h1 style='text-align:center; color:yellow;'>Movie Dashboard</h1>", unsafe_allow_html=True)

# ===== 1. Top Movies by Rating Count =====
st.subheader("Top Movies by Rating Count")
if filtered_df.empty:
    st.warning("No movies found with current filters.")
else:
    top_movies = filtered_df.groupby('title')['rating_count'].sum().reset_index().sort_values('rating_count', ascending=False).head(6)
    fig1 = px.bar(top_movies, x='rating_count', y='title', orientation='h', color_discrete_sequence=['#FFD700'])
    fig1.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font_color='yellow',
        title_font_size=22,
        title_x=0.5,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        title="Top Movies by Rating Count"
    )
    st.plotly_chart(fig1, use_container_width=True)

# ===== 2. Trending Movies (Last 5 years) =====
st.subheader("Trending Movies (Last 5 Years)")
recent_year = dashboard_df['year'].max() - 5
trending = dashboard_df[dashboard_df['year'] >= recent_year]
trending_top = trending.groupby('title')['rating_count'].sum().reset_index().sort_values('rating_count', ascending=False).head(10)
fig2 = px.bar(trending_top, x='rating_count', y='title', orientation='h', color_discrete_sequence=['#FFD700'])
fig2.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='yellow',
    title_font_size=22,
    title_x=0.5,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    title="Trending Movies (Last 5 Years)"
)
st.plotly_chart(fig2, use_container_width=True)

# ===== 3. Average Rating Over Years =====
st.subheader("Average Rating Over Years")
avg_rating_df = dashboard_df.copy()
if selected_genre != 'All' and selected_genre in avg_rating_df.columns:
    avg_rating_df = avg_rating_df[avg_rating_df[selected_genre] == 1]
trend = avg_rating_df.groupby('year').agg(avg_rating=('rating', 'mean')).reset_index()
fig3 = px.line(trend, x='year', y='avg_rating', markers=True, color_discrete_sequence=['#FFD700'])
fig3.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='yellow',
    title_font_size=22,
    title_x=0.5,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    title="Average Rating Over Years"
)
st.plotly_chart(fig3, use_container_width=True)

# ===== 4. Genre Popularity =====
st.subheader("Genre Popularity")
genre_df = dashboard_df.copy()
if selected_year != 'All':
    genre_df = genre_df[genre_df['year'] == selected_year]
genre_counts = {g: genre_df[genre_df[g] == 1]['rating_count'].sum() for g in genre_cols}
genre_pop_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Rating Count']).sort_values('Rating Count', ascending=False)
fig4 = px.bar(genre_pop_df, x='Rating Count', y='Genre', orientation='h', color_discrete_sequence=['#FFD700'])
fig4.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='yellow',
    title_font_size=22,
    title_x=0.5,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    title="Genre Popularity"
)
st.plotly_chart(fig4, use_container_width=True)

# ===== 5. Movies by Tags =====
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
        fig5.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='yellow',
            title_font_size=22,
            title_x=0.5,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            title="Movies Matching Selected Tags"
        )
        st.plotly_chart(fig5, use_container_width=True)
