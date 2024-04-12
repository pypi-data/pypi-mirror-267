from typing import Optional, List, Union
from yosemite.llms.llm import LLM
from yosemite.llms.rag import RAG
from yosemite.llms.instruct import Instruct

class MixtureOfExperts:
    def __init__(self, provider: Optional[str] = "openai", api_key: Optional[str] = None, model: Optional[str] = None):
        """
        A module for using the Mixtures of Experts (MoE) approach to combine responses from multiple language models.

        Example:
            ```python
            from yosemite.llms import LLM, RAG, Instruct, MixtureOfExperts

            llm = LLM(provider="openai")
            rag = RAG(provider="openai")
            instruct = Instruct(api_key="your_api_key")
            moe = MixtureOfExperts()
            moe.create([llm, rag, instruct])

            response = moe.invoke(query="What is the capital of France?")
            print(response)
            ```

        Attributes:
            provider (str): The provider of the language models.
            api_key (str): The API key for the language models.
            model_name_or_path (str): The model name or path for the language models.
            llm (LLM): The LLM instance for generating responses.
            experts (List[Union[LLM, RAG, Instruct]]): A list of language model instances to use as experts.

        Methods:
            create: Create a list of language model instances to use as experts.
            invoke: Invoke the mixture of experts approach to generate a response to a query.
        """
        self.provider = provider
        self.api_key = api_key
        self.model_name_or_path = model
        self.llm = None
        
        if not model and api_key:
            self.llm = LLM(provider=provider)
        elif model and api_key:
            self.llm = LLM(provider=provider, api_key=api_key, model=model)
        elif model and not api_key:
            self.llm = LLM(provider=provider, model=model)
        elif not model and not api_key:
            self.llm = LLM()
        else:
            self.llm = LLM()
        
        self.experts = []

    def create(self, experts: Union[LLM, RAG, Instruct, List[Union[LLM, RAG, Instruct]]]):
        """
        Create a list of language model instances to use as experts.

        Example:
            ```python
            llm = LLM(provider="openai")
            rag = RAG(provider="openai")
            instruct

        Args:
            experts (Union[LLM, RAG, Instruct, List[Union[LLM, RAG, Instruct]]]): An instance of an LLM, RAG, or Instruct model,
                or a list of those instances to use as experts.
            
        Raises:
            ValueError: If the input is not a valid language model instance or a list of language model instances.
        """
        if isinstance(experts, (LLM, RAG, Instruct)):
            self.experts = [experts]
        elif isinstance(experts, list) and all(isinstance(expert, (LLM, RAG, Instruct)) for expert in experts):
            self.experts = experts
        else:
            raise ValueError("Invalid input. Expected an instance of LLM, RAG, or Instruct, or a list of those instances.")

    def invoke(self, query: str, k: int = 10, max_chunks: int = 10, max_chunk_length: int = 250, model: Optional[str] = None):
        """
        Invoke the mixture of experts approach to generate a response to a query.

        Example:
            ```python
            response = moe.invoke(query="What is the capital of France?")
            ```

        Args:
            query (str): The query to ask the mixture of experts.
            k (int, optional): The number of search results to consider. Defaults to 10.
            max_chunks (int, optional): The maximum number of chunks to consider. Defaults to 10.
            max_chunk_length (int, optional): The maximum length of each chunk. Defaults to 250.
            model (str, optional): The model to use for the response. Defaults to None.

        Returns:
            str: The response from the mixture of experts.
        """
        expert_responses = []
        
        for expert in self.experts:
            if isinstance(expert, RAG):
                if model:
                    response = expert.invoke(query=query, model=model)
                else:
                    response = expert.invoke(query=query)
            elif isinstance(expert, Instruct):
                response = expert.instruct(query=query)
            else:  # LLM
                response = expert.invoke(query=query)
            
            expert_responses.append(str(response))

        system_prompt = f"""
        # CONTEXT
        Responses: {expert_responses}
        
        Using the knowledge provided by a few sources, as well as your own understanding and the relevant information,
        provide a comprehensive and insightful response to the query. Synthesize the information from all sources to
        generate a well-informed and helpful answer. Please make sure your response is clear, concise, and accurate.
        Your response should use natural, organic language any human can understand.

        # OBJECTIVE
        Do not explicitly mention your knowledge of the above information; simply use it as context for your response.

        # QUERY
        {query}
        """

        if self.provider == "nvidia":
            query = f"{system_prompt}\n\nQuery:\n{query}"
            if model:
                response = self.llm.invoke(query=query, model=self.model_name_or_path)
            else:
                response = self.llm.invoke(query=query, model="mistral")
        else:
            response = self.llm.invoke(system=system_prompt, query=query)

        return response