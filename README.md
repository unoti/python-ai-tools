# aitools

Utility functions for putting AI projects into production.

 * **Multithread.run_parallel**.  A simple recipe for running many work requests in parallel on multiple threads with multiple consumers.

## Next steps
These are ideas for improving this library:
 * **Multithread.run_parallel**  Make an object that runs manages the pool of workers.  Add methods on it to tell you how many items have been submitted, how many are remaining, how many are being processed per second, and estimated time until completion.