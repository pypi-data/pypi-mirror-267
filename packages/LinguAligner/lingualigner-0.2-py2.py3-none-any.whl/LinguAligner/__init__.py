"""An amazing sample package!dd"""

__version__ = "0.2"


from . import aligners
import spacy
from . import translation
from transformers import BertTokenizer, BertModel, logging
logging.set_verbosity_error()


class Pipeline:
    def __init__(self, config):
        self.config = config
        print("Loading spacy model: " + config["spacy_model"])
        self.nlp = spacy.load(config["spacy_model"])
        print("Model loaded")
        if "word_aligner" in config["pipeline"]:
            print("Loading WAligner model: " + config["WAligner_model"])
            self.tokenizer = BertTokenizer.from_pretrained(config["WAligner_model"])
            self.model = BertModel.from_pretrained(config["WAligner_model"])
            print("Model loaded")

    def align_annotation(self, src_sent,src_ann, tgt_sent, trans_ann, lookupTable=None):
        pipeline = self.config["pipeline"]
        nlp = self.nlp
        res = aligners.regex_string_match(tgt_sent,trans_ann) 
        if not res:
            
            for method in pipeline:
                print(res, method)
                if not res and method == 'lemma':
                    res = aligners.lemma_match(tgt_sent,trans_ann,nlp)
                elif not res and method == 'external_resource' and lookupTable: # Mtrans is combined with lemma method since we also calculate the lemma of the translations
                    res = aligners.resource_match(tgt_sent,src_ann,nlp,lookupTable)
                elif not res and method == 'word_aligner':
                    res = aligners.wordAligner(src_sent,tgt_sent,src_ann,nlp, self.tokenizer, self.model)
                elif not res and method == 'gestalt':
                    res = aligners.gestalt_match(src_ann,tgt_sent,nlp)
                elif not res and method == 'leveinstein':
                    res = aligners.leveinstein_match(src_ann,tgt_sent,nlp)
                else:
                    print(f"Invalid alignment method: {method}")
        return res
    


#res = align_annotation("The ship land on the shore","O barco desembarcou na costa","land","terra",nlp) # Expected output: "teste
#print(res)
