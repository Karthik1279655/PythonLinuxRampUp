import multiprocessing as mp

# Define the shared memory variable
shared_var = mp.Value('i', 0)


# Define the test function
def test_func(shared_var):
    # Access the shared memory variable
    shared_var.value += 1
    print(f"Test function: Shared variable value = {shared_var.value}")


# Create a new process and start the test function
p = mp.Process(target=test_func, args=(shared_var,))
p.start()

# Wait for the process to finish
p.join()

# Print the final value of the shared memory variable
print(f"Main function: Shared variable value = {shared_var.value}")
