from app.oauth_clients.views.view_oauth_client import ViewOauthClients

from app.ext.register import url

urlpatterns = [
    url(ViewOauthClients, endpoint=['/oauth/clients', '/oauth/clients/<string:id>'], namespace="oauth_client"),
]
