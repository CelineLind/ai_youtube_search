from youtube_search import YoutubeSearch
from youtube_transcript_api import YouTubeTranscriptApi

search_term = "women in tech"
print("searching for: ",search_term)
search_results = YoutubeSearch(search_term, max_results=5).to_dict()

# get transcriptions for videos below a certain duration
results = {}
for item in search_results:
    if int(item['duration'].split(":")[0]) < 3:

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
