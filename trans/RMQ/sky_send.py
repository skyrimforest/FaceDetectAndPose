from service_rmq import rmq_send,rmq_recv

if __name__ == '__main__':
    message={
        'sky':'test',
        'password':'233',
    }
    for i in range(1,10):
        message['sky']='test'+str(i)
        rmq_send(message)
    # rmq_send(message)
    # rmq_recv()
