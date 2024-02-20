import subprocess

subprocess.run(["pip", "install", "discord.py", "accuweather", "urbandictionary_top", "requests", "--break-system-packages"])

TOKEN = input("Enter your Discord bot token: ")

with open("main.py", "r") as file:
    main_content = file.read()

main_content = main_content.replace("BOT_TOKEN", TOKEN)

with open("main.py", "w") as file:
    file.write(main_content)

print("All done! Your bot will start now. ")
subprocess.run(["python3", "main.py"])
