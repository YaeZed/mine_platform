from rest_framework import serializers

from mines.models import Mine, ThreeDMineTunnel,Tunnel,Node


class MineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mine
        fields = '__all__'


class ThreeDMineTunnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreeDMineTunnel
        fields = '__all__'

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'

class TunnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tunnel
        fields = '__all__'
