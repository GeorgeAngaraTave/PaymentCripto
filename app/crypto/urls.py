from app.crypto.views.crypto import ViewCrypto, ViewCryptoTransation

from app.ext.register import url

urlpatterns = [
    url(ViewCrypto, endpoint=['/crypto', '/crypto/<string:id>'], namespace="View_crypto"),
    url(ViewCryptoTransation, endpoint=['/cryptoTransation', '/cryptoTransation/<string:id>'], namespace="View_CryptoTransation")
]
