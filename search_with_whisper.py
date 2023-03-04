from youtube_search import YoutubeSearch
from transformers import pipeline
from pytube import YouTube

print("importing pipeline...")
whisper = pipeline('automatic-speech-recognition', model="openai/whisper-base.en")

search_term = "women in tech"
print("searching for: ",search_term)
search_results = YoutubeSearch(search_term, max_results=5).to_dict()

# get transcriptions for videos below a certain duration
results = {}
for item in search_results:
    if int(item['duration'].split(":")[0]) < 3: # video less than 5 minutes long

        print("found: ",item['title'])

        url = 'https://www.youtube.com'+item['url_suffix']
        yt = YouTube(url)

        streams = yt.streams.filter(only_audio=True)
        stream = streams.first()

        print("downloading video...")
        file_name = str(yt.title).replace(' ','')
        video_filepath = "temp_videos/"+file_name+".mp3"
        stream.download(filename=video_filepath)
        
        print("sending data to model...")
        text = whisper(video_filepath)

        print(text)
        results[item['title']] = {'url':url, 'filepath':video_filepath, 'transcript':text}

# embed each transcription
