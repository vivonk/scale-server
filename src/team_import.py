#!/usr/bin/env python
import json
import os
import os.path
import shutil
from flask import current_app, request, Response
from flask.views import MethodView
import src.utils.constant as constants
import logging
from src.runner import import_task
# Meta
##################
__version__ = '0.1.0'

# Config
##################
DEBUG = True
SECRET_KEY = constants.secret_key

BASE_DIR = os.path.dirname(__file__)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
UPLOAD_DIRECTORY = '/tmp/backend-scops/uploads/'
CHUNKS_DIRECTORY = '/tmp/backend-scops/chunks/'
app = {
    'UPLOAD_DIRECTORY': UPLOAD_DIRECTORY,
    'CHUNKS_DIRECTORY': CHUNKS_DIRECTORY
}


# Utils
##################
def make_response(status=200, content=None):
    """ Construct a response to an upload request.
    Success is indicated by a status of 200 and { "success": true }
    contained in the content.
    """
    return current_app.response_class(json.dumps(content,
                                                 indent=None if request.is_xhr else 2), mimetype='text/plain')


def validate(attrs):
    """ No-op function which will validate the client-side data.
    """
    try:
        return True
    except Exception as e:
        return False


def handle_delete(uuid):
    """ Handles a filesystem delete based on UUID."""
    location = os.path.join(app['UPLOAD_DIRECTORY'], uuid)
    print(uuid)
    print(location)
    shutil.rmtree(location)


def handle_upload(f, attrs):
    """ Handle a chunked or non-chunked upload.
    """

    chunked = False
    only_one = False
    dest_folder = os.path.join(app['UPLOAD_DIRECTORY'])
    dest = os.path.join(dest_folder, attrs['qqfilename'])
    # Chunked
    if 'qqtotalparts' in attrs and int(attrs['qqtotalparts']) > 1:
        chunked = True
        dest_folder = os.path.join(app['CHUNKS_DIRECTORY'], attrs['qquuid'])
        dest = os.path.join(dest_folder, attrs['qqfilename'], str(attrs['qqpartindex']))
    else:
        only_one = True

    save_upload(f, dest, only_one)

    if chunked and (int(attrs['qqtotalparts']) - 1 == int(attrs['qqpartindex'])):
        combine_chunks(attrs['qqtotalparts'],
                       attrs['qqtotalfilesize'],
                       source_folder=os.path.dirname(dest),
                       dest=os.path.join(app['UPLOAD_DIRECTORY'],
                                         attrs['qqfilename']))

        shutil.rmtree(os.path.dirname(os.path.dirname(dest)))


def save_upload(f, path, only_one):
    """ Save an upload.
    Uploads are stored in /tmp/backend-scops/uploads
    """
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'wb+') as destination:
        destination.write(f.read())

    if only_one:
        logging.info('New file upload : ' + path)
        import_task.save_data_from_csv.delay(path)
        logging.info('Ran csv data save task')


def combine_chunks(total_parts, total_size, source_folder, dest):
    """ Combine a chunked file into a whole file again. Goes through each part
    , in order, and appends that part's bytes to another destination file.

    Chunks are stored in /tmp/backend-scops/chunks
    Uploads are saved in /tmp/backend-scops/uploads
    """

    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))

    with open(dest, 'wb+') as destination:
        for i in range(int(total_parts)):
            part = os.path.join(source_folder, str(i))
            with open(part, 'rb') as source:
                destination.write(source.read())
    logging.info('New file upload : ' + dest)
    import_task.save_data_from_csv.delay(dest)
    logging.info('Ran csv data save task')


class UploadAPI(MethodView):
    """ View which will handle all upload requests sent by Fine Uploader.

    Handles POST and DELETE requests.
    """

    def post(self):
        """A POST request. Validate the form and then handle the upload
        based ont the POSTed data. Does not handle extra parameters yet.
        """
        if validate(request.form):
            handle_upload(request.files['qqfile'], request.form)
            return make_response(200, {"success": True})
        else:
            return make_response(400, {"error", "Invalid request"})

    def delete(self, uuid):
        """A DELETE request. If found, deletes a file with the corresponding
        UUID from the server's filesystem.
        """
        try:
            handle_delete(uuid)
            return make_response(200, {"success": True})
        except Exception as e:
            return Response(400, {"success": False, "error": e.__str__()})


upload_team_view = UploadAPI.as_view('upload_team_view')
