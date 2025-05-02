import streamlit as st
import random

# クイズデータ
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
if 'current_quiz_index' not in st.session_state:
    st.session_state.current_quiz_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
# 'answer_submitted' は、回答ボタンが押され、結果を表示すべき状態かを示す
if 'answer_submitted' not in st.session_state:
    st.session_state.answer_submitted = False
# 'user_answer' は、ユーザーがラジオボタンで選択した回答を保持 (ラジオボタンのkeyで自動管理)
if 'user_answer_radio' not in st.session_state:
     st.session_state.user_answer_radio = None
# 'last_answer_correct' は、直前の回答が正解だったか不正解だったかを結果表示用に保持
if 'last_answer_correct' not in st.session_state:
     st.session_state.last_answer_correct = None
# 'correct_answer_text' は、不正解だった場合に正解のテキストを結果表示用に保持
if 'correct_answer_text' not in st.session_state:
    st.session_state.correct_answer_text = None


st.title('かんたんクイズアプリ')

# 現在の問題を表示
if st.session_state.current_quiz_index < len(quizzes):
    current_quiz = quizzes[st.session_state.current_quiz_index]

    st.header(f"問題 {st.session_state.current_quiz_index + 1}")
    st.write(current_quiz["question"])

    # 選択肢を表示（ラジオボタン）
    # key を指定することで、Streamlitがセッションステートで状態を管理してくれる
    # 回答済みの場合、ラジオボタンは無効にする
    st.radio(
        "答えを選んでください:",
        current_quiz["options"],
        index=None, # 初期選択なし
        key='user_answer_radio', # セッションステートで user_answer_radio としてアクセス可能になる
        disabled=st.session_state.answer_submitted # 回答済みなら無効化
    )

    # 回答ボタン
    # 回答済みでない場合のみボタンを表示
    if not st.session_state.answer_submitted:
        if st.button('回答する'):
            # ボタンが押されたときにこのブロックが実行される
            # ユーザーの回答は st.session_state.user_answer_radio で取得できる
            if st.session_state.user_answer_radio is not None:

                # ★ 回答を判定し、スコアを加算するのはここで一度だけ行う ★
                if st.session_state.user_answer_radio == current_quiz["correct_answer"]:
                    st.session_state.score += 1 # 正解ならスコア加算
                    st.session_state.last_answer_correct = True # 結果表示用に記録
                else:
                    st.session_state.last_answer_correct = False # 結果表示用に記録
                    st.session_state.correct_answer_text = current_quiz['correct_answer'] # 正解のテキストも記録

                # 回答済みフラグを立てる
                st.session_state.answer_submitted = True

                # 結果表示のためにアプリを再実行
                st.rerun()
            else:
                st.warning("答えを選択してください！") # 回答が選ばれていない場合

# 回答が提出され、結果を表示すべき状態の場合 (st.rerun() 後の実行で評価される)
# answer_submitted が True であり、かつ、表示すべき結果がある場合
# 現在表示している問題が、結果を表示すべき問題の「次」になっているため、インデックスは st.session_state.current_quiz_index を使う
# ただし、全問題終了時は表示しない
if st.session_state.answer_submitted and st.session_state.current_quiz_index <= len(quizzes):
     # 'last_answer_correct' が存在することを確認することで、結果表示が必要か判断
     if st.session_state.last_answer_correct is not None:
         # 直前の回答の結果を表示
         if st.session_state.last_answer_correct:
              st.success("正解でした！ 🎉")
         else:
              st.error(f"残念！不正解でした。正解は「{st.session_state.correct_answer_text}」でした。")

         # 次の問題へ進むボタン (結果表示後に表示)
         if st.button("次の問題へ"):
             # 次の問題へ進む準備は、回答ボタンのブロックで行われているため
             # ここではセッションステートのフラグをリセットして再実行するだけでOK
             st.session_state.answer_submitted = False # 回答済みフラグをリセット
             # 結果表示用のセッションステートもクリア
             if 'last_answer_correct' in st.session_state: del st.session_state.last_answer_correct
             if 'correct_answer_text' in st.session_state: del st.session_state.correct_answer_text
             # ラジオボタンの状態もリセット（key を使っているため、key の値をリセットするのが推奨）
             st.session_state.user_answer_radio = None
             st.rerun() # 次の問題を表示するためにアプリを再実行


else: # 全ての問題が終了
    st.header("クイズ終了！")
    st.write(f"あなたのスコアは {st.session_state.score} / {len(quizzes)} でした！")

    # もう一度プレイするボタン
    if st.button("もう一度プレイする"):
        st.session_state.current_quiz_index = 0
        st.session_state.score = 0
        st.session_state.answer_submitted = False
        st.session_state.user_answer_radio = None # ラジオボタンの状態をリセット
        # 結果表示用のセッションステートもクリア
        if 'last_answer_correct' in st.session_state: del st.session_state.last_answer_correct
        if 'correct_answer_text' in st.session_state: del st.session_state.correct_answer_text
        st.rerun() # 最初からやり直すためにアプリを再実行


# アプリケーションのフッター（任意）
st.markdown("---")
st.write("シンプルなクイズアプリの例 (スコア修正版)")
