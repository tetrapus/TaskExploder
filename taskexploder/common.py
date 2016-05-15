from flask import jsonify


def invalid_request(message):
    """ Construct an invalid request error """
    # TODO: return 400
    return jsonify({"status": "error", "message": message})
