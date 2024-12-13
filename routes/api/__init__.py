from flask import Blueprint

api_routes = Blueprint("api", __name__, url_prefix='/api')

from .age_group import get_age_group
from .score_ranking import get_score_ranking
from .song_counts import get_song_counts

api_routes.add_url_rule("/age_group", view_func=get_age_group, methods=["GET"])
api_routes.add_url_rule("/score_ranking", view_func=get_score_ranking, methods=["GET"])
api_routes.add_url_rule("/song_counts", view_func=get_song_counts, methods=["GET"])
