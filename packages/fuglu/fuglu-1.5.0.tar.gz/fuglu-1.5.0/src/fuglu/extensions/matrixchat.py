import os
import time
import logging
from unittest.mock import MagicMock
try:
    from matrix_client.client import MatrixClient
    from matrix_client.room import Room
    from matrix_client import htmlmsgs
    from matrix_client.errors import MatrixHttpLibError
    HAVE_MATRIX = True
except ImportError:
    HAVE_MATRIX = False
    htmlmsgs = None
    MatrixClient = MagicMock()
    



def room_invite_cb(room_id, state):
    """
    callback (func(room_id, state)): Callback called when an invite arrives.
    """
    try:
        import json
        statedata = str(json.dumps(state, indent=4))
        logging.getLogger('matrix').warning(f"Got room invite to room: {room_id}, state data:\n{statedata}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        logging.getLogger('matrix').warning(f"Got room invite to room: {room_id}, state={state}")

    client = MatrixClientSingleton.get()
    client.join_room(room_id)
    logging.getLogger('matrix').warning(f"Accepted room invite to room: {room_id}")



class MatrixClientSingleton(object):
    """
    Process singleton to store a default MatrixClient instance
    """

    instance = None
    _proc_pid = None
    _token = None
    _reset_timestamp = None

    @staticmethod
    def reset() -> None:
        MatrixClientSingleton.instance = None
        MatrixClientSingleton._proc_pid = None
        MatrixClientSingleton._token = None
        MatrixClientSingleton._reset_timestamp = None

    
    @staticmethod
    def get(username=None, password=None, server=None) -> MatrixClient:
        pid = os.getpid()

        if MatrixClientSingleton._reset_timestamp and time.time() > MatrixClientSingleton._reset_timestamp:
            # reset client
            MatrixClientSingleton.reset()

        if pid == MatrixClientSingleton._proc_pid and MatrixClientSingleton.instance is not None:
            pass
        else:
            
            # change retry time from (default=5000ms)
            matrixhttpapi_kwargs = {'max_retry': 2,
                                    'request_timeout': 2,  # 2 seconds...
                                    }
            MatrixClientSingleton.instance = MatrixClient(server.rstrip("/"), matrixhttpapi_kwargs=matrixhttpapi_kwargs)
            MatrixClientSingleton._token = MatrixClientSingleton.instance.login(username, password)
            MatrixClientSingleton.instance.add_invite_listener(room_invite_cb)
            # to join a room, the listener thread has to be enabled, for simple logging this is not required...
            #MatrixClientSingleton.instance.start_listener_thread()

            MatrixClientSingleton._proc_pid = pid

        return MatrixClientSingleton.instance
