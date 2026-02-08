from rest_framework import serializers
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    
    student_no = serializers.RegexField(
        regex=r'^\d{3,20}$',
        trim_whitespace=True,
        error_messages={
            "invalid": "Student number must contain digits only"
        }
    )

    roll_no = serializers.RegexField(
        regex=r'^\d{3,20}$',
        trim_whitespace=True,
        error_messages={
            "invalid": "Roll number must contain digits only"
        }
    )
    class Meta:
        model = Player
        exclude = ['team']


class TeamRegistrationSerializer(serializers.Serializer):
    # teamId = serializers.CharField()
    teamId = serializers.RegexField(
        regex=r'^[A-Z0-9]{4,20}$',
        trim_whitespace=True,
        error_messages={
            "invalid": "Team ID must be uppercase letters/numbers"
        }
    ) 
    team_type = serializers.ChoiceField(choices=['solo', 'duo'])
    
    password = serializers.RegexField(
        regex=r'^(?=.*\d).{6,50}$',
        write_only=True,
        trim_whitespace=False,
        error_messages={
            "invalid": "Password must be 6–50 chars and contain a number"
        }
    )
    
    player1 = PlayerSerializer()
    player2 = PlayerSerializer(required=False)
    # password = serializers.CharField()

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