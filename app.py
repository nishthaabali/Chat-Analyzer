import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    user_list = df['user'].unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show Analysis by Users",user_list)

    if st.sidebar.button("Analyze"):
        st.title("Statistics")
        col1, col2, col3, col4 = st.columns(4)

        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)

        with col1:
            st.header("Messages:")
            st.title(num_messages)
        with col2:
            st.header("Words:")
            st.title(words)
        with col3:
            st.header("Media:")
            st.title(num_media)
        with col4:
            st.header("Links:")
            st.title(num_links)


        #finding the busiest users in group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #activity
        st.title('Activity Chart')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Busy Days: ")
            busy_day = helper.activity(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Busy months: ")
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.pie(busy_month.values, labels=busy_month.index, autopct="%1.1f",startangle=90)
            ax.axis('equal')
            st.pyplot(fig)



        st.title('Distribution: ')
        col1, col2 = st.columns(2)

        with col1:

            #daily timeline
            st.header("Daily Timeline: ")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['date1'], daily_timeline['message'], color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        with col2:

            #mon Timeline
            st.header("Monthly Timeline: ")
            timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color = 'green')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        #daily timeline
        st.title("Hourly Activity:")
        hour_heatmap = helper.hour_activity(selected_user, df)
        fig,ax = plt.subplots(figsize=(8, 6))
        ax = sns.heatmap(hour_heatmap)
        st.pyplot(fig)



        #wordcloud
        st.title("WordCloud: ")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation = 'vertical')

        st.title('Most Common Words: ')
        st.pyplot(fig)

        st.dataframe(most_common_df)


        #emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(),autopct = "%0.2f")
            st.pyplot(fig)