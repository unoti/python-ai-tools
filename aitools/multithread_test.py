import unittest
from multithread import run_parallel

def worker_fn(req):
    """Req will be an integer.  Our work will be to multiply it by 2."""
    return req * 2

class MultiTest(unittest.TestCase):
    def test(self):
        requests = [i for i in range(10)]
        results = run_parallel(requests, worker_fn)
        results.sort()
        self.assertEqual(10, len(results))
        self.assertEqual(2, results[1])
        self.assertEqual(18, results[9])


if __name__ == '__main__':
    unittest.main()