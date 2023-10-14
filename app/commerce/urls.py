from app.commerce.views.commerce import ViewCommerce

from app.ext.register import url

urlpatterns = [
    url(ViewCommerce, endpoint=['/commerce', '/commerce/<string:id>'], namespace="View_Commerce"),
]
