# Echo Server with Gradio UI

A responsive web application built with Gradio that echoes back any message you send to it.

## Features

- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- 🌐 **Network Access**: Accessible over LAN/WAN from other devices
- 🎨 **Modern UI**: Clean and intuitive interface with a soft theme
- ⌨️ **Keyboard Support**: Press Enter in the textbox to submit
- 🔄 **Real-time Echo**: Instantly displays your message back as a server response

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```bash
   python app.py
   ```

2. **Access the application:**
   - **Local access**: http://localhost:7860
   - **Network access**: http://[YOUR_IP_ADDRESS]:7860
   
   The application will automatically open in your default browser.

3. **Find your IP address** (to access from other devices):
   - **macOS/Linux**: `ifconfig | grep inet`
   - **Windows**: `ipconfig`

## How it Works

1. Enter any text in the input textbox
2. Click the "Echo Message" button (or press Enter)
3. The server will respond with the exact same message
4. The response appears in the "Server Response" section

## Network Configuration

The application is configured to:
- Listen on all network interfaces (`0.0.0.0`)
- Use port `7860` (Gradio default)
- Accept connections from any device on your network

### Firewall Considerations

If you can't access the app from other devices, you may need to:
- Allow port 7860 through your firewall
- Check your router's settings for internal network access

## Customization

You can modify the application by editing `app.py`:
- Change the port by modifying the `server_port` parameter
- Customize the UI theme and styling in the CSS section
- Add more complex processing logic in the `echo_message` function

## Technologies Used

- **Gradio**: Web UI framework for machine learning and general applications
- **Python**: Backend logic and server
- **HTML/CSS**: Responsive design and styling

## License

This project is open source and available under the MIT License.
