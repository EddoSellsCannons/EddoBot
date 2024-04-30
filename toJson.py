text = """Take a photo from the top floor of the Melbourne State Library to the ground.
Ride 5 different free trams
Take a photo of Southern Cross Station Platform 1
Take a photo of any Gaming Console in Big W in QV Village
Purchase someone a gift (Send who you are giving it to)
Purchase food worth over $15 and eat all of it.
Take a photo of the Chinatown Arches (Main entrance)
Take a photo of any physical Pokemon Merch (Including Plush, keychain, poster etc.)
Take a photo of any Gentleman’s club (Strip Club) or Adult store (Or anything adult based)
Purchase any Drink from any store for each member of your team
Win a game from any claw/skill tester machine
Take a photo of the Marvel Stadium sign
Take a picture of a Clocktower pointing between 6 and 7
Take a picture of the Street Sign displaying the name: “Russell Street”
Play a game of Chess against a stranger outside the State Library Melbourne
Take a picture of any monument/statue
Take a photo of Beanley Lane Street Art
Take a photo of any item worth more than $500 with price tag
Take a photo of any water fountain/water sprinkler
Take a photo of any empty parking spot
Take a photo of any physical boat
Take a photo of any physical Anime Merch (Figure, Poster etc.)
Buy any Ice Cream from any shop
Buy anything that is majority Pink or Orange.
Buy anything that is majority red or grey
Visit and use any Public Restroom
Take a photo of exactly 10 birds in a single photo
Buy, take a photo and consume any cookie
Take a photo of any establishment that is also available in Sydney/NSW
Take a photo of any pet
Take a photo of any item that is priced lower than $1 (AUD)
Take a photo of any non-english word
Take a photo of anything from Riot Games (Any picture, figure etc.)
Take a photo of any Ruler or Measuring Tape
Take a photo of any street performer
Take a photo of a Big W, Woolworths & Coles(Send separate 3 photos)
Take a photo of the word “Respect” or “Authority” on anything
Take a photo of Flinders Street Railway Station Entrance
Take a photo of anything Fortnite (Does not include collabs like Naruto)
Take a photo of any phone number or email address containing 3 consecutive numbers or letters
Receive a gift from another team (In chat) or do google coin flip until you hit heads 3 times in a row."""

textSplit = text.split("\n")
ls = []
for t in textSplit:
    t = "{\"name\":\"" + t + "\"}"
    ls.append(t)
print(str(ls).replace("\'", ""))