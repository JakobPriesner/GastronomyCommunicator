from flask import Flask, request, jsonify
from gevent import pywsgi
import logging


def webapp(core):
    web_app = Flask("GASTROCOM")

    def get_data():
        data = request.args.to_dict()
        data.update(request.form.to_dict())
        return data

    @web_app.route("/api/GET/<action>/<inf>", methods=['GET'])
    def get_action(action, inf):
        if action == 'action':
            action = core.get_action(inf)
            return jsonify(action)

    @web_app.route("/api/POST/<action>", methods=['POST'])
    def post_action(action):
        data = get_data()
        if action == 'addAction':
            core.assign_action(data["description"], data["table_id"])
            return "ok"
        elif action == 'completeAction':
            core.complete_action(data["action_id"])
            return "ok"
        else:
            return "err"

    ws = pywsgi.WSGIServer(("0.0.0.0", 50500), web_app)
    logging.info('Server started successfully!')
    ws.serve_forever()
