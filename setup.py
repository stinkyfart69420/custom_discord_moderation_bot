# config.py
import subprocess

subprocess.run(["pip", "install", "discord.py", "accuweather", "urbandictionary_top", "requests", "--break-system-packages"])

TOKEN = input("Enter your Discord bot token: ")

# Read the main.py file content
with open("main.py", "r") as file:
    main_content = file.read()

# Replace "BOT_TOKEN" with the actual token
main_content = main_content.replace("BOT_TOKEN", TOKEN)

# Write the modified content back to main.py
with open("main.py", "w") as file:
    file.write(main_content)

print("All done! Your bot will start now. ")
subprocess.run(["python3", "main.py"])
