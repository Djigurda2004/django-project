def get_article_views_key(article_id):
    return f"articles:article:{article_id}:views"

def get_most_popular_articles_key():
    return "articles:article:most_popular"