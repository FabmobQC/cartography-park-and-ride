import os
import pandas as pd
import math

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
                fields = line.split(',')
                if fields[1] != '0' or fields[2] != '0':
                    data += f"{network},{line}"
    with open('output.csv', 'a') as f:
        f.write(data)

# Print warnings for data which is part of different networks and very close (suggesting duplication)
col_names = ['network', 'name', 'spaces_bikes', 'spaces_cars', 'latitude', 'longitude']
df = pd.read_csv('output.csv', names=col_names)
other_network_values = {}
last_network = ''
close_pairs = []
for row in df.sort_values(by=['network']).itertuples():
    if last_network != row.network:
        last_network = row.network
        other_network_values = df[df['network'] != row.network]
    for other in other_network_values.itertuples():
        distance = math.sqrt(
            math.pow(row.latitude - other.latitude, 2) +
            math.pow(row.longitude - other.longitude, 2)
        )
        if distance <= 0.005:
            if f"{other.network}:{other.name}-{row.network}:{row.name}" not in close_pairs:
                close_pairs.append(f"{row.network}:{row.name}-{other.network}:{other.name}")
                print(f"{row.network}:{row.name} CLOSE TO {other.network}:{other.name}")
                print(f"   {row.latitude},{row.longitude} - {other.latitude},{other.longitude}")
