from queue import Queue
from threading import Thread

_terminate = object()   # We'll send this as a request when it's time for workers to stop.

def run_parallel(job_requests, worker_fn, worker_count=8):
    """Process jobs in parallel over multiple threads.

    Parameters
    ----------
    job_requests:
        A sequence of objects that specify information about each piece of work
        that must be performed.  These will be handed to workers.
    worker_fn:
        A function that will be called to process the job requests.
        This function will receive as a parameter one of the job_requests,
        and will return as its result a job_result.
    
    Returns
    -------
    A sequence of job_results that were returned by the worker_fn.
    Note that the jobs will be processed in an undetermined sequence,
    so you cannot rely on the returned results being in the same sequence
    as the input requests.

    The results are returned as a generator and are returned one at a time
    as they are processed.
    """

    results_q = Queue()
    requests_q = Queue()

    # Start worker threads.
    threads = []
    for i in range(worker_count):
        ## Here's the problem: you can't invoke worker proc here.
        thread = Thread(target=_worker_proc, args=(i, worker_fn, requests_q, results_q))
        threads.append(thread)
        #thread.daemon = True
        thread.start()

    # Enqueue work requests.
    num_requests = 0
    for request in job_requests:
        requests_q.put(request)
        num_requests += 1
    
    # Wait until all tasks are done.
    requests_q.join()

    # Collate results.
    for i in range(num_requests):
        result = results_q.get()
        results_q.task_done()
        yield result

    # Shut down the worker threads.
    for i in range(worker_count):
        requests_q.put(_terminate)

def _worker_proc(worker_num, work_fn, requests_q: Queue, results_q: Queue):
    """The main processing queue for the workers.
    Each worker invokes this function on its own thread.
    """
    while True:
        request = requests_q.get()
        if request == _terminate:
            break
        result = work_fn(request)
        requests_q.task_done()
        results_q.put(result)
