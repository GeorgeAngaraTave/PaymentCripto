from app.reports.views.reports_transation import ViewReportsTransation

from app.ext.register import url

urlpatterns = [
    url(ViewReportsTransation, endpoint=['/repostsTransation', '/repostsTransation/<string:id>'], namespace="View_ReportsTransation")
]
