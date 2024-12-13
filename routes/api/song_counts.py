from flask import jsonify
from models import Score
from peewee import fn

def get_song_counts():
    # ここでデータの取得と整形をする！
    # 曲の出現回数を集計し、上位5曲を取得
    top_songs = (
        Score
        .select(Score.song, fn.COUNT(Score.song).alias('count'))
        .group_by(Score.song)
        .order_by(fn.COUNT(Score.song).desc())
        .limit(5)
    )
    
    # データを整形
    song_counts_data = {
        "labels": [song.song.song for song in top_songs],  # 曲名
        "data": [song.count for song in top_songs]         # 出現回数
    }
    
    # json形式でreturn
    # /api/song_countsでreturnできてるか確認！
    return jsonify(song_counts_data)