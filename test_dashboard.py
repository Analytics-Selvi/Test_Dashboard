import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Movie Explorer by Tag", layout="wide")
st.title("🎬 Movie Explorer by Tag")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/your-username/your-repo/main/dashboard_df.csv"
    return pd.read_csv(url)

Dasbboard_df = load_data()

required_cols = {'title', 'rating_count', 'tag'}
if not required_cols.issubset(set(dashboard_df.columns)):
    st.error(f"Missing columns in data: {required_cols - set(dashboard_df.columns)}")
    st.stop()

unique_tags = sorted(dashboard_df['tag'].dropna().unique())
selected_tag = st.sidebar.selectbox("Select a Tag", unique_tags)

filtered_df = dashboard_df[dashboard_df['tag'] == selected_tag]

if not filtered_df.empty:
    top_movies = (filtered_df
                  .groupby('title', as_index=False)['rating_count']
                  .sum()
                  .sort_values(by='rating_count', ascending=False)
                  .head(10))

    fig = px.bar(top_movies,
                 x='rating_count',
                 y='title',
                 orientation='h',
                 title=f"Top Movies for Tag: {selected_tag}",
                 labels={'rating_count': 'Rating Count', 'title': ''},
                 template='plotly_dark',
                 color_discrete_sequence=['#FFD700'])

    fig.update_layout(
        yaxis=dict(categoryorder='total ascending'),
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#FFD700')
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No movies found for the selected tag.")
