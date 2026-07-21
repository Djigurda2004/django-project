from rest_framework import serializers
from ..models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Article
        fields=('id',
                'title',
                'announcement',
                'created_at',
                'author',
                )

class ArticleDetailSeriazlizer(serializers.ModelSerializer):
    class Meta:
        model=Article
        fields=('id',
                'title',
                'announcement',
                'full_text',
                'created_at',
                'updated_at',
                'author',
                'likes_count',
                'views',
                )
        read_only_fields=('id',
                          'created_at',
                          'updated_at',
                          'author',
                          'likes_count',
                          'views',
                          )