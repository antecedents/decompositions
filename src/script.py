import logging
import multiprocessing

def computations():
    logging.info(multiprocessing.cpu_count())


if __name__ == '__main__':

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n\n',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # .join() ensures script waits for <process> to terminate
    process = multiprocessing.Process(target=computations)
    process.start()
    process.join()
