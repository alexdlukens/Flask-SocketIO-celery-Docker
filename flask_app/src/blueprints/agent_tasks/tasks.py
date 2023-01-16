
from flask_socketio import SocketIO
from celery.contrib.abortable import AbortableTask
import time
import json

from src.app import create_celery_app, socketio

celery = create_celery_app()

@celery.task(bind=True, base=AbortableTask)
def agent_show_status_celery(self, agent_info, user_id):
	print(f'IN CELERY TASK, agent_info = {agent_info}')
	sio = SocketIO(logger=True, engineio_logger=True, message_queue='redis://:devpassword@redis:6379/0', async_mode='threading')
	#from src.app import socketio as sio
	message = None
	self.update_state(state='PROGRESS',
                          meta={'current': 'working'})

	for i in range(100):
		sio.emit('web_response2', {'data': json.dumps({'msg':'SENT MESSAGE FROM CELERY TASK',
										'agent_info': agent_info,
										'user_id': user_id,
										'task_id': self.request.id,
										'idx': i})}, 
							broadcast=True, 
							namespace='/test_web2')
		time.sleep(10)
		if self.is_aborted():
			sio.emit('web_response2', {'data': json.dumps({'msg': f"aborting task with idx = {i}",
														  'task_id': self.request.id})},
					broadcast=True, 
					namespace='/test_web2')
			return
	sio.sleep(1)
	print('TRIED EMIT FROM CELERY AGENT STATUS')
	return('tried to print')
