from yosemite.nlp.chunker import Chunker
from yosemite.nlp.sentences import Transformer, CrossEncoder, Loss, SemanticSearch, SentenceSimilarity

#==============================================================================

class NaturalLanguage:
    def __init__(self):
        self.chunker = Chunker
        self.transformer = Transformer
        self.cross_encoder = CrossEncoder
        self.loss = Loss
        self.semantic_search = SemanticSearch
        self.sentence_similarity = SentenceSimilarity

#==============================================================================