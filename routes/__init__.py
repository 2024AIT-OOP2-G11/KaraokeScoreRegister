from .challenger import challenger_bp
from .song import song_bp
from .score import score_bp
from .api import api_routes

# Blueprintをリストとしてまとめる
blueprints = [
  challenger_bp,
  song_bp,
  score_bp,
  api_routes
]
