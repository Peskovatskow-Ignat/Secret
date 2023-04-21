from pytube import YouTube

link = input("Введите ссылку на видео: ")
try:
    video = YouTube(link)
except:
    print("Недействительная ссылка на видео.")
    exit()

print("Выберите качество (High/Low)")
quality = input("Выбор: (H/L): ").upper()

if quality == "H":
    output = video.streams.get_highest_resolution()
elif quality == "L":
    output = video.streams.get_lowest_resolution()
else:
    print("Некорректный выбор качества.")
    exit()

output.download(output_path='.', filename='video')
print("Загрузка завершена.")
