import json
from enum import Enum

from typing import Annotated

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class NewsModel(BaseModel):
    

    country: str = Field(
        None, title='Country', description='the country of the location',
        required=False
    )

    region: str = Field(
        None, title='Region', description='the region of the location',
        required=False
    )

    city: str = Field(
        None, title='City', description='the city of the location',
        required=False
    )

    approximate_location: list[float] = Field(
        None, title='Approximate Location', description='the approximate location of the location (lat, lon)',
        required=False
    )

    short_description: str = Field(
        ...,
        title='Short Description',
        description='this is the short description of the news',
    )

    

main_model_schema = NewsModel.model_json_schema()  # (1)!
print(json.dumps(main_model_schema, indent=2))  # (2)!


specific_instruction = "Summarize the provided text into a concise version, capturing the key points and main ideas."
json_schema = {
    "summary": "string",
    "key_points": "array of strings",
    "length": "number (number of words in summary)"
}


def get_system_prompt(analysis_type: str, instruction: str, json_schema: dict) -> str:
    # Format the JSON schema into a string representation
    json_schema_str = json.dumps(json_schema, indent=4)

    # Construct the system prompt with updated instruction
    return (f"You are a data analyst API capable of {analysis_type} analysis. "
            f"{instruction} Please respond with your analysis directly in JSON format "
            f"(without using Markdown code blocks or any other formatting). "
            f"The JSON schema should include: {{{json_schema_str}}}.")


if __name__ == '__main__':
    builder = SchemaBuilder()
    builder.add_schema({"type": "object", "properties": {}})
    builder.add_object({"hi": "there"})
    builder.add_object({"hi": 5})
