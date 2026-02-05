from rest_framework import serializers
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        exclude = ['team']


class TeamRegistrationSerializer(serializers.Serializer):
    teamId = serializers.CharField()
    team_type = serializers.ChoiceField(choices=['solo', 'duo'])
    player1 = PlayerSerializer()
    player2 = PlayerSerializer(required=False)
    password = serializers.CharField()

    def validate(self, data):
        if data["team_type"] == "duo" and "player2" not in data:
            raise serializers.ValidationError(
                "player2 required for duo team"
            )
        if data["team_type"] == "solo" and "player2" in data:
            raise serializers.ValidationError(
                "solo team cannot have player2"
            )    
        return data