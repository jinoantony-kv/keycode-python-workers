def worker1_cb(ch, method, properties, body):
    print("Worker called successfully")
    print(ch, method, properties, body)
