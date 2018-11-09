import logging
from flask import Flask

import src.controllers.upload as upload_controller
import src.utils.constant as constant
import src.export as export
from src.upload import upload_view
import src.controllers.export as export_controller
import src.controllers.team_import as import_controller
from src.team_import import upload_team_view

# app upper layer secrets
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = constant.secret_key
app.config['SESSION_TYPE'] = 'filesystem'

# register endpoints

# UI
app.add_url_rule(rule='/upload', view_func=upload_controller.upload_file, methods=['GET'])
app.add_url_rule(rule='/export', view_func=export_controller.export_file, methods=['GET'])
app.add_url_rule(rule='/team', view_func=import_controller.import_file, methods=['GET'])

# Task
app.add_url_rule(rule='/api/upload', view_func=upload_view, methods=['POST', ])
app.add_url_rule(rule='/api/upload/<uuid>', view_func=upload_view, methods=['DELETE', ])
app.add_url_rule(rule='/api/export', view_func=export.export_data, methods=['POST', 'PUT'])
app.add_url_rule(rule='/api/task/result/<task_id>', view_func=export.get_task_status, methods=['GET'])
app.add_url_rule(rule='/api/task/revoke/<task_id>', view_func=export.revoke_task, methods=['GET'])
app.add_url_rule(rule='/api/task/download/<task_id>', view_func=export.download_file, methods=['GET'])
app.add_url_rule(rule='/api/team', view_func=upload_team_view, methods=['POST', ])
app.add_url_rule(rule='/api/team/<uuid>', view_func=upload_team_view, methods=['DELETE', ])

# logger configs
logging.basicConfig(filename="./debug-server.log", level=logging.DEBUG)
logging.warning("INFO: Server starting")


@app.route('/ping')
def ping_pong():
    return 'pong'


if __name__ == '__main__':
    app.run(port=8081)
