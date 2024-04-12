import os
import json
from typing import List, Dict, Union
from yosemite.llms.llm import LLM
from yosemite.llms.rag import RAG
from monterey.tools.text import Text
from monterey.tools.inputs import Input

class Chatbot:
    """
    A lightweight chatbot client for interacting with LLMs or RAG instances through a CLI interface.

    ```python
    from yosemite.llms.chatbot import Chatbot
    from yosemite.llms import LLM

    llm = LLM(provider="openai")
    chatbot = ChatServe(llm)
    chatbot.serve()
    ```

    Args:
        model (Union[LLM, RAG]): An instance of an LLM or RAG model to be used for generating responses.
        history_file (str, optional): The file path to store the chat history. Defaults to "chat_history.json".
        max_history (int, optional): The maximum number of messages to keep in the chat history. Defaults to 10.

    Methods:
        serve: Start the chatbot client and handle user interactions.
        load_history: Load the chat history from the specified file.
        save_history: Save the chat history to the specified file.
    """

    def __init__(self, model: Union[LLM, RAG], prompt: str = "Welcome to the Chatbot!", history_file: str = "chat_history.json", max_history: int = 10):
        self.text = Text()
        self.prompt = prompt
        self.model = model
        self.history_file = history_file
        self.max_history = max_history
        self.chat_history = self.load_history()

    def serve(self):
        """
        Start the chatbot client and handle user interactions.

        This method enters a loop where the user can input their messages, and the chatbot generates responses
        based on the provided LLM or RAG instance. The chat history is stored and updated throughout the conversation.
        The user can exit the chat by typing "/exit" or "/bye".
        """
        self.text.say(message=self.prompt, style="bold underline")
        print("Type '/exit' or '/bye' to end the conversation.\n")

        while True:
            user_input = Input.ask("User: ")

            if user_input.lower() in ["/exit", "/bye"]:
                self.text.say("Chatbot: Goodbye!", style="bold")
                break

            self.chat_history.append({"role": "user", "content": user_input})

            if isinstance(self.model, LLM):
                response = self.model.invoke(query=user_input)
            elif isinstance(self.model, RAG):
                response = self.model.invoke(query=user_input)
            else:
                raise ValueError("Invalid model type. Expected an instance of LLM or RAG.")

            self.chat_history.append({"role": "assistant", "content": response})
            print(f"Chatbot: {response}\n")

            if len(self.chat_history) > self.max_history:
                self.chat_history = self.chat_history[-self.max_history:]

            self.save_history()

    def load_history(self) -> List[Dict[str, str]]:
        """
        Load the chat history from the specified file.

        Returns:
            List[Dict[str, str]]: The loaded chat history, or an empty list if the file doesn't exist.
        """
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as file:
                return json.load(file)
        return []

    def save_history(self):
        """
        Save the chat history to the specified file.
        """
        with open(self.history_file, "w") as file:
            json.dump(self.chat_history, file, indent=2)

if __name__ == "__main__":
    llm = LLM(provider="openai")
    chatbot = Chatbot(llm)
    chatbot.serve() 