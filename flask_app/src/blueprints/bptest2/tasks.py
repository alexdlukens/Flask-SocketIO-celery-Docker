
from flask_socketio import SocketIO

from src.app import create_celery_app, socketio

celery = create_celery_app()

@celery.task(bind=True)
def test_tally_celery(self):
	print('IN CELERY BACKGROUND TASK')
	sio = SocketIO(logger=True, engineio_logger=True, message_queue='redis://:devpassword@redis:6379/0', async_mode='threading')
	#from src.app import socketio as sio
	message = None
	self.update_state(state='PROGRESS',
                          meta={'current': 'working'})
	#sio.emit('local_request',{'data': message }, namespace='/test_local', broadcast=True)
	#sio.sleep(1)
	sio.emit('web_response2', {'data': 'SENT MESSAGE FROM CELERY TASK - BPTEST2'}, broadcast=True, namespace='/test_web2')
	sio.sleep(1)
	print('TRIED EMIT FROM CELERY BPTEST2')
	return('tried to print')
