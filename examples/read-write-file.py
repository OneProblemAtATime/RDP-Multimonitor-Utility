def main():
    myfile = open("textfile.txt", "w+") # write and create if it does not exist

    for i in range(10):
        myfile.write("This is some text\n")

    myfile.close()

def append_to_file():
    myfile = open("textfile.txt", "a+") # append and create if it does not exist

    for i in range(10):
        myfile.write("(This is some text)\n")

    myfile.close()

def read_from_file():
    myfile = open("textfile.txt", "r") # append and create if it does not exist

    if myfile.mode == "r":
        #contents = myfile.read()
        content_list = myfile.readlines()
        print(content_list[6], end="")


    #myfile.close() #reading a file does not require closing the file

if __name__ == "__main__":
    append_to_file()