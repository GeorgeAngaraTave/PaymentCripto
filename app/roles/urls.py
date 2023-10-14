from app.roles.views.view_roles import ViewRoles

from app.ext.register import url

urlpatterns = [
    url(ViewRoles, endpoint=['/roles', '/roles/<string:id>'], namespace="view_roles"),
]
