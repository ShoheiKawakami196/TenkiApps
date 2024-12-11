import os
from openai import OpenAI
import streamlit as st

# 環境変数からAPIキーを取得
api_key=os.getenv("OPENAI_API_KEY")

client = OpenAI()

# GPTリクエスト関数
def run_gpt(content_text_to_gpt, content_kind_of_to_gpt, content_maxStr_to_gpt):
    # リクエスト内容を組み立て
    request_to_gpt = (
        content_text_to_gpt
        + " また、これを記事として読めるように、記事のタイトル、目次、内容の順番で出力してください。"
        + content_maxStr_to_gpt
        + "文字以内で出力してください。"
        + "また、文章は"
        + content_kind_of_to_gpt
        + "にしてください。"
    )

    # GPTにリクエストを送信
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたはアントニオ猪木です。"},
                {"role": "user", "content": request_to_gpt},
            ],
        )
        # レスポンスの取り出し
        output_content = response["choices"][0]["message"]["content"].strip()
        return output_content

    except Exception as e:
        return f"エラーが発生しました: {e}"

# Streamlitフロントエンド
st.title("GPTに記事を書かせるアプリ")

# ユーザー入力
content_text_to_gpt = st.text_input("書かせたい内容を入力してください", "ワンピースについて教えてください！")
content_kind_of_to_gpt = st.selectbox(
    "文章のテイストを選んでください", ["中立的で客観的な文章", "熱血的な文章", "コミカルな文章"]
)
content_maxStr_to_gpt = st.text_input("出力文字数", "500")

# 実行ボタン
if st.button("実行"):
    output_content_text = run_gpt(content_text_to_gpt, content_kind_of_to_gpt, content_maxStr_to_gpt)
    st.markdown("### 出力結果")
    st.write(output_content_text)