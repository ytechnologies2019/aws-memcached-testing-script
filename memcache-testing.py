import pylibmc
import string
import random
import time

def random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Replace 'your-cluster-endpoint' with your actual Memcached cluster endpoint
memcached_endpoint = 'demo-cache.mseyjw.0001.use1.cache.amazonaws.com:11211'

# Create a connection to the Memcached server
client = pylibmc.Client([memcached_endpoint], binary=True,
                        behaviors={"tcp_nodelay": True, "ketama": True})

# Insert a large number of keys into the cache
num_keys = 100000  # Number of keys to insert
value_size = 1000  # Size of each value in bytes

print(f"Starting to insert {num_keys} keys with value size of {value_size} bytes each...")

for i in range(num_keys):
    key = f"key_{i}"
    value = random_string(value_size)
    client.set(key, value)

    if i % 1000 == 0:
        print(f"Inserted {i} keys")

print("Insertion completed!")

# Retrieve some of the keys to verify they are stored
print("Verifying some keys...")
for i in range(0, num_keys, num_keys // 10):
    key = f"key_{i}"
    value = client.get(key)
    if value:
        print(f"Key {key} is in the cache.")
    else:
        print(f"Key {key} has been evicted.")

print("Verification completed!")
