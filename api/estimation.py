from flask import make_response


# keeping it sample for now
def estimate_time():
    return make_response({"time": 3 * 30 * 24 * 60, "cost": 86400}, 200)
