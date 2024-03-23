# Project

The project is a simple word game in which the player is given a random set of letters to construct a word with. When the player constructs a word that is found in the database, they will receive score equal to the length of the word ^ 2, and new letters will be arranged. There will be 11 letters given, and the player can press reroll button to gain new letters with progressively increasing penalty.

The player gets a number of attempts to come up with as many words as is possible (rerolls do not subtract), after which the game ends and the player has their game recorded into the highscores which will be displayed to everybody. It is also possible to inspect the record of the game, along with both the letters, rerolls and the guessed word.

The player can also leave messages on the message board when they are logged in should they wish to communicate with other players.

# Configuration

1. Create your database for psql using the name you like. I used "tikawebdb"
2. Create .env file in the project root folder (where app.py is)
3. Insert "SECRET_KEY=[your-key]"
4. Insert "DATABASE_URL=postgresql://[your-username]:[your-password]@localhost/[name-of-the-database]"

# Word system

Only words found in the data/wordlist.txt will be compared against. Words that are invalid are either modified or removed.

- Words with 2 or less length are removed
- Words with special letters are removed (Only english alphabets allowed!)
- Words with whitespace are corrected
- Words with capital letters are converted to lower case

The original file will be adjusted based on this! If you wish to add your own words to quickly adjust the database based on your needs, these are how the words will be filtered out from the txt file, The original file will be modified!

# Scoring

Correct word will score (Length of the word - 2) ^ 2. A correct word must be:
- Length 3 or more
- Is found
- Can be made with the given letters
Successful word check will automatically reroll.

Skip reroll penalty: Each reroll costs 3 * the amount of rerolls taken in the game, note that this only applies if you press the reroll button itself, the success rerolls do not deduct from points!

# Course Requirements & What this project offers

- The website has been made with flask
- Contains 5 tables
    - Score, used to store score of games and to display them on the highscores
    - User, self-explanatory
    - GameRound, used to store the flow of the game by containing a list of guesses (can find them linked in the highscores)
    - Guess, contains information on what the player guessed (or rerolled) and the letters they had. Useful to check how well someone might've played in the highscores
    - Message, contains messages from users displayed in the front page, almost like a chat.
- Uses SQL queries to handle functionalities between the website and the database
