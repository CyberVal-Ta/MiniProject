# This is project Little Wolf

A tiny desktop companion that asks how your day was and gives you a little love!

![screenshot](ProjectImages/HappyWolf.png)

## what it does?

- it will ask for your name and birthday and remembers it
- asks how your day was (good/okay/bad)
- responds with a random, personalised message and a little heart! </3
- with different wolf expressions for each mood
- it will also remember your birthday and celebrates it!

## why did I make this?
This is a small project for me to improve my programming but also a birthday present for my best friend!  

## how does it run from
```bash
pip install -r requirements.txt
python Wolfapp.py
```

## Build the .exe (windows)

```bash
pyinstaller --onefile --windowed --add-data "ProjectImages;ProjectImages" --name LittleWolf wolf_app.py
```

The '.exe' will appear in the 'dist/LittleWolf.exe"
- this is so that the windows will show a smart screen warning the first time cause the exe isnt code signed 

Click **More info → Run anyway**

## how to use?
How to use

1. Click the **⚙ gear** in the top-left corner
2. Enter your name and birthday (MM-DD, e.g. `04-15`)
3. Pick your colours
4. Click **Save**

## images

All images are made by me and are inspired by my friends character!

Also put the pngs into ProjectImages/
These include:
- HappyWolf.png
- SadWolf.png
- NormalWolf.png

They should be avaliable on my gitHub! or if you dont have them 
Don't have images? Want to use your own?

Custom images:

Replace the three PNGs in `ProjectImages/`:
- `NormalWolf.png`
- `HappyWolf.png`
- `SadWolf.png`

Aim for **400×400 or larger** PNGs with transparency.

 ## Settings

Click the ⚙ button in the corner of the wolf window to change your
name or birthday at any time.

# I hope you enjoy this mini project!
By CyberV