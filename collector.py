"""
Continuing with the theme of the last project, I will be scraping Club Penguin Information
Using the Club Penguin Wiki. This will leverage beautifulsoup4 to scrape the website.
Then the data will be saved in a text file for later LLM parsing.
We also use rich to show a progress bar and a spinner while the data is being scraped and written to the file.
"""

import requests
from bs4 import BeautifulSoup
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

CONSOLE = Console()


def scrape_data(url):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=CONSOLE,
        transient=True,
    ) as progress:
        # Add task for fetching data
        fetch_task = progress.add_task(
            "🌐 Fetching data from Club Penguin Wiki...", total=None
        )

        response = requests.get(url)
        progress.update(fetch_task, description="🔄 Processing HTML content...")

        soup = BeautifulSoup(response.text, "html.parser")

        progress.update(fetch_task, description="✅ Data fetching completed!")

    # Return HTML without prettify formatting to reduce whitespace
    return soup.get_text()


def main(filename):
    URL = "https://clubpenguin.fandom.com/wiki/List_of_Characters_in_Club_Penguin"
    data = scrape_data(URL)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

    CONSOLE.print(f"[green]✨ Successfully saved data to {filename}[/green]")
    return data


if __name__ == "__main__":
    main("clubpenguin.txt")
