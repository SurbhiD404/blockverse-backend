import re
from rest_framework import serializers
from .models import Player, Team

class PlayerSerializer(serializers.ModelSerializer):
    name = serializers.RegexField(
        regex=r"^[A-Za-z .'-]{3,40}$" ,
        error_messages={
            "invalid": "Name must contain only letters and spaces (3–40 chars)"
        }
    )
    phone = serializers.RegexField(
        regex=r'^[6-9]\d{9}$',
        error_messages={
            "invalid": "Phone must be valid 10-digit Indian number"
        }
    )
    
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
    email = serializers.EmailField()
    
    class Meta:
        model = Player
        exclude = ['team']
    
    def validate(self,data):
        email = data.get("email")
        student_no = data.get("student_no")
        
        if not email or not student_no:
            return data
            
        email = email.lower().strip()
        student_no = str(student_no)
        
        if not email.endswith("@akgec.ac.in"):
             raise serializers.ValidationError({"email": "Email must be an AKGEC email address"})    
        username = email.split("@")[0]
        if student_no not in username:
                raise serializers.ValidationError({"email": "Email username must contain student number"}) 
         
        data["email"] = email    
        return data 

    def validate_student_no(self, value):
        if Player.objects.filter(student_no=value).exists():
            raise serializers.ValidationError("Student number already registered")
        return value

    def validate_roll_no(self, value):
        if Player.objects.filter(roll_no=value).exists():
            raise serializers.ValidationError("Roll number already registered")
        return value


class TeamRegistrationSerializer(serializers.Serializer):
    # teamId = serializers.CharField()
    teamId = serializers.RegexField(
        regex=r'^[A-Z0-9]{4,20}$',
        trim_whitespace=True,
        error_messages={
            "invalid": "Team ID must be uppercase letters/numbers"
        }
    ) 
    def validate_teamId(self, value):
        value = value.upper()
        if Team.objects.filter(team_id=value).exists():
           raise serializers.ValidationError("Team ID already exists")
        return value
    
    team_type = serializers.ChoiceField(choices=['solo', 'duo'])
    
    # password = serializers.RegexField(
    #     regex=r'^(?=.*\d).{6,50}$',
    #     write_only=True,
    #     trim_whitespace=False,
    #     error_messages={
    #         "invalid": "Password must be 6–50 chars and contain a number"
    #     }
    # )
    
    password = serializers.RegexField(
        regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,50}$',
        write_only=True,
        trim_whitespace=False,
        error_messages={
            "invalid": "Password must contain uppercase letter, number, symbol and be 8–50 chars long"
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
            
        if "player2" in data:
            if data["player1"]["roll_no"] == data["player2"]["roll_no"]:
                raise serializers.ValidationError(
                    "Both players cannot have the same roll number"
                )  
                
                
        
            if data["player1"]["student_no"] ==data["player2"]["student_no"]:
                raise serializers.ValidationError(
                    "Both players cannot have the same student number"
                ) 
            
                       
        return data