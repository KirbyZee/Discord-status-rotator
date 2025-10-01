import json
import os
import time
import requests
from colorama import Fore, init
import psutil


def get_system_usage():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    return cpu, ram


def read_file_lines(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]


def get_user_info(token):
    header = {'authorization': token}
    r = requests.get("https://discord.com/api/v10/users/@me", headers=header)
    if r.status_code == 200:
        return r.json()["username"], True
    return "Invalid token", False


def read_emojis(file_name):
    emojis = []
    for line in read_file_lines(file_name):
        parts = line.split(":")
        if len(parts) == 2 and parts[1].isdigit():
            emojis.append({"name": parts[0], "id": parts[1]})
        else:
            emojis.append({"name": line, "id": None})
    return emojis


def change_status(token, message, emoji_name, emoji_id, new_status, hypesquad=None):
    header = {'authorization': token}
    payload = {"custom_status": {"text": message}}
    
    if new_status:
        payload["status"] = new_status
    
    if emoji_id:
        payload["custom_status"].update({"emoji_name": emoji_name, "emoji_id": emoji_id})
    else:
        payload["custom_status"]["emoji_name"] = emoji_name
    
    if hypesquad:
        payload["hypesquad"] = hypesquad
    
    r = requests.patch("https://discord.com/api/v10/users/@me/settings", headers=header, json=payload)
    return r.status_code == 200


def change_hypesquad(token, hypesquad_type):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    body = {"house_id": hypesquad_type}
    response = requests.post('https://discord.com/api/v10/hypesquad/online', headers=headers, json=body)
    
    if response.status_code == 204:
        print('Hypesquad successfully changed!')
        return True
    
    print('Error when changing Hypesquad.')
    return False


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_config():
    with open("config.json", "r") as file:
        return json.load(file)


def color_text(text, color_code):
    return f"{color_code}{text}{Fore.RESET}"


def print_banner():
    banner = f"""
{Fore.MAGENTA}╔═══════════════════════════════════════════════════════════════╗
║                     Discord Status Rotator                     ║
║                           by Kirby                              ║
╚═══════════════════════════════════════════════════════════════╝{Fore.RESET}
"""
    print(banner)


def print_status_change(time_formatted, token_colored, status_colored, emoji_name, hypesquad, bio, 
                       current_status, status_count, total_statuses, show_system_usage=False):
    separator = f"{Fore.MAGENTA}{'─' * 65}{Fore.RESET}"
    print(separator)
    print(f"{Fore.LIGHTMAGENTA_EX}⏰ Time:{Fore.RESET} {time_formatted}")
    print(f"{Fore.LIGHTBLUE_EX}👤 User:{Fore.RESET} {token_colored}")
    print(f"{Fore.CYAN}💬 Status:{Fore.RESET} {status_colored}")
    print(f"{Fore.MAGENTA}😀 Emoji:{Fore.RESET} {color_text(emoji_name, Fore.LIGHTMAGENTA_EX)}")
    print(f"{Fore.LIGHTMAGENTA_EX}🏆 HypeSquad:{Fore.RESET} {color_text(hypesquad, Fore.LIGHTBLUE_EX)}")
    print(f"{Fore.LIGHTMAGENTA_EX}📝 Bio:{Fore.RESET} {color_text(bio[:30] + '...' if len(bio) > 30 else bio, Fore.WHITE)}")
    print(f"{Fore.MAGENTA}🔮 Discord Status:{Fore.RESET} {color_text(str(current_status), Fore.LIGHTMAGENTA_EX)}")
    print(f"{Fore.LIGHTMAGENTA_EX}📊 Progress:{Fore.RESET} {color_text(f'{status_count % total_statuses + 1}/{total_statuses}', Fore.LIGHTCYAN_EX)}")
    
    # Progress bar
    progress = (status_count % total_statuses + 1) / total_statuses
    bar_length = 20
    filled_length = int(bar_length * progress)
    bar = f"{Fore.MAGENTA}{'█' * filled_length}{Fore.LIGHTBLACK_EX}{'░' * (bar_length - filled_length)}{Fore.RESET}"
    print(f"{Fore.LIGHTMAGENTA_EX}📈 Progress Bar:{Fore.RESET} {bar} {progress*100:.1f}%")
    
    # CPU + RAM if enabled
    if show_system_usage:
        cpu, ram = get_system_usage()
        print(f"{Fore.LIGHTMAGENTA_EX} CPU:{Fore.RESET} {color_text(str(cpu) + '%', Fore.LIGHTMAGENTA_EX)} "
              f"{Fore.LIGHTMAGENTA_EX}🖥️ RAM:{Fore.RESET} {color_text(str(ram) + '%', Fore.LIGHTBLUE_EX)}")


def print_rotation_message(time_formatted, rotation_type, value):
    icons = {
        "hypesquad": "🏆",
        "bio": "📝",
        "emoji": "😀"
    }
    icon = icons.get(rotation_type, "🔄")
    print(f"\n{Fore.LIGHTMAGENTA_EX}✨ {icon} {time_formatted} Rotating {rotation_type}: {color_text(value, Fore.LIGHTMAGENTA_EX)}{Fore.RESET}")


def print_error_message(error_type):
    error_messages = {
        "status": "❌ Error changing status",
        "hypesquad": "❌ Error changing HypeSquad",
        "bio": "❌ Error changing bio"
    }
    message = error_messages.get(error_type, "❌ Unknown error")
    print(f"{Fore.RED}{message}{Fore.RESET}")


def print_startup_info(user_info, is_valid_token):
    status_color = Fore.LIGHTMAGENTA_EX if is_valid_token else Fore.RED
    status_text = "✅ Valid" if is_valid_token else "❌ Invalid"
    
    print(f"\n{Fore.LIGHTMAGENTA_EX}🚀 Starting Discord Status Rotator...{Fore.RESET}")
    print(f"{Fore.LIGHTMAGENTA_EX}👤 Connected user:{Fore.RESET} {color_text(user_info, Fore.LIGHTBLUE_EX)}")
    print(f"{Fore.LIGHTMAGENTA_EX}🔑 Token:{Fore.RESET} {status_color}{status_text}{Fore.RESET}")
    print(f"{Fore.MAGENTA}{'─' * 50}{Fore.RESET}\n")


def print_configuration_info(config, total_statuses, total_emojis):
    print(f"{Fore.LIGHTMAGENTA_EX}⚙️ Current configuration:{Fore.RESET}")
    print(f"{Fore.LIGHTMAGENTA_EX} • Rotation speed:{Fore.RESET} {config['speed_rotator']} seconds")
    print(f"{Fore.LIGHTMAGENTA_EX} • Total statuses:{Fore.RESET} {total_statuses}")
    print(f"{Fore.LIGHTMAGENTA_EX} • Total emojis:{Fore.RESET} {total_emojis}")
    print(f"{Fore.LIGHTMAGENTA_EX} • Emoji mode:{Fore.RESET} {config.get('emoji_rotation_mode', 'with_text')}")
    
    clear_status = ('✅ Every ' + str(config.get('clear_interval', 15)) + ' updates' 
                   if config.get('clear_enabled', False) else '❌ Disabled')
    print(f"{Fore.LIGHTMAGENTA_EX} • Console clear:{Fore.RESET} {clear_status}")
    
    hypesquad_status = '✅ Enabled' if config.get('rotate_hypesquad', False) else '❌ Disabled'
    print(f"{Fore.LIGHTMAGENTA_EX} • HypeSquad rotation:{Fore.RESET} {hypesquad_status}")
    
    bio_status = '✅ Enabled' if config.get('rotate_aboutme', False) else '❌ Disabled'
    print(f"{Fore.LIGHTMAGENTA_EX} • Bio rotation:{Fore.RESET} {bio_status}")
    print(f"{Fore.MAGENTA}{'─' * 50}{Fore.RESET}\n")


def change_bio(token, bio_text):
    url = 'https://discord.com/api/v10/users/@me/profile'
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    payload = {'bio': bio_text}
    response = requests.patch(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print('Bio successfully changed!')
        return True
    
    print('Error when changing bio.')
    return False


# Initialize colorama
init()


def main():
    config = load_config()
    token = config["token"]
    clear_enabled = config["clear_enabled"]
    clear_interval = config["clear_interval"]
    speed_rotator = config["speed_rotator"]
    status_sequence = config["status_sequence"]
    use_status_sequence = config["use_status_sequence"]
    emoji_rotation_mode = config.get("emoji_rotation_mode", "with_text")
    hypesquad_sequence = config.get("custom_hypesquad_sequence", config["hypesquad_sequence"])
    rotate_hypesquad = config.get("rotate_hypesquad", True)
    hypesquad_rotation_interval = config.get("hypesquad_rotation_interval", 60)
    rotate_aboutme = config.get("rotate_aboutme", True)
    aboutme_rotation_interval = config.get("aboutme_rotation_interval", 60)
    aboutme_sequence = read_file_lines("aboutme.txt") if rotate_aboutme else []
    
    # Filter out empty items and ensure sequences have content
    hypesquad_sequence = [item for item in hypesquad_sequence if item.strip()]
    aboutme_sequence = [item for item in aboutme_sequence if item.strip()]
    
    if rotate_hypesquad and not hypesquad_sequence:
        print(f"{Fore.LIGHTMAGENTA_EX}⚠️ HypeSquad rotation enabled but no valid HypeSquad items found{Fore.RESET}")
        rotate_hypesquad = False
    
    if rotate_aboutme and not aboutme_sequence:
        print(f"{Fore.LIGHTMAGENTA_EX}⚠️ Bio rotation enabled but no valid bio items found{Fore.RESET}")
        rotate_aboutme = False
    
    status_count = emoji_count = hypesquad_count = aboutme_count = 0
    next_hypesquad_time = next_aboutme_time = time.time()
    
    try:
        statuses = read_file_lines("text.txt")
        emojis = read_emojis("emojis.txt")
        
        # Filter out empty lines and ensure we have at least one item
        statuses = [status for status in statuses if status.strip()]
        emojis = [emoji for emoji in emojis if emoji.get("name", "").strip()]
        
        if not statuses:
            statuses = ["Default Status"]
            print(f"{Fore.LIGHTMAGENTA_EX}⚠️ No statuses found in text.txt, using default status{Fore.RESET}")
        
        if not emojis:
            emojis = [{"name": "🎮", "id": None}]
            print(f"{Fore.LIGHTMAGENTA_EX}⚠️ No emojis found in emojis.txt, using default emoji{Fore.RESET}")
            
    except Exception as e:
        print(f"{Fore.RED}❌ Error reading files: {e}{Fore.RESET}")
        print(f"{Fore.LIGHTMAGENTA_EX}💡 Make sure 'text.txt' and 'emojis.txt' files exist{Fore.RESET}")
        return
    
    user_info, is_valid_token = get_user_info(token)
    if not is_valid_token:
        print(f"{Fore.RED}❌ Invalid token. Exiting the program.{Fore.RESET}")
        return
    
    clear_console()
    print_banner()
    print_startup_info(user_info, is_valid_token)
    print_configuration_info(config, len(statuses), len(emojis))
    
    bio = aboutme_sequence[0] if rotate_aboutme and aboutme_sequence else "N/A"
    
    while True:
        try:
            current_status = status_sequence[status_count % len(status_sequence)] if use_status_sequence else None
            
            if config.get("system_usage_as_status", False):
                if status_count % 2 == 0:
                    cpu, ram = get_system_usage()
                    status = f" CPU: {cpu}% | 🖥 RAM: {ram}%"
                else:
                    status = statuses[status_count % len(statuses)]
            else:
                status = statuses[status_count % len(statuses)]
            
            time_formatted = color_text(time.strftime("%I:%M %p:"), Fore.LIGHTMAGENTA_EX)
            token_info = f"{token[:6]}****** | {user_info}"
            token_colored = color_text(token_info, Fore.LIGHTMAGENTA_EX if is_valid_token else Fore.RED)
            status_colored = color_text(status, Fore.LIGHTBLUE_EX)
            
            emoji = emojis[emoji_count % len(emojis)]
            emoji_name, emoji_id = emoji["name"], emoji["id"]
            current_time = time.time()
            hypesquad = "none"
            house_id = 0
            
            if rotate_hypesquad and current_time >= next_hypesquad_time:
                hypesquad = hypesquad_sequence[hypesquad_count % len(hypesquad_sequence)]
                house_id = config["hypesquad_mapping"].get(hypesquad.lower(), 0)
                print_rotation_message(time_formatted, "hypesquad", hypesquad)
                if not change_hypesquad(token, house_id):
                    print_error_message("hypesquad")
                hypesquad_count += 1
                next_hypesquad_time = current_time + hypesquad_rotation_interval
            
            if rotate_aboutme and current_time >= next_aboutme_time:
                bio = aboutme_sequence[aboutme_count % len(aboutme_sequence)]
                print_rotation_message(time_formatted, "bio", bio)
                if not change_bio(token, bio):
                    print_error_message("bio")
                aboutme_count += 1
                next_aboutme_time = current_time + aboutme_rotation_interval
            
            print_status_change(time_formatted, token_colored, status_colored, emoji_name, hypesquad, 
                               bio, current_status, status_count, len(statuses), 
                               show_system_usage=config.get("show_system_usage", False))
            
            if not change_status(token, status, emoji_name, emoji_id, current_status):
                print_error_message("status")
            
            status_count += 1
            
            if emoji_rotation_mode == "with_text":
                emoji_count += 1
            elif emoji_rotation_mode == "after_text_cycle" and status_count % len(statuses) == 0:
                emoji_count += 1
                print_rotation_message(time_formatted, "emoji", 
                                     f"Cycle completed - New emoji: {emojis[emoji_count % len(emojis)]['name']}")
            
            if clear_enabled and status_count % clear_interval == 0:
                time.sleep(speed_rotator)
                clear_console()
                print_banner()
            else:
                time.sleep(speed_rotator)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTMAGENTA_EX}⚠️ Program stopped by user.{Fore.RESET}")
            print(f"{Fore.LIGHTMAGENTA_EX}👋 Thanks for using Discord Status Rotator!{Fore.RESET}")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ An error occurred: {e}{Fore.RESET}")
            time.sleep(speed_rotator)


if __name__ == "__main__":
    main()