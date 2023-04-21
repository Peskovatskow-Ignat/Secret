import subprocess


def main():
    string = ""
    data = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("cp866").split("\n")
    Wi_Fis = [line.split(":")[1][1:-1] for line in data if "Все профили пользователей" in line]
    for Wi_fi in Wi_Fis:
        Wi_fi = Wi_fi.replace("-=", "").replace("=-", "")
        try:
            result = subprocess.check_output(["netsh", "wlan", "show", "profiles", Wi_fi, "key=clear"]).decode(
                "cp866").split("\n")
        except subprocess.CalledProcessError as e:
            continue
        result = [line.split(":")[1][1:-1] for line in result if "Содержимое ключа" in line]
        try:
            string += f"Имя сети: {Wi_fi}, password: {result[0] if result else 'no password'} \n"
        except IOError:
            continue
    return string


if __name__ == '__main__':
    main()
