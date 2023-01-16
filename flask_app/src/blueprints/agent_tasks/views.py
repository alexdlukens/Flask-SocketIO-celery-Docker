from flask import Blueprint, request, current_app

from src.app import socketio, CELERY_BACKEND_URL, create_celery_app
# from celery import current_app

from flask_socketio import emit, join_room, leave_room, \
    close_room, rooms, disconnect
from celery.contrib.abortable import AbortableAsyncResult

agent_tasks = Blueprint('agent_tasks', __name__)

@agent_tasks.route('/SendTallyFunc2/', methods=['GET','POST'])
def send_room_message_without_socketio():
        from src.blueprints.agent_tasks.tasks import agent_show_status_celery

        agent_data = request.get_json()
        task = agent_show_status_celery.delay(agent_data, 'user1')
        print ('SENDING TO CELERY.. Please wait..')
        print(f'started task {task.id}')
        return(f'Processing from CELERY.. please wait.. {task.id}')

@agent_tasks.route('/SendTallyFunc2/<name>', methods=['DELETE'])
def del_agent_status_task(name):
        celery = create_celery_app(current_app)
        
        
        try:
            task = AbortableAsyncResult(name, app=celery)
            print(f'about to abort task {task.id}')
            task.abort()

        except Exception as e:
            print(f'error: {e}')
        return(f'Aborted task {name}')

@socketio.on('connect', namespace='/test_web2')
def test_connect():
    print('WEB CONNECTED ON OPEN AUTO')
    emit('web_response', {'data': 'Connected', 'count': 0})


@socketio.on('web_event', namespace='/test_web2')
def test_message(message):
    emit('web_response', {'data': message['data']})

@socketio.on('disconnect_request', namespace='/test_web2')
def local_disconnect_request():
    emit('lweb_response',
         {'data': 'Disconnected!'})
    socketio.sleep(0)
    print('WEB DISCONNECTED ON CLOSE/REFRESH')
    disconnect()