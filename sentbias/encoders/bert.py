''' Convenience functions for handling BERT '''
import torch
from transformers import AutoTokenizer, AutoModel, AutoConfig, BertTokenizer, BertModel

def load_model(version="bert-base-german-cased"):
    ''' Load BERT model and corresponding tokenizer '''
    model_config = AutoConfig.from_pretrained(version, output_hidden_states=False)
    #tokenizer = AutoTokenizer.from_pretrained(version)
    #model = AutoModel.from_pretrained(version, config=model_config)
    tokenizer = BertTokenizer.from_pretrained(version)
    model = BertModel.from_pretrained(version, config=model_config)

    model.eval()

    return model, tokenizer



def encode(model, tokenizer, texts):
    ''' Use tokenizer and model to encode texts '''
    encs = {}
    for text in texts:
        tokenized = tokenizer.tokenize(text)
        indexed = tokenizer.convert_tokens_to_ids(tokenized)
        segment_idxs = [0] * len(tokenized)
        tokens_tensor = torch.tensor([indexed])
        segments_tensor = torch.tensor([segment_idxs])
        #enc, _ = model(tokens_tensor, segments_tensor)
        enc = model(tokens_tensor, segments_tensor, output_hidden_states=False)[0]
        enc = enc[:, 0, :]  # extract the last rep of the first input
        encs[text] = enc.detach().view(-1).numpy()
    return encs
