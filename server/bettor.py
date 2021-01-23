#!env/bin/python3

import logging
import sys
import os
import asyncio
import quart
import quart_cors
import jwt
import uuid
import base64
import hashlib
import json
import jsonpickle
import oauthlib.oauth2
import requests

from hypercorn.config import Config
from hypercorn.asyncio import serve

import models
import db
import schema as schema_factory


def get_google_provider_cfg():
    return requests.get(
        "https://accounts.google.com/.well-known/openid-configuration"
    ).json()


def create_app(path=None, auth_callback_url=None, prod=False):
    app = quart.Quart(__name__, static_folder=os.path.abspath("dist"))
    app = quart_cors.cors(app)

    google_client_id = os.environ.get("GOOGLE_CLIENT_ID", None)
    google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    session_key_string = os.getenv("SESSION_KEY")

    session_key = base64.b64decode(session_key_string)

    google_provider_cfg = get_google_provider_cfg()
    session = db.create(path=path)
    schema = schema_factory.create()

    def create_user_from_google_info(
        sub: str = None,
        name: str = None,
        email: str = None,
        picture: str = None,
        **kwargs
    ) -> models.User:
        return models.User(sub=sub, name=name, email=email, picture=picture)

    def authenticate():
        if "authorization" in quart.request.headers:
            header = quart.request.headers["authorization"]
            bearer, encoded = header.split(" ")
            decoded = jwt.decode(
                base64.b64decode(encoded), session_key, algorithms="HS256"
            )
            email = decoded["email"]
            user = session.query(models.User).filter(models.User.email == email).first()
            if user is None:
                user = create_user_from_google_info(**decoded)
                session.add(user)
                session.flush()
            return user
        quart.abort(401)

    @app.route("/v1/graphql", methods=["GET"])
    async def introspection():
        print(str(schema))
        return {"data": schema.introspect()}

    @app.route("/v1/graphql", methods=["POST"])
    async def graphql():
        user = authenticate()
        body = await quart.request.get_json()
        variables = body["variables"] if "variables" in body else None
        context = {"session": session, "user": user}
        res = schema.execute(body["query"], context_value=context, variables=variables)
        return res.to_dict()

    @app.route("/v1/login", methods=["GET"])
    def login_begin():
        client = oauthlib.oauth2.WebApplicationClient(google_client_id)
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=auth_callback_url,
            scope=["openid", "email", "profile"],
        )
        return jsonpickle.dumps({"url": request_uri})

    @app.route("/v1/login", methods=["POST"])
    async def login_complete():
        payload = await quart.request.get_json()
        code = payload["code"]

        client = oauthlib.oauth2.WebApplicationClient(google_client_id)
        token_url, headers, body = client.prepare_token_request(
            google_provider_cfg["token_endpoint"],
            redirect_url=auth_callback_url,
            code=code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(google_client_id, google_client_secret),
        )
        parsed = client.parse_request_body_response(json.dumps(token_response.json()))
        uri, headers, body = client.add_token(google_provider_cfg["userinfo_endpoint"])
        user_info_response = requests.get(uri, headers=headers, data=body)
        user = user_info_response.json()

        token = jwt.encode(user, session_key, algorithm="HS256")
        encoded = base64.b64encode(token.encode("utf-8"))
        return {"token": encoded.decode("utf-8"), "user": user}

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    async def index(path):
        if path == "":
            path = "index.html"
        file_path = "dist/" + path
        if os.path.isfile(file_path):
            logging.info("sending %s", file_path)
            return await app.send_static_file(path)
        logging.info("sending default")
        return await app.send_static_file("index.html")

    return app


def get_config():
    path = os.getenv("BETTOR_PATH")
    auth_callback_url = os.getenv("BETTOR_AUTH_CALLBACK_URL")

    return {
        "path": path if path else "sqlite:///data/bettor.sqlite3",
        "auth_callback_url": auth_callback_url
        if auth_callback_url
        else "http://127.0.0.1:8082/callback",
        "prod": os.getenv("BETTOR_PROD") != None,
    }


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )

    cfg = get_config()

    app = create_app(**cfg)

    if cfg["prod"]:
        config = Config()
        config.bind = ["0.0.0.0:5000"]
        asyncio.run(serve(app, config))
    else:
        app.run()


if __name__ == "__main__":
    main()
