from flask import Blueprint, jsonify, request

from sqlalchemy import exc

from project.api.models import Request
from database_singleton import Singleton

request_blueprint = Blueprint("requests", __name__)

db = Singleton().database_connection()


@request_blueprint.route("/requests", methods=["POST"])
def create_request():
    post_data = request.get_json()

    error_response = {"status": "fail", "message": "Invalid payload."}

    productname = (post_data.get("productname"),)
    startdate = (post_data.get("startdate"),)
    enddate = (post_data.get("enddate"),)
    description = (post_data.get("description"),)
    requester = (post_data.get("requester"),)
    productcategoryid = (post_data.get("productcategoryid"),)
    lender = None

    lending_request = Request(
        productname,
        startdate,
        enddate,
        description,
        requester,
        lender,
        productcategoryid,
    )

    try:
        db.session.add(lending_request)
        db.session.commit()

        response = {"status": "success", "data": {"request": lending_request.to_json()}}

        return jsonify(response), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(error_response), 400
