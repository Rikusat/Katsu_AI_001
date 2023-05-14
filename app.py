
import streamlit as st
import openai

# スタイルをカスタマイズするCSSを定義
custom_css = """
body {
    background-color: #f7f7f7; /* 背景色を設定 */
}

h1 {
    color: #ff9900; /* 見出しのテキスト色を設定 */
}

p {
    color: #333333; /* 本文のテキスト色を設定 */
}
"""

# スタイルを適用する
st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)



# ユーザーインターフェースの構築
st.title("AI司法書士くん")
st.write("勝司法書士法人の任意後見チャットです")
st.header("Header Section")
st.subheader("Subheader Section")
st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus quis ultrices velit, at lobortis ligula. Nullam nec sem lacinia, sagittis odio eu, tempor elit. Suspendisse finibus mi at enim vehicula, nec viverra sem pulvinar. Cras id eros id nulla rutrum tincidunt. Sed aliquam, lacus at efficitur ultricies, metus sapien vulputate erat, non semper quam tellus sed augue. Suspendisse finibus tellus at neque eleifend, eu tempus nisi semper. Mauris id lacinia sapien, non varius elit.")



# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去
    

# 動的なエフェクトを追加するHTML要素
st.markdown("""
    <style>
    @keyframes robot {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }
    </style>
    <div style="display: flex; justify-content: center;">
        <div style="font-size: 40px; animation: robot 2s infinite; padding-right: 10px;">🤖</div>
        <div style="font-size: 30px;">AIアシスタントがお答えします！</div>
    </div>
""", unsafe_allow_html=True)


user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker = "🤖カツ！"  # AIが使う語尾の指示プロンプト

        st.write(speaker + ": " + message["content"])
