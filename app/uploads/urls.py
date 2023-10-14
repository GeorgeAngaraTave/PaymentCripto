from app.uploads.views.uploads import ViewUpload
from app.ext.register import url

urlpatterns = [
    url(ViewUpload, endpoint=['/upload', '/upload/<string:id>'], namespace="register_upload"),
]
