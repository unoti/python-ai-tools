

def run_parallel(job_requests, worker_fn, worker_threads=8):
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
    """

    results = []
    for req in job_requests:
        result = worker_fn(req)
        results.append(result)
    return results