import os, shutil, zipfile, stat

def main():
    if os.path.exists("textfile.txt"):
        src = os.path.realpath("textfile.txt")
        dst = src + ".bak"
        shutil.copy(src, dst)

        if not os.path.exists("newtextfile.txt.bak"):
            os.rename("textfile.txt.bak", "newtextfile.txt.bak")

        #root_dir, filename = os.path.split(src)
        #shutil.make_archive("archive", "zip", root_dir) # zip directory

        with zipfile.ZipFile("testzip.zip", "w") as newzip: # Put a specific file in the archive
            newzip.write("loop.py")

        print(os.path.getsize(os.path.split(src)[0]))
        print(os.stat(os.path.split(src)[0]).st_size)
        print(os.stat('deps').st_size)
        print(sum(os.path.getsize(os.path.join('deps', file)) for file in os.listdir('deps') if file.endswith('.txt')))

if __name__ == "__main__":
    main()

