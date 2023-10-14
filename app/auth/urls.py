from app.auth.views.login import ViewLogin, ViewLoginMovil
from app.auth.views.logout import ViewLogout

from app.ext.register import url


urlpatterns = [
    url(ViewLogin, endpoint=['/auth/login', '/login/<int:id>'], namespace="register_login"),
    url(ViewLoginMovil, endpoint=['/auth/loginMovil', '/login/<int:id>'], namespace="movil_login"),
    url(ViewLogout, endpoint=['/auth/logout'], namespace="register_logout"),
]
