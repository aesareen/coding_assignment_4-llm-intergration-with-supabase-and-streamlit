# ---
# lambda-test: false  # auxiliary-file
# ---
# ## Demo Streamlit application.
#
# This application is the example from https://docs.streamlit.io/library/get-started/create-an-app.
#
# Streamlit is designed to run its apps as Python scripts, not functions, so we separate the Streamlit
# code into this module, away from the Modal application code.
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from typing import Union


def get_supabase_client() -> Client:
    load_dotenv()
    SUPABASE_URL, SUPABASE_API_KEY = os.getenv("SUPABASE_URL"), os.getenv(
        "SUPABASE_KEY"
    )
    return create_client(SUPABASE_URL, SUPABASE_API_KEY)


def select_rows_from_table(
    client: Client, table_name: str
) -> dict[str, Union[str, float]]:
    response = client.table(table_name).select("*").limit(50).execute()
    return response.data


def get_supabase_client() -> Client:
    import os
    from dotenv import load_dotenv

    load_dotenv()
    SUPABASE_URL, SUPABASE_API_KEY = os.getenv("SUPABASE_URL"), os.getenv(
        "SUPABASE_KEY"
    )
    return create_client(SUPABASE_URL, SUPABASE_API_KEY)


def select_rows_from_table(
    client: Client, table_name: str
) -> dict[str, Union[str, float]]:
    response = client.table(table_name).select("*").limit(50).execute()
    return response.data


def main():
    import numpy as np
    import pandas as pd
    import streamlit as st
    import plotly.express as px

    # Set the browser tab title
    st.set_page_config(
        page_title="Club Penguin Wiki Characters Demo",
        page_icon="🐧",
        layout="centered",
    )

    st.title("BeautifulSoup, OpenAI Completions API, Supabase, Streamlit, and Modal Integration")
    st.write("The data is scraped from the [Club Penguin Wiki](https://clubpenguin.fandom.com/wiki/List_of_Characters_in_Club_Penguin)")
    
    @st.cache_data
    def load_data():
        client = get_supabase_client()
        wiki_character_rows = (
            pd.DataFrame(select_rows_from_table(client, "wiki_characters"))
            .set_index("character_name")
            .sort_index()
        )
        return wiki_character_rows

    df = load_data().reset_index()
    st.dataframe(df)

    # We can create a bar chart of the most popular character types with plotly
    st.plotly_chart(
        px.bar(
            df,
            x="character_type",
            y="character_name",
            color="character_type",
            labels={"character_type": "Character Type", "character_name": "Number of Characters"},
            title="Number of Characters by Type",
        )
    )

    # Use streamlit popover, we can pick a random character and display their information
    st.header("Random Character Spotlight")
    
    random_character = df.sample(1).iloc[0]
    with st.popover(random_character["character_name"]):
        # Create a nicely formatted markdown block with the character information
        st.markdown(f"**Type:** {random_character['character_type']}")
        st.markdown(f"**First Appearance:** {random_character['character_first_appearance']}")
        st.markdown(f"**Description:** {random_character['character_description']}")    

if __name__ == "__main__":
    main()
