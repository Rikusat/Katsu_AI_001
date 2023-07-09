import streamlit as st
import pandas as pd
import requests
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# Page setup
st.set_page_config(page_title="関東圏：補助金検索くん", page_icon="🎈", layout="wide")
st.title("関東圏：補助金検索くん🎈")

# Define CSS styles
st.markdown(
    """
    <style>
    body {
        background-color: #f8f8f8;
    }

    .highlight {
        color: #e4572e;
        font-weight: bold;
    }

    .card {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 20px;
        background-color: #ffffff;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.3s;
    }

    .card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom CSS classes
highlight_class = "highlight"
card_class = "card"



# Correct the formation of the URL
sheet_id = "1PmOf1bjCpLGm7DiF7dJsuKBne2XWkmHyo20BS4xgizw"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# Function to filter data based on selected 地域 and selected_options
def filter_data(selected_地域, selected_options):
    df = pd.read_csv(url, dtype=str).fillna("")
    df_filtered = df[(df["地域"] == selected_地域) & (df["対象事業者"].str.contains("|".join(selected_options)))]
    return df_filtered

# Get a list of unique 地域
df = pd.read_csv(url, dtype=str).fillna("")
unique_地域 = df["地域"].unique()

# Create a selectbox for 地域
selected_地域 = st.selectbox('地域を選択', unique_地域, index=0)

# 対象事業者の各文字列を取得して一意の値を生成
filter_options = set()
for item in df[df["地域"] == selected_地域]["対象事業者"]:
    options = item.split("／")
    filter_options.update(options)

st.markdown("---")

# Show the options as a selectbox
selected_options = st.multiselect("当てはまる項目を選択 : 複数可", list(filter_options))

st.markdown("---")

# フィルタリング
df_search = filter_data(selected_地域, selected_options)

# Prepare the initial question
info_to_ask = f"地域:{selected_地域} 対象事業者:{', '.join(selected_options)} "

# Get user's input
user_input = st.text_input("補足情報を自由に入力してください", value=info_to_ask)

if st.button("AIに聞く"):
    # Check if the dataframe is empty
    if df_search.empty:
        st.write("No matching data found.")
    else:
        # If not, use the data to generate a message for GPT-3
        message = f"I found {len(df_search)} matches for the 地域 '{user_input}'. Here's the first one: {df_search.iloc[0].to_dict()}"

        # Add user's input to the message
        message += f"\n{user_input}"

       # Use OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[
                {"role": "system", "content": "与えられた情報を元に該当するデータを10個ほど箇条書きで書き出してください"},
                {"role": "user", "content": message}
            ]
        )
        # Show OpenAI's response
        st.write(response['choices'][0]['message']['content'])

st.markdown("---")
        
# Show the cards
N_cards_per_row = 3
cols = st.columns(N_cards_per_row, gap="large")
for n_row, row in df_search.iterrows():
    i = n_row % N_cards_per_row
    if i == 0:
        st.markdown("---")
    # Draw the card
    with cols[i]:
        # Apply CSS class to highlight important information
        st.markdown(f"<h3 class='{highlight_class}'>{row['補助金名'].strip()}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p class='{highlight_class}'>{row['詳細'].strip()}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='{highlight_class}'>{row['上限金額・助成額'].strip()}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='{highlight_class}'>{row['申請期間'].strip()}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='{highlight_class}'>地域: {row['地域'].strip()}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='{highlight_class}'>実施機関: {row['実施機関'].strip()}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='{highlight_class}'>対象事業者: {row['対象事業者'].strip()}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='{highlight_class}'>公式公募ページ: <a href='{row['公式公募ページ'].strip()}' target='_blank'>{row['公式公募ページ'].strip()}</a></p>", unsafe_allow_html=True)
        st.markdown(f"<p><a href='{row['掲載元'].strip()}' target='_blank'>掲載元</a></p>", unsafe_allow_html=True)
        # Apply CSS class to the entire card
        st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
        st.markdown("---")
