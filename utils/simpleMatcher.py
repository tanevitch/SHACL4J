import spacy
from spacy.matcher import Matcher

NLP = spacy.load("es_dep_news_trf")
class SimpleMatcher:
    matcher = Matcher(NLP.vocab)
    
    def add_pattern(self, pattern_name: str, expression: list):
        self.matcher.add(pattern_name, expression)

    def remove_pattern(self,pattern_name:str):
        self.matcher.remove(pattern_name)

    def get_matches(self, sentence: str):
        processed_sentence = NLP(sentence)
        # for token in processed_sentence:
        #     print(token.text, token.pos_, token.dep_)
        matches = {}
        
        for match_id, start, end in self.matcher(processed_sentence):
            string_id = NLP.vocab.strings[match_id]  
            span = processed_sentence[start:end]  
            if not string_id in matches.keys():
                matches[string_id] = [span.text]  
            else:
                matches[string_id].append(span.text)

        return matches