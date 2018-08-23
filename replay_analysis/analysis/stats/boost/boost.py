from typing import TYPE_CHECKING, Dict

import numpy as np
import pandas as pd

from replay_analysis.analysis.stats.stats import BaseStat
from replay_analysis.generated.api import game_pb2
from replay_analysis.generated.api.player_pb2 import Player
from replay_analysis.generated.api.stats.player_stats_pb2 import PlayerStats
from replay_analysis.json_parser.game import Game

if TYPE_CHECKING:
    from ...saltie_game.saltie_game import SaltieGame


class BoostStat(BaseStat):

    def calculate_player_stat(self, player_stat_map: Dict[str, PlayerStats], game: Game, proto_game: game_pb2.Game,
                              player_map: Dict[str, Player], data_frames):
        goal_frames = data_frames.game.goal_number.notnull()

        for player_key, stats in player_stat_map.items():
            proto_boost = stats.boost
            player_name = player_map[player_key].name
            proto_boost.usage = self.get_player_boost_usage(data_frames[player_name][goal_frames])
            collection = self.get_player_boost_collection(data_frames[player_name][goal_frames])
            proto_boost.wasted_collection = self.get_player_boost_waste(proto_boost.usage, collection)
            proto_boost.num_small_boosts = collection['small']
            proto_boost.num_large_boosts = collection['big']

    @staticmethod
    def get_player_boost_usage(player_dataframe: pd.DataFrame) -> np.float64:
        _diff = -player_dataframe.boost.diff()
        boost_usage = _diff[_diff > 0].sum() / 255 * 100
        return boost_usage

    @staticmethod
    def get_player_boost_usage_max_speed(player_dataframe: pd.DataFrame) -> np.float64:
        """TODO: do this"""
        _diff = -player_dataframe.boost.diff()
        boost_usage = _diff[_diff > 0].sum() / 255 * 100
        return boost_usage

    @staticmethod
    def get_player_boost_collection(player_dataframe: pd.DataFrame) -> Dict[str, int]:
        value_counts = player_dataframe.boost_collect.value_counts()
        try:
            return {
                'big': int(value_counts[True]),
                'small': int(value_counts[False])
            }
        except KeyError:
            return {}

    @staticmethod
    def get_player_boost_waste(usage: np.float64, collection: Dict[str, int]) -> float:
        try:
            total_collected = collection['big'] * 100 + collection['small'] * 12
            return total_collected - usage
        except KeyError:
            return 0
