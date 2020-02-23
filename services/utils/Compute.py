from threading import Thread

#sample usage
# def runCompute(image_folder, _id, service_name):
#     result = ServiceLayer.train_neural_network(image_folder, _id, service_name)
#     print(result)

# myThread = Compute(runCompute, { 'image_folder': image_folder, '_id': _id, 'service_name': service_name } )
# myThread.start()

class Compute(Thread):
    def __init__(self, func, kwargs):
        Thread.__init__(self)
        self.func = func
        self.kwargs = kwargs

    def run(self):
        print("start")
        self.func(**(self.kwargs))
        print("done")