import time

print("Testing")
test_time = 5


start = time.perf_counter()

# next_tick = time.perf_counter() + 1
# for count in range(test_time):
#     remaining = next_tick - time.perf_counter()
#     if remaining < 0.9:
#         remaining = 1
#     time.sleep(remaining)

for count in range(test_time):
    time.sleep(1)

end = time.perf_counter()
elapsed = end - start
print(f'Drifted by {abs(test_time-elapsed)}')