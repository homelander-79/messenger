# Messenger Application

## Overview
This Messenger Application is a multi-threaded Python program that allows users to communicate in real-time through text messages. It utilizes SQLite3 for database management, ensuring data persistence and efficient storage.

## Features
- **Real-time Messaging**: Users can send and receive messages instantly.
- **User Authentication**: Secure login system to ensure only authorized users can access the application.
- **SQLite3 Database**: Efficient storage and management of user data and messages.
- **Multi-threaded Design**: Utilizes threading to handle multiple client connections concurrently, improving performance and scalability.
- **Command Line Interface (CLI)**: Simple and intuitive interface for ease of use.

## Requirements
- Python 3.x
- SQLite3

## Installation
1. Clone this repository:
   ```
   [git clone https://github.com/yourusername/messenger.git](https://github.com/homelander-79/messenger)
   ```
2. Navigate to the project directory:
   ```
   cd messenger
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the server:
   ```
   python server.py
   ```
2. Run the client:
   ```
   python client.py
   ```
3. Follow the prompts to log in or create a new account.
4. Start messaging with other users!

## Configuration
- **Database Configuration**: Modify the database configuration in `config.py` if necessary.
- **Server Configuration**: Adjust server settings such as host and port in `server.py`.
- **Client Configuration**: Modify client settings in `client.py` if needed.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Special thanks to the developers of Python, SQLite3, and any other libraries or frameworks used in this project.

## Troubleshooting
- If you encounter any issues, please check the [Troubleshooting](docs/TROUBLESHOOTING.md) document for common problems and solutions.

---

Feel free to customize this template according to your project's specific details and requirements!
