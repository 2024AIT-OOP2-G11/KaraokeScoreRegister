from flask import Blueprint, render_template, request, redirect, url_for
from models import Score, Challenger, Song

# Blueprintの作成
score_bp = Blueprint('score', __name__, url_prefix='/scores')


@score_bp.route('/')
def list():
    scores = Score.select()
    return render_template('score_list.html', title='得点一覧', items=scores)


@score_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        challenger_id = request.form['challenger_id']
        song_id = request.form['song_id']
        score_id = request.form['score_id']
        Score.create(challenger=challenger_id, song=song_id, score=score_id)
        return redirect(url_for('score.list'))
    
    challengers = Challenger.select()
    songs = Song.select()
    return render_template('score_add.html', challengers=challengers, songs=songs)


@score_bp.route('/edit/<int:score_id>', methods=['GET', 'POST'])
def edit(score_id):
    score = Score.get_or_none(Score.id == score_id)
    if not score:
        return redirect(url_for('score.list'))

    if request.method == 'POST':
        score.challenger = request.form['challenger_id']
        score.song = request.form['song_id']
        score.score = request.form['score_id']
        score.save()
        return redirect(url_for('score.list'))

    challengers = Challenger.select()
    songs = Song.select()
    return render_template('score_edit.html', score=score, challengers=challengers, songs=songs)

@score_bp.route('/delete/<int:score_id>', methods=['POST'])
def delete(score_id):
    # 指定されたIDの得点を取得
    score = Score.get_or_none(Score.id == score_id)
    if score:
        score.delete_instance()  # 得点を削除
    return redirect(url_for('score.list'))  # 得点一覧ページにリダイレクト
