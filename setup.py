import subprocess
import sys
import os

# __name__ = 'C.D.M.B'
__author__ = 'stinkyfart69420'

try:
    subprocess.call(["pip", "install", "-q", "-r", "requirements.txt", "--break-system-packages"], shell = False)

except Exception as e:
    print(e)
    exit()


def wrtie(l_content, content):

    reading_file = open("main.py", "r")

    new_file_content = ""
    for line in reading_file:
        new_line = line.replace(l_content, content)
        new_file_content += new_line
    reading_file.close()

    writing_file = open("main.py", "w")
    writing_file.write(new_file_content)
    writing_file.close()

if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1]== "--reset":

            # file_path = os.path.join("preMadeFiles", "_main.py")

            r_file = open("main_2.py", "r")
            contents = r_file.read()
            l_file = open("main.py", "w")
            l_file.seek(0)
            l_file.truncate()
            l_file.write(contents)
            l_file.close()
            r_file.close()

            print("reset completed!")

    else:

        bTOKEN = input("Enter your Discord bot token: ")

        API_KEY = input("Input your Accuweater API KEY(press enter if you dont have one!): ")

        wrtie("[TOKEN]", bTOKEN)

        if API_KEY != "":

            wrtie("[WeatherAPIKey]", API_KEY)

        print(f"Token: {bTOKEN}")

        if API_KEY!= "":

            print(f"API Key: {API_KEY}")

        print("All done! Your bot will start now. ")

        subprocess.call("python main.py", shell = True)