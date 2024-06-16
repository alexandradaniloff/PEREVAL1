from rest_framework import serializers, viewsets, status, generics
from .models import *
from drf_writable_nested import WritableNestedModelSerializer


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"

class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = "__all__"


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"


class ImagesSerializer(serializers.ModelSerializer):
    image=serializers.URLField()

    class Meta:
        model = Images
        fields = "__all__"


class PerevalSerializer(WritableNestedModelSerializer):
    tourist_id = UsersSerializer()
    coord_id = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True)
    add_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    #status = serializers.CharField()
    class Meta:
        model = Pereval
        fields = ['id', 'status', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'tourist_id', 'coord_id', 'level',
                  'images']

    def create(self, validated_data, **kwargs):
        tourist_id = validated_data.pop('tourist_id')
        coord_id = validated_data.pop('coord_id')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        tourist_id, created = Users.objects.get_or_create(**tourist_id)

        coord_id = Coords.objects.create(**coord_id)
        level = Level.objects.create(**level)
        pereval = Pereval.objects.create(**validated_data, tourist_id=tourist_id, coord_id=coord_id, level=level,
                                         status="NW")

        for i in images:
            image = i.pop('image')
            title = i.pop('title')
            Images.objects.create(image=image, pereval_id=pereval, title=title)

        return pereval

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.tourist_id
            data_user = data.get('tourist_id')
            validating_user_fields = [
                instance_user.last_name != data_user['last_name'],
                instance_user.first_name != data_user['first_name'],
                instance_user.patronymic != data_user['patronymic'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],

            ]

            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError({'Отклонено': 'Нельзя изменять данные пользователя'})
        return data


