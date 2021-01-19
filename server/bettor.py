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

import models
import storage
import gql


def get_google_provider_cfg():
    return requests.get(
        "https://accounts.google.com/.well-known/openid-configuration"
    ).json()


def create_app():
    app = quart.Quart(__name__, static_folder=os.path.abspath("dist"))
    app = quart_cors.cors(app)

    google_client_id = os.environ.get("GOOGLE_CLIENT_ID", None)
    google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    session_key_string = os.getenv("SESSION_KEY")

    session_key = base64.b64decode(session_key_string)

    google_provider_cfg = get_google_provider_cfg()
    g = gql.create()
    session = storage.create()

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
            google_id = decoded["sub"]
            print(google_id)
            user = (
                session.query(models.User).filter(models.User.sub == google_id).first()
            )
            if user is None:
                user = create_user_from_google_info(**decoded)
                session.add(user)
                session.flush()
            return user
        quart.abort(401)

    @app.route("/v1/graphql", methods=["POST"])
    async def graphql():
        user = authenticate()
        body = await quart.request.get_json()
        context = {"session": storage.create, "user": user}
        res = g.execute(body["query"], context_value=context)
        return res.to_dict()

    @app.route("/v1/login", methods=["GET"])
    def login_begin():
        client = oauthlib.oauth2.WebApplicationClient(google_client_id)
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri="http://127.0.0.1:8082/callback",
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
            redirect_url="http://127.0.0.1:8082/callback",
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


def main():
    app = create_app()

    app.run()


if __name__ == "__main__":
    main()