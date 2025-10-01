# 🎮 Discord Status Rotator

A beautiful Python application that automatically rotates your Discord status, emojis, HypeSquad house, and bio with a stunning purple-themed interface.

![Discord Status Rotator](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## ✨ Features

- 🔄 **Automatic Status Rotation**: Cycles through custom status messages
- 😀 **Emoji Rotation**: Changes emojis with your status
- 🏆 **HypeSquad Rotation**: Automatically switches between Discord HypeSquad houses
- 📝 **Bio Rotation**: Rotates your Discord profile bio
- ⚡ **System Usage Display**: Shows CPU and RAM usage in your status
- 🎨 **Beautiful Purple Theme**: Modern, elegant interface
- 📊 **Progress Tracking**: Visual progress bars and counters
- ⚙️ **Highly Configurable**: Customize rotation speeds, intervals, and behavior

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Discord account with a valid user token

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Discord-Status-Changer.git
   cd Discord-Status-Changer
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your Discord token**
   - Open Discord in your browser
   - Press `F12` to open Developer Tools
   - Go to `Network` tab
   - Send a message in any channel
   - Look for requests to `discord.com/api`
   - Find the `Authorization` header in the request headers
   - Copy the token (it starts with your user ID)

4. **Configure the application**
   - Copy `config.example.json` to `config.json`
   - Edit `config.json` and add your Discord token
   - Customize other settings as needed

5. **Add your statuses and emojis**
   - Edit `text.txt` with your custom status messages
   - Edit `emojis.txt` with your preferred emojis
   - Optionally edit `aboutme.txt` for bio rotation

6. **Run the application**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
Discord-Status-Changer/
├── main.py                 # Main application file
├── config.json            # Configuration file (create from example)
├── config.example.json    # Example configuration
├── text.txt              # Status messages (one per line)
├── emojis.txt            # Emojis to rotate (one per line)
├── aboutme.txt           # Bio messages for rotation (optional)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## ⚙️ Configuration

### config.json

```json
{
  "token": "YOUR_DISCORD_TOKEN_HERE",
  "status_sequence": ["online", "idle", "dnd"],
  "clear_enabled": false,
  "clear_interval": 15,
  "speed_rotator": 15,
  "use_status_sequence": true,
  "emoji_rotation_mode": "with_text",
  "hypesquad_sequence": ["bravery", "brilliance", "balance"],
  "hypesquad_mapping": {
    "bravery": 1,
    "brilliance": 2,
    "balance": 3
  },
  "rotate_hypesquad": false,
  "hypesquad_rotation_interval": 60,
  "rotate_aboutme": false,
  "aboutme_rotation_interval": 60,
  "show_system_usage": true,
  "system_usage_as_status": true
}
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `token` | Your Discord user token | Required |
| `speed_rotator` | Seconds between status changes | 15 |
| `status_sequence` | Discord status types to rotate | ["online", "idle", "dnd"] |
| `use_status_sequence` | Enable status type rotation | true |
| `emoji_rotation_mode` | How emojis rotate ("with_text" or "after_text_cycle") | "with_text" |
| `rotate_hypesquad` | Enable HypeSquad house rotation | false |
| `rotate_aboutme` | Enable bio rotation | false |
| `show_system_usage` | Display CPU/RAM in console | true |
| `system_usage_as_status` | Use system stats as status text | true |
| `clear_enabled` | Clear console periodically | false |
| `clear_interval` | Updates before clearing console | 15 |

## 📝 File Formats

### text.txt
```
Playing some games! 🎮
Listening to music 🎵
Working on projects 💻
Chilling with friends 👥
Coding something cool 🚀
```

### emojis.txt
```
🎮
🎵
💻
👥
🚀
```

### aboutme.txt
```
Software Developer | Gaming Enthusiast
Always learning something new
Coffee powered ☕
```

## 🎨 Emoji Formats

The application supports two emoji formats:

1. **Unicode Emojis**: Just the emoji character
   ```
   🎮
   🎵
   💻
   ```

2. **Custom Discord Emojis**: `name:id` format
   ```
   custom_emoji:1234567890123456789
   another_emoji:9876543210987654321
   ```

## 🔧 Advanced Features

### System Usage Integration
When `system_usage_as_status` is enabled, the bot alternates between:
- Custom status messages
- System usage display (CPU and RAM percentages)

### HypeSquad House Rotation
Rotate between Discord's HypeSquad houses:
- **Bravery** (House 1)
- **Brilliance** (House 2) 
- **Balance** (House 3)

### Bio Rotation
Automatically change your Discord profile bio with custom messages.

## 🛠️ Dependencies

Create a `requirements.txt` file with:

```
requests>=2.25.1
colorama>=0.4.4
psutil>=5.8.0
```

Install with:
```bash
pip install -r requirements.txt
```

## ⚠️ Important Notes

### Token Security
- **Never share your Discord token** - it provides full access to your account
- **Don't commit your token** to version control
- **Use config.json** (not config.example.json) for your actual token
- Consider using environment variables for production use

### Rate Limiting
- Discord has API rate limits
- The default 15-second interval is safe
- Don't set intervals below 5 seconds

### Account Safety
- This tool uses Discord's official API
- It's safe to use with your main account
- Always keep your token secure

## 🚨 Troubleshooting

### Common Issues

**"Invalid token" error**
- Make sure your token is correct and not expired
- Ensure the token is in the `config.json` file (not the example)

**"Integer modulo by zero" error**
- Make sure `text.txt` and `emojis.txt` have content
- Check that files aren't empty or contain only blank lines

**Status not updating**
- Check your internet connection
- Verify the token is valid
- Ensure you're not rate limited

**Emojis not showing**
- Use Unicode emojis or proper Discord custom emoji format
- Check that emoji names are correct

### Getting Help

1. Check that all files exist and have content
2. Verify your configuration is correct
3. Make sure your Discord token is valid
4. Check the console output for specific error messages

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

## 🔗 Links

- [Discord API Documentation](https://discord.com/developers/docs)
- [Python Requests Library](https://docs.python-requests.org/)
- [Colorama Documentation](https://pypi.org/project/colorama/)

---

**⚠️ Disclaimer**: This tool is for educational purposes. Use responsibly and in accordance with Discord's Terms of Service.
