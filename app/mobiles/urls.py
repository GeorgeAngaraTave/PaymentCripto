from app.mobiles.views.mobiles import ViewMobiles

from app.ext.register import url

urlpatterns = [
    url(ViewMobiles, endpoint=['/mobiles', '/mobiles/<string:id>'], namespace="View_Mobiles"),
]
