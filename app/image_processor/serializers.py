from rest_framework import serializers
from .models import Palette, ClusterData
from django.db import transaction


class ClusterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClusterData
        fields = ('cluster_index', 'colors', 'ratios')


class PaletteSerializer(serializers.ModelSerializer):
    clusterData = serializers.JSONField(write_only=True)

    class Meta:
        model = Palette
        fields = ('id', 'name', 'date', 'imageUrl', 'clusterData')
        read_only_fields = ('id',)

    def create(self, validated_data):
        cluster_data = validated_data.pop('clusterData')
        clusters = cluster_data.get('clusters')
        ratios = cluster_data.get('ratio')

        with transaction.atomic():
            palette = Palette.objects.create(**validated_data)
            for index, colors in enumerate(clusters):
                ClusterData.objects.create(
                    palette=palette,
                    cluster_index=index,
                    colors=colors,
                    ratios=ratios[index]
                )
        return palette

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        cluster_data_representation = {
            'clusters': [],
            'ratio': []
        }
        for cluster in instance.cluster_data.all():
            cluster_data_representation['clusters'].append(cluster.colors)
            cluster_data_representation['ratio'].append(cluster.ratios)
        representation['clusterData'] = cluster_data_representation
        return representation
