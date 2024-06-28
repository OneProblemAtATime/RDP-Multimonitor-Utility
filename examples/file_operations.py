import os, datetime, time

def main():
    print(os.name)
    print("Item existes:", str(os.path.exists("textfile.txt")))
    print("Isfile: ", os.path.isfile("textfile.txt"))
    print("Item is a directory: ", os.path.isdir("textfile.txt"))

    print("Item's path:", os.path.realpath("textfile.txt"))
    print("Item path and filename: ", os.path.split(os.path.realpath("textfile.txt")))
    #os.path.split(os.path.realpath("textfile.txt"))[-1] is the file name

    t = time.ctime(os.path.getmtime("textfile.txt"))
    print(t)
    print(datetime.datetime.fromtimestamp(os.path.getmtime("textfile.txt")))

    td = datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime("textfile.txt"))
    print("It has been", td.total_seconds(), "since the last modification.")

if __name__ == "__main__":
    main()