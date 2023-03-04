from youtube_search import YoutubeSearch
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import AutoTokenizer, BertLMHeadModel
import torch

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = BertLMHeadModel.from_pretrained("bert-base-uncased", output_hidden_states = True)
model.eval()

search_term = "women in tech"
print("searching for: ",search_term)
search_results = YoutubeSearch(search_term, max_results=5).to_dict()

# get transcriptions for videos below a certain duration
results = {}
for item in search_results:
    if int(item['duration'].split(":")[0]) < 4:

        print("found: ",item['title'])
        id = item['url_suffix'].split("=")[1]

        srt = YouTubeTranscriptApi.get_transcript(id)
        text = []

        for value in srt:
            text.append(value['text'])

        text = ' '.join(text)
        
        print(text)

        results[item['title']] = {'id':id, 'transcript':text}

# embed each transcription
for item in results.values():
    transcript = item['transcript']

    marked_text = "[CLS] " + transcript + " [SEP]"

    tokenized_text = tokenizer.tokenize(marked_text)
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    segments_ids = [1] * len(tokenized_text)

    # Convert inputs to PyTorch tensors
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segments_ids])

    # Run the text through BERT, and collect all of the hidden states produced
    # from all 12 layers. 
    with torch.no_grad():

        print(len(tokens_tensor[0]))
        print(len(segments_tensors[0]))

        outputs = model(tokens_tensor, segments_tensors)
        hidden_states = outputs[2]

    token_embeddings = torch.stack(hidden_states, dim=0)
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    token_embeddings = token_embeddings.permute(1,0,2)
    
    token_vecs = hidden_states[-2][0]
    # Calculate the average of all 22 token vectors.
    sentence_embedding = torch.mean(token_vecs, dim=0)

    print(sentence_embedding)