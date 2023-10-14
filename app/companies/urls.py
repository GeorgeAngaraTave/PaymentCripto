from app.companies.views.view_companies import ViewCompanies

from app.ext.register import url

urlpatterns = [
    url(ViewCompanies, endpoint=['/companies', '/companies/<string:id>'], namespace="companies"),
]
