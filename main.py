import os

from flask import Flask, g, request

from infrastructure.application_infra_adapter import \
    ApplicationRepositoryAdapter
from infrastructure.domain_infra_adapter import DomainRepositoryAdapter
from interfaces import api_routes

# from infrastructure.database.domain_database_repository_adapter import DomainRespositoryAdapter

app = Flask(__name__)
app.register_blueprint(api_routes.routes)


@app.before_request
def setup_global_objects():
    g.APPLICATION_INFRA_ADAPTOR = ApplicationRepositoryAdapter()
    g.DOMAIN_INFRA_ADAPTER = DomainRepositoryAdapter()


# g.CLEANE_DATA_ADAPTOR = DomainRespositoryAdapter()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
