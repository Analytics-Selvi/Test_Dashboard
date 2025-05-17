import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Movie Explorer by Tag", layout="wide")
st.title(" Movie Explorer by Tag")

# Load your data
@st.cache_data
def load_data():
    # Replace this with your actual data loading
    # Example: pd.read_csv("your_dashboard_df.csv")
    df = pd.read_csv("dashboard_df.csv")
    return df

dashboard_df = load_data()

# Validate essential columns
required_cols = {'title', 'rating_count', 'tag'}
if not required_cols.issubset(set(dashboard_df.columns)):
    st.error(f"Missing columns in data: {required_cols - set(dashboard_df.columns)}")
    st.stop()

# Sidebar tag filter
unique_tags = sorted(dashboard_df['tag'].dropna().unique())
selected_tag = st.sidebar.selectbox("Select a Tag", unique_tags)

# Filter data
filtered_df = dashboard_df[dashboard_df['tag'] == selected_tag]

# Top movies plot
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
