import os
from typing import Optional
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

class Instruct:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the Instruct class with the specified API key.

        Args:
            api_key (str, optional): The OpenAI API key. Defaults to None.

        Example:
            >>> instructor = Instruct

        Raises:
            ValueError: If the OpenAI API key is not available.
        """
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OpenAI API key is not available")
        self.llm = instructor.patch(OpenAI(api_key=api_key))

    def invoke(
        self,
        system: Optional[str] = None,
        query: Optional[str] = None,
        model: str = None,
        pydantic_model=None,
    ):
        if query is None:
            raise ValueError("Query is required for invoke()")

        if system is None:
            system = "You are a helpful assistant."

        if model is None:
            model = "gpt-3.5-turbo-1106"
        if model == "3":
            model = "gpt-3.5-turbo-1106"
        elif model == "4":
            model = "gpt-4-turbo-preview"

        completion = self.llm.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": query},
            ],
            response_model=pydantic_model,
        )

        if pydantic_model is None:
            return completion.choices[0].message.content
        else:
            return completion.completion

    def instruct(
        self,
        system: Optional[str] = None,
        query: Optional[str] = None,
        model: str = None,
        field_name: str = "result",
        field_type: str = "str",
        field_description: Optional[str] = None,
    ):
        if query is None:
            raise ValueError("Query is required for instruct()")

        class DynamicModel(BaseModel):
            pass

        field_type_mapping = {
            "str": str,
            "list": list,
        }

        field = Field(
            ...,
            description=field_description,
        )

        setattr(DynamicModel, field_name, field_type_mapping[field_type](field))

        completion = self.invoke(
            system=system,
            query=query,
            model=model,
            pydantic_model=DynamicModel,
        )

        return getattr(completion, field_name)

#====================================================================================================

if __name__ == "__main__":
    instructor = Instruct()
    completion = instructor.instruct(
        query="What is the capital of France?",
        field_name="capital",
        field_type="str",
        field_description="The capital city of France",
    )
    print(completion)