import os

from flask import request, Response, send_file
from src.runner.export_task import export_data_wrt_dates, app
import logging
import json
import src.utils.constant as constant


def export_data():
    """
    :Endpoint:  /api/task/revoke/<task_id>
    :Type:  POST
    Request JSON format

    {
        'type':'upload_csv | team_csv',
        'date': {
                'sd': '2018-11-22'
        }
    }

    in the case of range -> {'type': 'upload_csv', 'date': {'dd1': '2018-11-08', 'dd2': '2018-11-22'}}

    Sends export data request to celery and return worker id

    :return: worker id
    """
    logging.info('Export request of from dates ' + str(request.get_json()))
    json_req_data = request.get_json()
    dsize = len(json_req_data['date'])
    d1 = None
    d2 = None
    if json_req_data['type'] == 'upload_csv':
        if dsize > 1:
            d1 = json_req_data['date']['dd1']
            d2 = json_req_data['date']['dd2']
        else:
            d1 = json_req_data['date']['sd']
        task = export_data_wrt_dates.delay(d1, d2)
        return Response(response={json.dumps({'task_id': task.task_id,
                                              'current_status': app.AsyncResult(task.task_id).status, 'drop': False})}
                        , status=200, mimetype='application/json')
    # elif json_req_data['type'] == 'team_csv':
    #     if dsize > 1:
    #         d1 = json_req_data['date']['dd1']
    #         d2 = json_req_data['date']['dd2']
    #     else:
    #         d1 = json_req_data['date']['sd']
    #
    #     task = export_data_wrt_dates.delay(d1, d2)
    #     return Response(response={json.dumps({'task_id': task.task_id,
    #                                           'current_status': app.AsyncResult(task.task_id).status, 'drop': False})}
    #                     , status=200, mimetype='application/json')
    else:
        logging.error('Unknown type parameters for request :: {0}'.format(json_req_data))
        return Response(response=None, status=403)


def get_task_status(task_id):
    """
    :Endpoint: /api/task/status/<task_id>
    :param: task_id
    :return: JSON result with status of task and have flag variable drop, incase code throws any exception
    """
    logging.info('New query for getting status :: {0}'.format(task_id))
    try:
        return Response(response={json.dumps({'task_id': task_id,
                                              'current_status': app.AsyncResult(task_id).status, 'drop': False})}
                        , status=200, mimetype='application/json')
    except Exception as e:
        logging.error('Error while fetching task status, of task :: {0}, \n{1}'.format(task_id, e.__str__()))
        return Response(response={json.dumps({'task_id': task_id,
                                              'current_status': 'FAILURE', 'drop': True})}
                        , status=200, mimetype='application/json')


def revoke_task(task_id):
    """
    :Endpoint: /api/task/revoke/<task_id>
    :param task_id:
    :return: result of revoking process
    """
    logging.info('Revoking task, task id :: {0}'.format(task_id))
    try:
        app.control.revoke(task_id, terminate=True)
        return Response(response=json.dumps({'task_id': task_id, 'revoked': True}), status=200)
    except Exception as e:
        logging.error('Error while revoking the task :: {0}, \n{1}'.format(task_id, e.__str__()))
        return Response(response=json.dumps({'task_id': task_id, 'revoked': False, 'reason': e.__str__()}),  status=200)


def download_file(task_id):
    file_path = os.path.join(constant.EXPORT_DIR, task_id+'.csv')
    logging.info('New download request for file :: {0}'.format(file_path))
    try:
        return send_file(filename_or_fp=file_path, attachment_filename=task_id+'.csv',
                         as_attachment=True)
    except Exception as e:
        logging.error('Error while sending the file :: {0}, \n{1}'.format(file_path, e.__str__()))
        return Response(response=json.dumps({'task_id': task_id, 'revoked': False, 'reason': e.__str__()}),  status=200)
