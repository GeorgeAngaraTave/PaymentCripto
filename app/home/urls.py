from app.home.views.home import ViewHome

from app.ext.register import url


urlpatterns = [
    url(ViewHome, endpoint=['/home'], namespace="register_home")
]
