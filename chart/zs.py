import ssl
# print(ssl.get_default_verify_paths())

ssl._create_default_https_context = ssl._create_unverified_context