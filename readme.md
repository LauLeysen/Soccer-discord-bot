
# Football Match Data Bot

This is a Discord bot designed to provide live football match data. It fetches information from a custom API and updates users in real-time about ongoing, upcoming, and finished matches. The bot is built using the `discord.py` library.

## Features

- **Ping Command**: Responds with "Pong!" to check if the bot is active.
- **Purge Command**: Deletes a specified number of messages in the channel.
- **Live Matches**: Displays all live matches with scores and times.
- **Upcoming Matches**: Shows all upcoming matches.
- **Finished Matches**: Lists all finished matches with results.
- **Match by Team**: Retrieves live match details for a specified team.
- **Live Score Updates**: Periodically updates live match scores in a designated channel.

## Requirements

- Python 3.11.4
- `discord.py` library
- `aiohttp` library
- `.env` file with the following variables:
  - `DISCORD_TOKEN`: Your Discord bot token.
  - `BASE_URI`: The base URL of your API.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/football-match-data-bot.git
   cd football-match-data-bot
   ```

2. Create a virtual environment and activate it (*optional*):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your environment variables:
   ```
   DISCORD_TOKEN=your_discord_token
   BASE_URI=your_api_base_url
   ```

5. Run the bot:
   ```sh
   python bot.py
   ```

## Commands

- **`/ping`**: Replies with "Pong!".
- **`/purge <limit>`**: Deletes the specified number of messages in the channel. Use "all" to delete all messages.
- **`/live`**: Displays all live matches.
- **`/upcoming`**: Shows all upcoming matches.
- **`/finished`**: Lists all finished matches.
- **`/match <team>`**: Retrieves live match details for the specified team.
- **`/start_updates`**: Starts updating live match scores in the current channel.

## Background Task

The bot includes a background task that periodically updates live match scores in the specified channel every 10 seconds. It also sends notifications when scores change or matches end, mentioning a role named `pinglive` if it exists.

## API and Data Scraping

The bot relies on an external API for match data. The API and the data scraping mechanism are implemented in the following repositories:

- **API**: [football-api](https://github.com/MrSopia/football-api)
- **Data Scraping**: [livescore-scraper](https://github.com/MrSopia/livescore-scraper)

Ensure that the API is up and running, and the data scraper is populating the API with live match data.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to the authors of the [football-api](https://github.com/MrSopia/football-api) and [livescore-scraper](https://github.com/MrSopia/livescore-scraper) repositories for providing the data sources.
