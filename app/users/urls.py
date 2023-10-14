from app.users.views.users import ViewUsers

from app.ext.register import url

urlpatterns = [
    url(ViewUsers, endpoint=['/users', '/users/<string:id>'], namespace="view_users"),
]
