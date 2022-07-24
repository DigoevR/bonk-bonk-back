from rest_framework import serializers
from custom_auth.serializers import UserSerializer
from tennis.models import Game, Match
from custom_auth.models import User


class GameSerializer(serializers.ModelSerializer):
    my_score = serializers.IntegerField(min_value=0, max_value=40, required=True, source='requesting_player_score', write_only=True)
    opponents_score = serializers.IntegerField(min_value=0, max_value=40, required=True, source='confirming_player_score', write_only=True)
    winner = UserSerializer(read_only=True)
    loser = UserSerializer(read_only=True)

    def validate(self, attrs):
        if attrs['requesting_player_score'] == attrs['confirming_player_score']:
            raise serializers.ValidationError({'score': 'Draws are not allowed'})
        return super().validate(attrs)

    class Meta:
        model = Game
        fields = ('my_score', 'opponents_score', 'id', 'winner', 'loser', 'winner_score', 'loser_score')
        write_only_fields = ('my_score', 'opponents_score')
        read_only_fields = ('id', 'winner', 'loser', 'winner_score', 'loser_score')


class MatchSerializer(serializers.ModelSerializer):
    games = GameSerializer(many=True, required=True)
    opponent_id = serializers.PrimaryKeyRelatedField(source='confirming_player', required=True, queryset=User.objects.all(), write_only=True)
    winner = UserSerializer(read_only=True)
    loser = UserSerializer(read_only=True)
    
    def validate(self, attrs):
        validation = super().validate(attrs)
        games = attrs['games']
        if len(attrs['games']) > attrs['match_type']:
            raise serializers.ValidationError({'games': 'Too many games for this type of match'})
        games_results = [game['requesting_player_score'] > game['confirming_player_score'] for game in games]
        wins = len(list(filter(lambda x: x, games_results)))
        loses = len(games_results) - wins
        validation['result'] = wins > loses
        if max(wins, loses) < attrs['match_type'] // 2 + 1:
            raise serializers.ValidationError({'games': 'Not enough games'})
        return validation
    
    def create(self, validated_data):
        games_data = validated_data.pop('games')
        match = Match(**validated_data)
        match.calculate_elo_change()
        match.save()
        for game_data in games_data:
            game_data.update({'match': match})
            GameSerializer(data=game_data).create(game_data)
        return match

    class Meta:
        model = Match
        fields = ('match_type', 'opponent_id', 'games', 'id', 'winner', 'loser', 'elo_change', 'is_confirmed')
        write_only_fields = ('opponent_id')
        read_only_fields = ('id', 'winner', 'loser', 'elo_change', 'is_confirmed')