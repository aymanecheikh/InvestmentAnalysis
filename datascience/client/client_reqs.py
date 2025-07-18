import time

import client_init

start = time.perf_counter()
client = client_init.Client()
client.get_datafeed("AAPL")
end = time.perf_counter()
print(f"Elapsed time: {end - start:.2f} seconds")
