from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Photo, Category
from rest_framework.fields import CurrentUserDefault


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        #fields = ['user']
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    #category = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # print(user)
    #category = serializers.SerializerMethodField('get_category')

    def get_category(self, category):
        #user = CategorySerializer(required=True)
        user = PrimaryKeyRelatedField(allow_null=True, queryset=Category.objects.all(), required=False)
        qs = Category.objects.filter(user=user)
        print(qs)
        serializer = CategorySerializer(instance=qs, many=True)
        print(serializer.data)
        return serializer.data

    class Meta:
        model = Photo
        #fields = '__all__'
        fields = ['image', 'category', 'description']
