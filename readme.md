# Project

The project is a simple word game in which the player is given a random set of letters to construct a word with. When the player constructs a word that is found in the database, they will receive score equal to the length of the word ^ 2, and new letters will be arranged. There will be 11 letters given, and the player can press reroll button to gain new letters with progressively increasing penalty.

The player gets a number of attempts to come up with as many words as is possible (rerolls do not subtract), after which the game ends and the player has their game recorded into the highscores which will be displayed to everybody. It is also possible to inspect the record of the game, along with both the letters, rerolls and the guessed word.

The player can also leave messages on the message board when they are logged in should they wish to communicate with other players.

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
