import os
from threading import Thread
from queue import Queue

# The use of threading is completely overkill for 99.9% of use cases

def get_file_names(dir):
    files = []
    for filename in os.listdir(dir):
        files.append(os.path.join(dir, filename))
    return files

# Threaded function for queue processing.
# args:
#       q: queue of files to process
#       result: list of dicts
#       getData: a function that takes a filename as an argument and returns a dict
def readfile(q, result, getData):
    while not q.empty():
        files = q.get()                      #fetch new work from the Queue
        try:
            data = getData(files[1])
            result[files[0]] = data          #Store data back at correct index
        except Exception as e:
            print(f'Error with file {files[1]}: {e}!')
            result[files[0]] = {}
        #signal to the queue that task has been processed
        q.task_done()
    return True

def get_data_from_files(getData, dir):
    files = get_file_names(dir)
    #set up the queue to hold all the files
    q = Queue(maxsize=0)
    # Use many threads (50 max, or one for each file)
    num_theads = min(50, len(files))

    #Populating Queue with tasks
    results = [{} for x in files]
    #load up the queue with the files to fetch and the index for each job (as a tuple):
    for i in range(len(files)):
        #need the index and the file in each queue item.
        q.put((i,files[i]))

    #Starting worker threads on queue processing
    for i in range(num_theads):
        worker = Thread(target=readfile, args=(q, results, getData))
        #worker.setDaemon(True)    #setting threads as "daemon" allows main program to 
                                #exit eventually even if these dont finish 
                                #correctly.
        worker.start()
    #now we wait until the queue has been processed
    q.join()
    return results
#get_data_from_files()
