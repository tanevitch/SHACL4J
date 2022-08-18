import spacy

from utils.simpleMatcher import SimpleMatcher

NLP = spacy.load("es_dep_news_trf")
MATCHER= SimpleMatcher()

class Cleaner:
    def has_verb(self, sentence):
        MATCHER.add_pattern("verb", [
                            [
                                {
                                    "POS": "VERB",
                                }
                            ]
                        ])
        if MATCHER.get_matches(str(sentence))== {}:
            return False
        return True

    def clean_requirement(self, requirement):
        for key in requirement:
            if (type(requirement[key])== str):
                requirement[key]= requirement[key].strip().lower()
        return requirement

    def clean_stakeholder(self, stakeholder: str):
        MATCHER.add_pattern("noun_subj", [
                            [
                                {
                                    "POS": "NOUN",
                                    "DEP": "ROOT"
                                }
                            ]
                        ])

        if MATCHER.get_matches(str(stakeholder)) == {}:
            return None
        return stakeholder

    def clean_requirements(self, requirements):
        clean_requirements= []
        for requirement in requirements:
            requirement["Como"]= self.clean_stakeholder(requirement["Como"])
            if (self.has_verb(requirement["Quiero"])): #si no tiene un verbo es porque está mal escrito
                clean_requirements.append(self.clean_requirement(requirement))
        
        return clean_requirements 