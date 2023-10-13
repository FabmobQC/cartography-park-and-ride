import os

# Reset existing file
with open('output.csv', 'w') as f:
    f.write('')

# Combine data
for file in os.listdir('network-data'):
    data = ''
    network = file.split('.')[0]
    with open(f"network-data/{file}", 'r') as f:
        for line in f:
            if len(line.strip()) != 0:
                data += f"{network},{line}"
    with open('output.csv', 'a') as f:
        f.write(data)
