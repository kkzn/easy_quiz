import streamlit as st
import random

# クイズデータ
# 各要素は辞書で、'question' (問題文), 'options' (選択肢のリスト), 'correct_answer' (正解の選択肢) を含む
quizzes = [
    {
        "question": "空を飛ぶ鳥はどれ？",
        "options": ["ライオン", "ゾウ", "スズメ", "キリン"],
        "correct_answer": "スズメ"
    },
    {
        "question": "日本の首都はどこ？",
        "options": ["大阪", "東京", "名古屋", "福岡"],
        "correct_answer": "東京"
    },
    {
        "question": "1 + 1 は？",
        "options": ["1", "2", "3", "4"],
        "correct_answer": "2"
    }
]

# Streamlitのセッションステートを初期化
# アプリの状態（現在の問題番号、スコア、回答済みかなど）を保持するために使用
if 'current_quiz_index' not in st.session_state:
    st.session_state.current_quiz_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answer_submitted' not in st.session_state:
    st.session_state.answer_submitted = False
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = None

st.title('かんたんクイズアプリ')

# 現在の問題を取得
if st.session_state.current_quiz_index < len(quizzes):
    current_quiz = quizzes[st.session_state.current_quiz_index]

    # 問題を表示
    st.header(f"問題 {st.session_state.current_quiz_index + 1}")
    st.write(current_quiz["question"])

    # 選択肢を表示（ラジオボタン）
    # 回答済みの場合、ラジオボタンは無効にする
    user_answer = st.radio(
        "答えを選んでください:",
        current_quiz["options"],
        index=None, # 初期選択なし
        disabled=st.session_state.answer_submitted # 回答済みなら無効化
    )
    st.session_state.user_answer = user_answer # ユーザーの選択をセッションステートに保存

    # 回答ボタン
    # 回答済みでない場合のみボタンを表示
    if not st.session_state.answer_submitted:
        if st.button('回答する'):
            if st.session_state.user_answer is not None:
                st.session_state.answer_submitted = True # 回答済みフラグを立てる
                # 回答の判定と結果表示は、ボタンが押された後の再実行で行われる
                st.rerun() # 回答結果を表示するためにアプリを再実行
            else:
                st.warning("答えを選択してください！") # 回答が選ばれていない場合

    # 回答が提出された後の結果表示と次の問題へのボタン
    if st.session_state.answer_submitted:
        if st.session_state.user_answer == current_quiz["correct_answer"]:
            st.success("正解です！ 🎉")
            st.session_state.score += 1 # スコアを加算
        else:
            st.error(f"残念！不正解です。正解は「{current_quiz['correct_answer']}」でした。")

        # 次の問題へ進むボタン
        if st.button("次の問題へ"):
            st.session_state.current_quiz_index += 1
            st.session_state.answer_submitted = False # 回答済みフラグをリセット
            st.session_state.user_answer = None # ユーザーの回答をリセット
            st.rerun() # 次の問題を表示するためにアプリを再実行

else:
    # 全ての問題が終了した場合
    st.header("クイズ終了！")
    st.write(f"あなたのスコアは {st.session_state.score} / {len(quizzes)} でした！")
    
    # もう一度プレイするボタン
    if st.button("もう一度プレイする"):
        st.session_state.current_quiz_index = 0
        st.session_state.score = 0
        st.session_state.answer_submitted = False
        st.session_state.user_answer = None
        st.rerun() # 最初からやり直すためにアプリを再実行


# アプリケーションのフッター（任意）
st.markdown("---")
st.write("シンプルなクイズアプリの例")