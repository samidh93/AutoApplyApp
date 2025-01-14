from concurrent.futures import ThreadPoolExecutor

class ThreadPoolManager:
    def __init__(self, func, *func_args, **items):
        self.threaded_func = func
        self.threaded_func_args = func_args
        self.items = items

    def run(self):
        # Create a thread pool and map the items to the function
        with ThreadPoolExecutor(max_workers=2) as executor:
            self.results = executor.map(self.threaded_func, *self.threaded_func_args, **self.items)
        print("All threads have completed.")

def test(a, b, c):
    print(a)
    print(a+b)
    print(a+b+c)

pool = ThreadPoolManager(test, [1,2,3], items=["A", "B", "C"])
pool.run()