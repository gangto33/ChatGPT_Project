from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth import get_user_model, authenticate


class UserSerializer(ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password', 'password_confirm', 'nickname']
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def create(self, validated_data):
        validated_data.pop('password_confirm')  # 확인 비밀번호 필드는 저장하지 않음
        user = get_user_model().objects.create_user(**validated_data)
        return user
    
    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        def is_alpha(char):
            return 65 <= ord(char) <= 90 or 97 <= ord(char) <= 122

        if len(password) < 10 or len(password) > 50:
            raise serializers.ValidationError("비밀번호는 영문자, 숫자, 특수문자를 포함한 10자 이상이어야 합니다.")
        
        if not any(is_alpha(char) for char in password):
            raise serializers.ValidationError("비밀번호는 영문자를 포함해야 합니다.")
        
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("비밀번호는 숫자를 포함해야 합니다.")
        
        if not any(char in '!@#$%^&*()_+' for char in password):
            raise serializers.ValidationError("비밀번호는 특수문자를 포함해야 합니다.")
        
        if password != password_confirm:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        
        return data

    
class LoginSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError('이메일 또는 비밀번호가 올바르지 않습니다.')

        data['user'] = user
        return data