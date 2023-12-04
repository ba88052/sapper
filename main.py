import os

from flask import Flask, g, request
from domain.service.amadeus import start

from infrastructure.application_infra_adapter import \
    ApplicationRespositoryAdapter
from infrastructure.domain_infra_adapter import \
    DomainRespositoryAdapter
from interfaces import api_routes

# from infrastructure.database.domain_database_repository_adapter import DomainRespositoryAdapter

app = Flask(__name__)
app.register_blueprint(api_routes.routes)


@app.before_request
def setup_global_objects():
    g.APPLICATION_INFRA_ADAPTOR = ApplicationRespositoryAdapter()
    g.DOMAIN_INFRA_ADAPTER = DomainRespositoryAdapter()


# g.CLEANE_DATA_ADAPTOR = DomainRespositoryAdapter()


if __name__ == "__main__":
    start()
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
