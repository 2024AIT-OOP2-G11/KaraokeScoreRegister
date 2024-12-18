from flask import Flask, render_template, jsonify
from peewee import fn
from models import initialize_database, Score, Challenger
from routes import blueprints

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    # トップ5の得点を取得
    top_scores = (
        Score
        .select(Score.song, Score.challenger, Score.score)
        .order_by(Score.score.desc())
        .limit(5)
    )

    top_score_songs = []

    # データの整形
    for s in top_scores:
        temp = [s.challenger.name, s.song.song, s.score]
        top_score_songs.append(temp)

    # 曲の出現回数を集計し、上位5曲を取得
    top_songs = (
        Score
        .select(Score.song, fn.COUNT(Score.song).alias('count'))
        .group_by(Score.song)
        .order_by(fn.COUNT(Score.song).desc())
        .limit(5)
    )

    # データを整形
    song_names = [song.song.song for song in top_songs]  # 曲名
    song_counts = [song.count for song in top_songs]     # 出現回数

    # テンプレートにデータを渡してレンダリング
    return render_template(
        "index.html",
        song_names=song_names,
        song_counts=song_counts,
        top_score_songs=top_score_songs,
    )

# 年代別人数のルート
@app.route('/age')
def age_distribution():
    # 年代別の人数を取得
    age_list = (
        Challenger
        .select(Challenger.age, fn.COUNT(Challenger.id).alias('count'))
        .group_by(Challenger.age)
    )

    # 年代ラベル
    age_labels = ['10代以下', '20代', '30代', '40代', '50代以上']

    # 初期化された年代別カウント
    age_counts = [0, 0, 0, 0, 0]

    # 年代ごとに人数をカウント
    for al in age_list:
        if al.age <= 19:
            age_counts[0] += al.count
        elif al.age <= 29:
            age_counts[1] += al.count
        elif al.age <= 39:
            age_counts[2] += al.count
        elif al.age <= 49:
            age_counts[3] += al.count
        else:
            age_counts[4] += al.count

    # データを整形してテンプレートに渡す
    return render_template('age.html', age_labels=age_labels, age_counts=age_counts)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
