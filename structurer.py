"""
Utilizing the endpoint set up by Chris, we will feed the textual data
that was scraped into the chat completions API to be parsed into a JSON format.
The fields I am extracting are:
- Character Name
- Character First Appearance
- Character Type
- Character Description
"""

import openai
from openai import RateLimitError
from openai import OpenAI
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

CONSOLE = Console()

load_dotenv()

ENDPOINT = os.getenv("API_ENDPOINT")
API_KEY = os.getenv("API_KEY")
deployment_name = "gpt-4o"
client = OpenAI(base_url=ENDPOINT, api_key=API_KEY)


# Create a schema that we can pass a structured output to the chat completions API
class Character(BaseModel):
    character_name: str
    character_first_appearance: str
    character_type: str
    character_description: str


def open_data(data, max_lines=3000):
    with open(data, "r", encoding="utf-8") as f:
        data = f.read()
    return "\n".join(data.splitlines()[:max_lines])


def parse_data(data):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=CONSOLE,
        transient=True,
    ) as progress:
        parse_task = progress.add_task("🤖 Parsing data with LLM...", total=None)

        try:
            progress.update(parse_task, description="📤 Sending request to API...")
            response = client.chat.completions.create(
                model=deployment_name,
                # response_format={"type": "json_schema", "json_schema": {"name": "character_list", "schema": Character.model_json_schema()}},
                messages=[
                    {
                        "role": "system",
                        "content": """You are a helpful assistant that parses data from a text file scraped from a website and returns it in a JSON format. You must follow the provided schema exactly.
                        Return a JSON array of character objects, where each object contains the specified fields.
                        The schema is:
                        {
                            "character_name": "string",
                            "character_first_appearance": "string",
                            "character_type": "string",
                            "character_description": "string"
                        }
                        Remember to return only the JSON array, and nothing else or additional formatting.
                        """,
                    },
                    {
                        "role": "user",
                        "content": f"Parse the following data for every character within the text, but only for the selected character types: Mascots, Guest Mascots, and Puffles: {data}",
                    },
                ],
            )
            progress.update(parse_task, description="✅ Data parsing completed!")
        # I've hit the rate limit a few times, so I added a try-except block to more gracefully handle it
        except RateLimitError as e:
            CONSOLE.print(
                f"[red]Rate limit exceeded. Please try again later. Error: {e}[/red]"
            )
            return None
    return json.loads(response.choices[0].message.content)


def main():
    data = open_data("clubpenguin.txt")
    parsed_data = parse_data(data)
    with open("parsed_data.json", "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=4)
    CONSOLE.print(f"[green]✨ Successfully saved data to parsed_data.json[/green]")


if __name__ == "__main__":
    main()
