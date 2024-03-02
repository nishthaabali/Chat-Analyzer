from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

     #num of messages
    num_messages = df.shape[0]

     #num of words
    words = []
    for i in df["message"]:
        words.extend(i.split())

    #num of media messages
    num_media = df[df['message'] == "<Media omitted>\n"].shape[0]



    #fetch num of links shared
    links = []
    for i in df['message']:
        links.extend(extract.find_urls(i))


    return num_messages, len(words), num_media, len(links)


def most_busy_user(df):
     x= df['user'].value_counts().head()
     df= round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
         columns={'index': 'name', 'user': 'percent'})
     return x,df


def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=20, background_color='beige')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('hinglish_list.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for i in temp["message"]:
        for word in i.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df['Unicode'] = emoji_df[0].apply(lambda x: x.encode('unicode-escape').decode('utf-8'))

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('date1').count()['message'].reset_index()

    return daily_timeline

def activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def hour_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    hour_heatmap = df.pivot_table(index = 'day_name', columns= 'period', values = 'message', aggfunc= 'count').fillna(0)

    return hour_heatmap

