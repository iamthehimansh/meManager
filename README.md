# Me Manager

An advanced AI personal assistant designed to manage professional communications and optimize job search efforts.

## Features

- Email management and prioritization
- Job application tracking
- Professional network optimization
- Career development suggestions
- Information retrieval and analysis
- Communication optimization

## Components

- `server/`: Backend Python scripts
  - `ai.py`: Core AI logic and function calling
  - `functions.py`: Utility functions for various tasks
  - `main.py`: Flask server for handling requests
  - `vectorDb.py`: Vector database operations
- `mail/`: Email processing
  - `pool.js`: IMAP client for email retrieval and processing

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   npm install
   ```

2. Set up environment variables:
   - `EMAIL`: Your email address
   - `PASSWORD`: Your email password

3. Start the Flask server:
   ```
   python server/main.py
   ```

4. Run the email processing script:
   ```
   node mail/pool.js
   ```

## Usage

The AI assistant processes incoming emails and direct messages, providing intelligent responses and actions based on the content.

- Incoming emails are automatically processed and analyzed.
- Direct messages can be sent to the `/direct_message` endpoint for AI processing.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request for any improvements or bug fixes.

## License

[MIT License](LICENSE)
