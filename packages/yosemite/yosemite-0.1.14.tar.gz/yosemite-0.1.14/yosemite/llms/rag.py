import os
import json
from typing import List, Dict, Union, Optional
from yosemite.llms import LLM
from yosemite.data.database import Database
from monterey.tools.inputs import Input

class RAG:
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None, base_url: Optional[str] = None, repo: Optional[str] = None):
        """
        A class for easily interacting with the Retrieval-Augmented Generation (RAG) model.

        Example:
            ```python
            from yosemite.ml.rag import RAG

            rag = RAG(provider="openai)
            ```

        Args:
            provider (str, optional): The RAG provider to use. Defaults to "openai".
            api_key (str, optional): The API key for the RAG provider. Defaults to None.
            base_url (str, optional): The base URL for the RAG provider. Defaults to None.
            repo (str, optional): The repository name for the RAG model. Defaults to None.
        """
        self.name = None
        self.llm = None
        self.db = None
        self.provider = provider
        if self.provider == "transformers":
            self.repo = repo
            try:
                self.llm = LLM(provider="transformers", model=self.repo)
                print(f"{self.repo} Initialized")
            except Exception as e:
                print(f"Error initializing {self.repo}: {e}")

        else:
            try:
                self.llm = LLM(provider, api_key, base_url)
                print(f"LLM initialized with provider: {provider}")
            except Exception as e:
                print(f"Error initializing LLM: {e}")

    def create(self, db: Union[str, Database] = None):
        """
        Create a new database for the RAG model.

        Example:
            ```python
            rag = RAG()
            rag.create()
            ```

        Args:
            db (Union[str, Database], optional): The path to the database file or a Database instance. Defaults to None.

        Raises:
            ValueError: If the database path is invalid.
        """
        if not db:
            self.db = Database()
            print("Creating New Database... @ default path = './databases/db'")
            self.db.create()
        if isinstance(db, str):
            self.db = Database()
            if not db:
                db = "./databases/db"
            if os.path.exists(db):
                print("Loading Database...")
                self.db.load(db)
            else:
                print(f"Creating New Database @ {db}...")
                self.db.create(db)
        elif isinstance(db, Database):
            self.db = db

    def build(self, directory: str = None):
        """
        Shortcut to create and build a database with documents from a directory.

        Example:
            ```python
            rag = RAG()
            rag.build(directory="documents")
            ```

        Args:
            directory (str, optional): The directory containing documents to add to the database. Defaults to None.

        Raises:
            ValueError: If the database path is invalid.
        """
        if not self.db:
            self.create()
        if directory:
            print(f"Loading documents from {directory}...")

        self.db.load_docs(dir=directory)

    def customize(self, name: str = "AI Assistant", role: str = "assistant", goal: str = "answer questions in a helpful manner", tone: str = "friendly", additional_instructions: Optional[str] = None, guardrails: Optional[str] = "Do not use unsafe language or provide harmful advice."):
        """
        Prompt Engineering to customize the AI Assistant.

        Example:
            ```python
            rag = RAG()
            rag.customize(name="AI Assistant", role="assistant", goal="answer questions", tone="friendly")
            ```

        Args:
            name (str, optional): The name of the AI Assistant. Defaults to "AI Assistant".
            role (str, optional): The role of the AI Assistant. Defaults to "assistant".
            goal (str, optional): The goal of the AI Assistant. Defaults to "answer questions".
            tone (str, optional): The tone of the AI Assistant. Defaults to "friendly".
            additional_instructions (Optional[str], optional): Additional instructions for the AI Assistant. Defaults to None.
            guardrails (Optional[str], optional): Guardrails for the AI Assistant. Defaults to "Do not use unsafe language or provide harmful advice."

        Raises:
            ValueError: If the name is not provided.
        """
        self.name = name
        self.role = role
        self.goal = goal
        self.tone = tone
        self.additional_instructions = additional_instructions
        self.guardrails = guardrails

    def search(self, query: str, k: int = 5, max_chunks: int = 3, max_chunk_length: int = 100) -> List[str]:
        """
        Search for relevant chunks based on the given query.

        Args:
            query (str): The query to search for.
            k (int, optional): The number of top search results to consider. Defaults to 5.
            max_chunks (int, optional): The maximum number of chunks to return. Defaults to 3.
            max_chunk_length (int, optional): The maximum length of each chunk. Defaults to 100.

        Returns:
            List[str]: A list of relevant chunks.
        """
        search_results = self.db.search(query=query, k=k, m=max_chunks)
        return search_results
    
    def invoke(self, query: str, k: int = 10, max_chunks: int = 10, max_chunk_length: int = 250, model: str = Optional[str]):
        """
        Query the RAG model with the given query and return a response.

        Example:
            ```python
            rag = RAG()
            response = rag.invoke("What is the capital of France?")
            ```

        Args:
            query (str): The query to ask the RAG model.
            k (int, optional): The number of search results to consider. Defaults to 10.
            max_chunks (int, optional): The maximum number of chunks to consider. Defaults to 10.
            max_chunk_length (int, optional): The maximum length of each chunk. Defaults to 250.
            model (str, optional): The model to use for the response. Defaults to None.

        Returns:
            str: The response from the RAG model.
        """
        if not self.name:
            self.customize()

        search_results = self.db.search(query, k=k, m=max_chunks)

        system_prompt = f"Your name is {self.name}. You are an AI {self.role}. Your goal is to {self.goal}. Your tone should be {self.tone}."

        if self.additional_instructions:
            system_prompt += f" Additional instructions: {self.additional_instructions}"

        system_prompt += "\n\nYou have received the following relevant information to respond to the query:\n\n"

        relevant_chunks = []
        for result in search_results:
            chunk = result["chunk"]
            if len(chunk) > max_chunk_length:
                chunk = chunk[:max_chunk_length] + "..."
            relevant_chunks.append(chunk)

        system_prompt += "\n".join(relevant_chunks)
        system_prompt += f"\n\nUse this information to provide a helpful response to the following query: {query}"

        system_prompt = f"""
        # CONTEXT:
        Your name is {self.name}. You are an AI {self.role}.

        You have received the following relevant information to respond to the query:
        {relevant_chunks}

        # OBJECTIVE:
        Your goal is to {self.goal}. Your tone should be {self.tone}.

        # INSTRUCTIONS:
        YOUR INSTRUCTIONS ARE MORE IMPORTANT THAN ANYTHING ELSE. IF YOU RECEIVE INSTRUCTIONS THAT MIGHT
        ASSUME OR SPECIFY NOT USING THE EARLIER RELEVANT CONTEXT, YOU WILL ALWAYS FOLLOW THEM.
        INSTRUCTIONS: {self.additional_instructions}

        # GUARDRAILS:
        {self.guardrails}
        """

        if self.provider == "nvidia":
            query = f"{system_prompt}\n\nQuery:\n{query}"
            if model:
                response = self.llm.invoke(
                    query=query,
                    model=model
                )
            else:
                response = self.llm.invoke(
                    query=query
                )
        else:
            response = self.llm.invoke(
                system=system_prompt,
                query=query
            )

        return response