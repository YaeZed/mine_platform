from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(allow_blank=True, required=False)  # 允许为空
    nickname = serializers.CharField(allow_blank=True, required=False)  # 允许为空
    email = serializers.EmailField(allow_blank=True, required=False)  # 允许为空
    mobile = serializers.CharField(allow_blank=True, required=False)  # 允许为空
    class Meta:
        model = User
        fields = ('id', 'avatar', 'nickname', 'email', 'mobile')  # 包含要序列化的字段
        read_only_fields = ('id',) # id 是只读的
    def update(self, instance, validated_data):
        """
        自定义 update 方法，处理字段为空的情况
        """
        instance.avatar = validated_data.get('avatar', '')  # 如果没有提供，则设为空字符串
        instance.nickname = validated_data.get('nickname', '')  # 如果没有提供，则设为空字符串
        instance.email = validated_data.get('email', '')  # 如果没有提供，则设为空字符串
        instance.mobile = validated_data.get('mobile', '')  # 如果没有提供，则设为空字符串
        instance.save()
        return instance