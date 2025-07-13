from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GUEST_ACCOUNTS = [
    {
        "uid": "3967289164",
        "token": "F93BCABC034645D1A2EA21423B59AC80A740CAC748835D6DBECE726A2D75DAE7"
    },
    {
        "uid": "3998664944",
        "token": "90A3F497158A4F8CC6F4486977BCA3826EEF57310EC648442EDF5FB9EC7B3DDB"
    }
]

current_index = 0

def get_next_token():
    global current_index
    guest = GUEST_ACCOUNTS[current_index]
    current_index = (current_index + 1) % len(GUEST_ACCOUNTS)
    return guest

@app.route("/api/player-info")
def player_info():
    uid = request.args.get("uid")
    region = request.args.get("region")

    if not uid or not region:
        return jsonify({"error": "Missing uid or region"}), 400

    guest = get_next_token()
    headers = {
        "X-Requested-With": "com.dts.freefireth",
        "User-Agent": "FreeFireClient/1.100.1 Android/11",
        "X-Garena-Uid": guest["uid"],
        "X-Garena-Token": guest["token"]
    }

    try:
        url = f"https://ff.garena.com/api/playerInfo?account_id={uid}&region={region}"
        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()

        if "nickname" not in data:
            return jsonify({"error": "❌ Wrong UID or Region."}), 404

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "Failed", "details": str(e)}), 500
