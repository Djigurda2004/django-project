from rest_framework.permissions import IsAuthenticated,SAFE_METHODS

class IsArticleAuthor(IsAuthenticated):
    def has_object_permission(self,request,view,obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.id==obj.author.id