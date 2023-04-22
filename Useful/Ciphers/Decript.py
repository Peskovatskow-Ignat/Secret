import os
import sys
import pyAesCrypt

directory = os.getcwd()
password = "123"


def decrypt(file):
    print("-" * 80)
    password_str = str(password)
    buffer_size = 512 * 1024
    pyAesCrypt.decryptFile(str(file), str(os.path.splitext(file)[0]), password_str, buffer_size)
    print("[Decrypt] '" + str(os.path.splitext(file)[0]) + "'")
    os.remove(file)


def walk(directory):
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            try:
                decrypt(path)
            except Exception as e:
                print(f"Error: {e}")
                pass
        else:
            walk(path)


walk(directory)
print("-" * 80)
os.remove("Decript.exe")

