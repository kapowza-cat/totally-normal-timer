import time

print("Testing")
test_time = 300


start = time.perf_counter()
for count in range(test_time):
    time.sleep(1)
end = time.perf_counter()

elapsed = end - start
print(f'Drifted by {abs(test_time-elapsed)}')