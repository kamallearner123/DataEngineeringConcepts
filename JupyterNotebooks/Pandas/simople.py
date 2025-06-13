from multiprocessing import Process

def fun(args):
    print(args)
    pass


pid = Process(target=fun, args=(1,))
pid.start()
pid.join()
