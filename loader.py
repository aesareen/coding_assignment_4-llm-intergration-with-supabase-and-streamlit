"""
This script will load the parsed JSON file into a Supabase database.
It will first load it in as a pandas dataframe and then insert it into the database.
"""

from dotenv import load_dotenv
import os
import json
import pandas as pd
from supabase import create_client, Client
from datetime import datetime
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console

CONSOLE = Console()

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_KEY")


def load_data_as_dataframe(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data = pd.DataFrame(data)
    data.columns = [
        "character_name",
        "character_type",
        "character_first_appearance",
        "character_description",
    ]
    # data['created_at'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    CONSOLE.print(f"[green]✨ Successfully loaded data into pandas dataframe[/green]")
    return data


def load_data_into_supabase(dataframe, table_name):
    client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Inserting data into Supabase...", start=False)
        progress.start_task(task)
        client.table(table_name).insert(dataframe.to_dict("records")).execute()
        progress.update(task, description="Insert complete!")
        CONSOLE.print(f"[green]✨ Successfully inserted data into Supabase[/green]")


def main():
    dataframe = load_data_as_dataframe("parsed_data.json")
    load_data_into_supabase(dataframe, "wiki_characters")


if __name__ == "__main__":
    main()
