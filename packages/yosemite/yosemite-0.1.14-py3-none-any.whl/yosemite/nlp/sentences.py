from typing import List, Tuple, Optional, Union
from sentence_transformers import losses, util, CrossEncoder as CrossEncoderModel
from sentence_transformers import SentenceTransformer
from monterey.tools.logger import Logger
from monterey.tools.progress_bar import ProgressBar as RichProgress
from monterey.tools.text import Text as RichText
import torch

class Transformer:
    """
    A robust class for generating SentenceTransformer embeddings.

    Example:
        ```python 
        sentences = [
            "The cat is sitting on the mat.",
            "The dog is playing in the park.",
            "Paris is the capital of France.",
        ]

        embedder = Transformer()
        embeddings = embedder.encode(sentences)
        ```  
    """
    def __init__(self, model_name : str = "paraphrase-MiniLM-L6-v2", verbose: bool = False, logger_name: str = "SentenceTransformer", dimensions: int = 384):
        self.model = SentenceTransformer(model_name, device="cuda" if torch.cuda.is_available() else "cpu")
        self.inputs = []
        self.verbose = verbose
        if logger_name is None:
            logger_name = "SentenceTransformer"
        self.logger_name = logger_name
        self.logger = None
        self.dimensions = dimensions

        if self.verbose:
            self.logger = Logger(self.logger_name, verbose=True)
        else:
            self.logger = Logger(self.logger_name, verbose=False)

    def encode(self, input: Union[str, List[str]], batch_size: Optional[int] = None):
        embeddings = []
        if not isinstance(input, (str, list)):
            self.logger.error("Input must be a string or list of strings.")
            return None
        else:
            self.logger.status(f"""GENERATING EMBEDDINGS""")
            if batch_size is None:
                batch_size = min(len(input), 64) if isinstance(input, list) else 1
            self.inputs = input
            if isinstance(input, str):
                self.inputs = [input]
            with RichProgress(total=len(self.inputs)) as progress:
                for i in range(0, len(self.inputs), batch_size):
                    batch = self.inputs[i:i+batch_size]
                    batch_embeddings = self.model.encode(batch, convert_to_numpy=True)
                    embeddings.extend(batch_embeddings)
                    progress.update(len(batch))
            self.total_inputs = len(self.inputs)
            self.total_inputs_message = f"Total Inputs: [bold] {self.total_inputs} [/bold]"
            self.total_embeddings_generated = len(embeddings)
            self.total_embeddings_message = f"Total Embeddings Generated: [bold] {self.total_embeddings_generated} [/bold]"
            self.batch_size = batch_size
            self.batch_size_message = f"Batch Size: [bold] {self.batch_size} [/bold]"
            self.total_batches = len(embeddings) // batch_size
            self.total_batches_message = f"Total Batches: [bold] {self.total_batches} [/bold]"
            self.messages = [self.total_inputs_message, self.total_embeddings_message, self.batch_size_message, self.total_batches_message]
            if self.verbose:
                self.text = RichText()
                self.text.say("Embeddings generated successfully.", style="bold green", use_box=True)
                self.text.list(self.messages, style="white", use_box=True)
            return embeddings

class CrossEncoder:
    """
    Initializes the CrossEncoder with a specified model. Default model is "cross-encoder/ms-marco-MiniLM-L-12-v2".

    Example:
    ```python
    sentences = [
        "The cat is sitting on the mat.",
        "The dog is playing in the park.",
        "Paris is the capital of France.",
        "London is the capital of England.",
        "A feline is resting on the rug.",
    ]
    cross_encode = CrossEncoder()
    query = "What is the capital of France?"
    ranked_sentences = cross_encode.rank(query, sentences)
    ```

    ```bash
    CrossEncoder results:
    Paris is the capital of France. (Score: 0.99)
    London is the capital of England. (Score: 0.98)
    The cat is sitting on the mat. (Score: 0.97)
    The dog is playing in the park. (Score: 0.96)
    A feline is resting on the rug. (Score: 0.95)
    ```

    Args:
        model_name : str, optional
            The name of the CrossEncoder model to use (default is "cross-encoder/ms-marco-MiniLM-L-12-v2")
        max_length : int, optional
            The maximum length of the input sequences (default is None)
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-12-v2", max_length: int = None):
        self.model = CrossEncoderModel(model_name, max_length=max_length)

    def rank(self, query: str, sentences: List[str]) -> List[Tuple[str, float]]:
        """
        Re-ranks sentences based on their relevance to a single query using the CrossEncoder model.

        Example:
        ```python
        from sentence_transformers import CrossEncoder
        CrossEncoder.rank("What is the capital of France?", ["Paris is the capital of France.", "London is the capital of England."])
        ```

        Args:
            query : str
                The query to use for re-ranking
            sentences : List[str]
                The list of sentences to be ranked

        Returns:
            List[Tuple[str, float]]
                A list of ranked sentences with their scores
        """
        if not sentences:
            return []

        scores = self.model.predict([(query, sentence) for sentence in sentences])
        ranked_sentences = [(sentence, score) for sentence, score in sorted(zip(sentences, scores), key=lambda x: x[1], reverse=True)]
        return ranked_sentences
    
class Loss:
    """
    Initializes the Loss object with a specified loss type, data format, and model.

    Example:
        ```python
        loss = Loss(loss_type="BatchAllTripletLoss", data_format="single_sentences")
        print(f"Initialized loss: {loss.loss}")
        ```

    Args:
        loss_type : str
            The type of loss function to use
        data_format : str
            The format of the input data (single_sentences, sentence_pairs, or triplets)
        model_name : str, optional
            The name of the SentenceTransformer model to use (default is "all-MiniLM-L6-v2")
    """
    def __init__(self, loss_type: str, data_format: str, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.loss = self._initialize_loss(loss_type, data_format)

    def _initialize_loss(self, loss_type: str, data_format: str):
        if data_format == "single_sentences":
            return self._init_single_sentence_loss(loss_type)
        elif data_format == "sentence_pairs":
            return self._init_sentence_pair_loss(loss_type)
        elif data_format == "triplets":
            return self._init_triplet_loss(loss_type)
        else:
            raise ValueError("Unsupported data format")

    def _init_single_sentence_loss(self, loss_type: str):
        if loss_type == "BatchAllTripletLoss":
            return losses.BatchAllTripletLoss(model=self.model)
        elif loss_type == "BatchHardTripletLoss":
            return losses.BatchHardTripletLoss(model=self.model)
        elif loss_type == "BatchSemiHardTripletLoss":
            return losses.BatchSemiHardTripletLoss(model=self.model)
        else:
            raise ValueError("Unsupported loss type for single sentences")

    def _init_sentence_pair_loss(self, loss_type: str):
        if loss_type == "SoftmaxLoss":
            return losses.SoftmaxLoss(model=self.model)
        elif loss_type == "ContrastiveLoss":
            return losses.ContrastiveLoss(model=self.model)
        else:
            raise ValueError("Unsupported loss type for sentence pairs")

    def _init_triplet_loss(self, loss_type: str):
        if loss_type == "TripletLoss":
            return losses.TripletLoss(model=self.model)
        elif loss_type == "MultipleNegativesRankingLoss":
            return losses.MultipleNegativesRankingLoss(model=self.model)
        else:
            raise ValueError("Unsupported loss type for triplets")
        
class SemanticSearch:
    """
    Constructs all the necessary Args for the SemanticSearch object.

    Example:
        ```python
        semantic_search = SemanticSearch()
        corpus_embeddings = semantic_search.encode_corpus(sentences1 + sentences2)
        results = semantic_search.search(query, corpus_embeddings, sentences1 + sentences2)
        ```

    Args:
        model_name : str, optional
            The name of the SentenceTransformer model to use (default is "all-MiniLM-L6-v2")
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode_corpus(self, corpus: List[str]) -> torch.Tensor:
        """
        Encodes a list of sentences into embeddings.

        Example:
            ```python
            corpus = ["The cat is sitting on the mat.", "The dog is playing in the park.", "Paris is the capital of France."]
            semantic_search = SemanticSearch()
            corpus_embeddings = semantic_search.encode_corpus(corpus)
            ```

        Args:
            corpus : List[str]
                The list of sentences to encode

        Returns:
            torch.Tensor
                A tensor containing the embeddings of the sentences
        """
        return self.model.encode(corpus, convert_to_tensor=True)

    def search(self, query: str, corpus_embeddings: torch.Tensor, corpus: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Performs semantic search on a list of sentences.

        Example:
            ```python
            query = "What is the capital of France?"
            semantic_search = SemanticSearch()
            corpus_embeddings = semantic_search.encode_corpus(sentences1 + sentences2)
            results = semantic_search.search(query, corpus_embeddings, sentences1 + sentences2)
            ```

        Args:
            query : str
                The query sentence
            corpus_embeddings : torch.Tensor
                The embeddings of the corpus sentences
            corpus : List[str]
                The list of sentences to search
            top_k : int, optional
                The number of results to return (default is 5)

        Returns:
            List[Tuple[str, float]]
                A list of tuples, each containing a sentence from the corpus and its similarity score to the query
        """
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
        
        # Check if top_k is within the valid range
        top_k = min(top_k, len(corpus))
        
        top_results = torch.topk(cos_scores, k=top_k)
        return [(corpus[idx], score.item()) for score, idx in zip(top_results[0], top_results[1])]
    
class SentenceSimilarity:
    """
    Constructs all the necessary Args for the SentenceSimilarity object.

    Example:
        ```python
        sentence_similarity = SentenceSimilarity()
        similarities = sentence_similarity.compute_similarity(sentences1, sentences2)
        ```

    Args:
        model_name : str, optional
            The name of the SentenceTransformer model to use (default is "all-MiniLM-L6-v2")
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def compute_similarity(self, sentences1: List[str], sentences2: List[str]) -> List[Tuple[str, str, float]]:
        """
        Computes the cosine similarity between two lists of sentences.

        Example:
            ```python
            sentences1 = ["The cat is sitting on the mat.", "The dog is playing in the park.", "Paris is the capital of France."]
            sentences2 = ["A feline is resting on the rug.", "A canine is running in the garden.", "London is the capital of England."]
            sentence_similarity = SentenceSimilarity()
            similarities = sentence_similarity.compute_similarity(sentences1, sentences2)
            ```

        Args:
            sentences1 : List[str]
                The first list of sentences
            sentences2 : List[str]
                The second list of sentences

        Returns:
            List[Tuple[str, str, float]]
                A list of tuples, each containing a pair of sentences and their cosine similarity
        """
        embeddings1 = self.model.encode(sentences1, convert_to_tensor=True)
        embeddings2 = self.model.encode(sentences2, convert_to_tensor=True)
        cosine_scores = util.cos_sim(embeddings1, embeddings2)
        return [(sentences1[i], sentences2[j], cosine_scores[i][j].item()) for i in range(len(sentences1)) for j in range(len(sentences2))]

if __name__ == "__main__":
    sentences1 = [
        "The cat is sitting on the mat.",
        "The dog is playing in the park.",
        "Paris is the capital of France.",
    ]
    sentences2 = [
        "A feline is resting on the rug.",
        "A canine is running in the garden.",
        "London is the capital of England.",
    ]

    # CrossEncode example
    cross_encode = CrossEncoder()
    query = "What is the capital of France?"
    ranked_sentences = cross_encode.rank(query, sentences1, sentences2)
    print("CrossEncode results:")
    for sentence, score in ranked_sentences:
        print(f"{sentence} (Score: {score:.2f})")
    print()

    # Loss example
    loss = Loss(loss_type="BatchAllTripletLoss", data_format="single_sentences")
    print(f"Initialized loss: {loss.loss}")
    print()

    # SemanticSearch example
    semantic_search = SemanticSearch()
    corpus_embeddings = semantic_search.encode_corpus(sentences1 + sentences2)
    results = semantic_search.search(query, corpus_embeddings, sentences1 + sentences2)
    print("SemanticSearch results:")
    for sentence, score in results:
        print(f"{sentence} (Score: {score:.2f})")
    print()

    # SentenceSimilarity example
    sentence_similarity = SentenceSimilarity()
    similarities = sentence_similarity.compute_similarity(sentences1, sentences2)
    print("SentenceSimilarity results:")
    for sentence1, sentence2, score in similarities:
        print(f"{sentence1} - {sentence2} (Similarity: {score:.2f})")
    print()

    # Embedder example
    embedder = SentenceTransformer()
    embeddings = embedder.embed(sentences1 + sentences2)
    print("Embedder results:")
    for sentence, embedding in embeddings:
        print(f"{sentence} (Embedding length: {len(embedding)})")