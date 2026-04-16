print("\n--- Cihazın yaddaşında olan bütün dəyişənlər və datalar ---")

# Sadəcə sadə dəyişənləri çap edirik
device_data_list = []

# Sadə dəyişənləri sadalayırıq
for key, value in globals().items():
    # Modulları və funksiyaları atlayırıq
    if not key.startswith('__') and not isinstance(value, object):
        device_data_list.append((key, value))

# Dataları çap edirik
if not device_data_list:
    print("Cihazda heç bir data tapılmadı.")
else:
    for key, value in device_data_list:
        print(f"{key}: {value}")
        
        
