"""
Little Wolf! The tiny desktop companion
Asks how your day was and gives you a little love!

Run:       python wolf_app.py
Build exe: pyinstaller --onefile --windowed --add-data "ProjectImages;ProjectImages" --name LittleWolf wolf_app.py
"""

import tkinter as tk
from tkinter import colorchooser
import random
import os
import sys
import json
from datetime import datetime


# config stuff
FLOATING_PET    = True
USE_IMAGES      = True
ALWAYS_ON_TOP   = True
WOLF_IMAGE_SIZE = 220        # max dimension (aspect preserved)

# show a heart even during the greeting? if False, heart only appears after
# they pick a mood. if True, the space is never empty and nothing jumps.
HEART_ON_GREETING = False


IMG_NORMAL   = "ProjectImages/NormalWolf.png"
IMG_SAD      = "ProjectImages/SadWolf.png"
IMG_HAPPY    = "ProjectImages/HappyWolf.png"
IMG_QUESTION = "ProjectImages/QuestionWolf.png"

CONFIG_FILE = "config.json"

DEFAULT_THEME = {
    "bg":       "#182259",
    "bubble":   "#616eba",
    "text":     "#ffffff",
    "btn_bg":   "#2e3875",
    "btn_text": "#ffffff",
}


# messages!!
GREETINGS = [
    "How was your day, {name}?",
    "Hey {name}! How are you feeling?",
    "Hi {name}, how's your day going?",
    "Hello {name}! Tell me about your day — I'm nosy, get it? nosy!",
    "Hey {name}, how are you doing right nowww?",
    "What's up {name}, how was your day?",
    "Howl's it going, {name}?",
    "Howl do you do, {name}?",
    "Welcome back {name}! How was your day?",
    "Hey {name}, how are you feeling today?",
    "Hi {name}, how's your day been so far?",
    "What's good {name}! How are you doing today?",
    "Missed you today, {name}! How was your day?",
]

GREETINGS_NO_NAME = [
    "How was your day?",
    "Hey! How are you feeling?",
    "Hi, how's your day going?",
    "Hello! Tell me about your day — I'm nosy, get it? nosy!",
    "Hey, how are you doing right nowww?",
    "What's up, how was your day?",
    "Howl's it going?",
    "Howl do you do?",
    "Missed you today! How was your day?",
]

RESPONSES = {
    "good": [
        "That's great to hear! I'm so happy for you, {name}!",
        "Yay! I'm glad your day was good, {name}!",
        "Awesome! I'm happy to hear that, {name}!",
        "That's wonderful! I'm glad you had a good day, {name}!",
        "Fantastic! I'm so happy for you, {name}!",
        "Howl yeah! I'm glad your day was good, {name}!",
        "Howly moly! I'm happy to hear that, {name}!",
        "That's pawsome! I'm glad you had a good day, {name}!",
        "That's fur-tastic! I'm so happy for you, {name}!",
        "That's howling good news! I'm glad your day was good, {name}!",
        "That's fur-bulous! I'm glad you had a good day, {name}!",
        "That's paw-sitively wonderful! I'm so happy for you, {name}!",
        "That's howl-arious! I'm glad your day was good, {name}!",
        "That's fur-tunate! I'm happy to hear that, {name}!",
        "That's paw-some sauce! I'm glad you had a good day, {name}!",
    ],
    "okay": [
        "I'm glad to hear that your day was okay, {name}.",
        "That's good to hear, {name}. I'm glad your day was okay.",
        "I'm happy to hear that your day was okay, {name}.",
        "That's great to hear, {name}. I'm glad your day was okay.",
        "I'm glad your day was okay, {name}. That's good news.",
        "I hope your day gets even better, {name}. I'm glad it was okay.",
        "I hope your day improves, {name}. I'm glad it was okay.",
        "I'm glad your day was okay, {name}. That's a positive sign.",
        "May it get even better, {name}. I'm glad your day was okay.",
        "Can't wait for it to get even better, {name}. I'm glad your day was okay.",
        "Can't wait to see howl it gets even better, {name}. I'm glad your day was okay.",
    ],
    "normal": [
        "I see. I hope your day gets better, {name}.",
        "I understand. I hope your day improves, {name}.",
        "I hear you. I hope your day gets better, {name}.",
        "I get it. I hope your day improves, {name}.",
        "You're working hard, {name}. I hope your day improves.",
        "You're doing your best, {name}. I hope your day gets better.",
        "I know things can be tough, {name}. I hope your day improves.",
        "I'm rooting for you, {name}. I hope your day gets better.",
        "I'm proud of you, {name}. I hope your day improves.",
        "You did a great job today, {name}. I hope your day gets better.",
        "Keep up the good work, {name}. I hope your day improves.",
        "Sending you a heart, {name}.",
        "I wish I could hug you right now, {name}.",
    ],
}

BIRTHDAY_MESSAGES = [
    "Happy Birthday {name}!!! 🎉",
    "How was your birthday, {name}?",
    "I hope you had a wonderful day filled with love and joy! And HAPPY BIRTHDAYYYYY {name}!",
    "It's your birthday today, {name}! I hope you have a fantastic day filled with love and happiness!",
    "Wishing you a very happy birthday, {name}! May your day be filled with love, laughter, and all the things that make you happy!",
    "Happy Birthday, {name}! I hope your day is as special as you are.",
    "On your birthday, {name}, I want to remind you how much you mean to me. Happy Birthday!",
    "Happy Birthday, {name}! May this year bring you new adventures and all the love you deserve!",
    "I saved you a heart 💕! Happy birthday, {name}!",
]

# ok so this is the special nockai/nocky birthday stuff
# if theyre named nockai or nocky AND its their birthday, they get these instead
# i made them extra special for them cause they deserve it
NOCKAI_BIRTHDAY_MESSAGES = [
    "HAPPY BIRTHDAY NOCKAI!!! 🎉🎂 i saved you a WHOLE CAKE and i'm not even sharing it with anyone else ok it's all yours I genuinely don’t think I’ll ever be able to put into words just how much you mean to me, but I’m going to try anyway. You’re not just my best friend. You’ve become such a deeply important part of my life, someone who has been there through so many different versions of me, through the good days, the awful days, the moments where I felt completely lost, and the moments where I felt genuinely happy. And somehow, through all of it, you’ve stayed.",
    "NOCKAIIIII IT'S YOUR BIRTHDAY!!! 🎉 did you know you're literally the best?? cause you are. happy birthday!! I think one of the most beautiful things about our friendship is that you’ve seen me in moments where I wasn’t at my best and never made me feel like I had to become someone else to deserve your friendship. You’ve listened to me when I needed to talk, stayed when I needed someone beside me, made me laugh when I probably didn’t feel like laughing, and reminded me that I wasn’t alone even when I felt like I was.",
    "happy birthday nockai!!! 🎂🥳 i would howl for you but i'm too excited so here's a heart instead 💕 There are people who come into your life for a season, people you meet because your paths happen to cross, and then there are people who somehow become part of your story. You are one of those people for me. When I look back at everything we’ve been through, I honestly can’t imagine my life without all the memories, conversations, stupid jokes, late-night talks, random moments, and little things that somehow became some of my favourite memories.",
    "NOCKY!!! 🎉🎂 HAPPY BIRTHDAY you wonderful human!!! i hope today is as amazing as you are!! I hope you know that your presence in my life has mattered more than you probably realise. You’ve made difficult moments easier simply by being there. You’ve made good moments even better. And even when you probably thought you were doing something small, there have been so many times where your kindness, patience, or just having you there meant the world to me.",
    "ok so it's nockai's birthday today and i just want everyone to know how cool they are 🎉🎂 happy birthday!!! I’m so grateful that I get to call you my best friend. I’m grateful for every version of our friendship we’ve had and every version that’s still ahead of us. I hope that as we grow older, change, meet new people, and go through different chapters of life, we never forget how special this friendship has been to us. And no matter where life takes us, I want you to know that I’ll always be grateful that our paths crossed. Thank you for being my safe place, my person, my best friend, and someone I can always count on.",
    "NOCKAI HAPPY BIRTHDAYYYYYY!!!!! 🥳🎂🎉 you get ALL the hearts today 💕💕💕💕💕 On your birthday, I hope you remember how loved you are. Not just today, but every day. You deserve people who appreciate your heart, who listen to you, who celebrate you, and who stay when things aren't easy. I hope this next year gives you so many reasons to smile, so many memories that you’ll look back on years from now, and so many moments where you realise just how far you’ve come.",
    "howly moly it's nockai's birthday!!! 🎂🎉 i'm so happy you exist!!! happy birthday!!! I love you more than I probably say enough, and I hope you never forget how much you mean to me. Here’s to another year of us, and hopefully a lifetime of memories we haven’t even made yet. ",
]

HEARTS = ["❤️", "💛", "💚", "💙", "💜", "🖤", "🤍", "💖", "💗", "💓", "💕"]

# names that trigger the special birthday messages (case insensitive)
SPECIAL_BIRTHDAY_NAMES = ["nockai", "nocky"]


# loading and saving the config file
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Error saving config: {e}")


# for the exe — makes sure images load when its bundled up
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# render an emoji to a tkinter image so hearts show in colour (windows thing)
def emoji_to_image(emoji_char, size=64):
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageTk

        font = None
        for name in ["seguiemj.ttf", "Segoe UI Emoji", "Apple Color Emoji", "NotoColorEmoji.ttf"]:
            try:
                font = ImageFont.truetype(name, size)
                break
            except Exception:
                continue

        if font is None:
            return None

        canvas_size = size * 3
        img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((canvas_size // 2, canvas_size // 2),
                  emoji_char, font=font, embedded_color=True, anchor="mm")

        # crop tight so it centers properly
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)

        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"[emoji] render failed: {e}")
        return None


# is it their birthday today?
def is_birthday(birthday_str):
    if not birthday_str:
        return False
    try:
        today = datetime.now().strftime("%m-%d")
        return today == birthday_str.strip()
    except Exception:
        return False


# is this one of the special names that gets the extra special birthday stuff?
def is_special_birthday_name(name):
    if not name:
        return False
    return name.strip().lower() in SPECIAL_BIRTHDAY_NAMES


# the actual app
class WolfApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Little Wolf")

        self.cfg = load_config()
        self.theme = {**DEFAULT_THEME, **self.cfg.get("theme", {})}
        self.name = self.cfg.get("name", "")
        self.birthday = self.cfg.get("birthday", "")

        self.root.configure(bg=self.theme["bg"])

        if FLOATING_PET:
            self.root.overrideredirect(True)
            if ALWAYS_ON_TOP:
                self.root.attributes("-topmost", True)

        self.is_answered = False
        self.wolf_photo = None
        self.heart_photo = None

        self.root.bind("<ButtonPress-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)

        self.build_ui()
        self.refresh_greeting()

        # initial size + center on screen
        self.autosize(center=True)

    # resize the window to fit whats inside it
    def autosize(self, center=False):
        self.root.update_idletasks()

        w = self.card.winfo_reqwidth() + 20
        h = self.card.winfo_reqheight() + 20

        w = max(360, min(w, 620))
        h = max(400, min(h, 950))

        if center:
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            x = (sw - w) // 2
            y = (sh - h) // 2
        else:
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            if x + w > sw: x = sw - w - 20
            if y + h > sh: y = sh - h - 40
            if x < 0: x = 20
            if y < 0: y = 20

        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # build everythingggg
    def build_ui(self):
        t = self.theme

        self.card = tk.Frame(
            self.root, bg=t["bg"], bd=0,
            highlightthickness=1, highlightbackground="#616eba",
        )
        self.card.pack(fill="both", expand=True, padx=10, pady=10)

        # reserve the bottom FIRST so the reset button never gets pushed off
        bottom_area = tk.Frame(self.card, bg=t["bg"])
        bottom_area.pack(side="bottom", fill="x", pady=(6, 12))

        self.reset_btn = tk.Button(
            bottom_area, text="Reset", bg=t["btn_bg"], fg=t["btn_text"],
            font=("Calibri", 10), relief="flat", bd=0, cursor="hand2",
            activebackground=t["bubble"],
            padx=10, pady=5, command=self.reset,
        )
        self.reset_btn.pack()

        # close button (the little x)
        self.close_btn = tk.Label(
            self.card, text="X", bg=t["btn_bg"], fg=t["btn_text"],
            font=("Calibri", 10, "bold"), cursor="hand2", padx=5, pady=2,
        )
        self.close_btn.place(relx=1.0, rely=0.0, anchor="ne")
        self.close_btn.bind("<Button-1>", lambda e: self.root.destroy())

        # settings gear
        self.settings_btn = tk.Label(
            self.card, text="⚙", bg=t["btn_bg"], fg="#616eba",
            font=("Calibri", 10, "bold"), cursor="hand2", padx=5, pady=2,
        )
        self.settings_btn.place(relx=0.0, rely=0.0, anchor="nw")
        self.settings_btn.bind("<Button-1>", lambda e: self.open_settings())

        # the wolf!!
        self.wolf_label = tk.Label(
            self.card, bg=t["bg"], text="🐺",
            font=("Segoe UI Emoji", 50),
        )
        self.wolf_label.pack(pady=(20, 4))
        if USE_IMAGES:
            self.set_wolf_image(IMG_QUESTION)

        # speech bubble
        self.bubble = tk.Label(
            self.card, text="...", bg=t["bubble"], fg=t["text"],
            font=("Calibri", 12), wraplength=280, justify="center",
            bd=0, padx=10, pady=10,
            highlightthickness=1, highlightbackground="#616eba",
        )
        self.bubble.pack(pady=10, padx=10)

        # mood buttons
        btn_row = tk.Frame(self.card, bg=t["bg"])
        btn_row.pack(pady=10)

        self.buttons = []
        for label, mood in [("Good", "good"), ("Okay", "okay"), ("Normal", "normal")]:
            b = tk.Button(
                btn_row, text=label, bg=t["btn_bg"], fg=t["btn_text"],
                font=("Calibri", 10), relief="flat", bd=0,
                cursor="hand2", padx=10, pady=5,
                activebackground=t["bubble"],
                command=lambda m=mood: self.handle_mood(m),
            )
            b.pack(side="left", padx=5)
            self.buttons.append(b)

        # heart — no fixed height so it collapses when empty
        self.heart_label = tk.Label(
            self.card, text="", bg=t["bg"],
        )
        self.heart_label.pack(pady=(4, 0))

    # pick the greeting — birthday overrides but we still combine em
    def refresh_greeting(self):
        greeting = self._pick_greeting()
        if is_birthday(self.birthday):
            birthday_line = self.fill(self._pick_birthday_message())
            greeting_line = self.fill(greeting)
            msg = f"{birthday_line}\n\n{greeting_line}"
        else:
            msg = self.fill(greeting)
        self.set_bubble_text(msg)

        # greeting wolf = QuestionWolf
        if USE_IMAGES:
            self.set_wolf_image(IMG_QUESTION)

        # heart on greeting (optional, controlled by HEART_ON_GREETING)
        if HEART_ON_GREETING:
            self.show_heart()
        else:
            self.clear_heart()

    def _pick_greeting(self):
        pool = GREETINGS if self.name else GREETINGS_NO_NAME
        return random.choice(pool)

    # picks a birthday message — special one if theyre nockai or nocky!
    def _pick_birthday_message(self):
        if is_special_birthday_name(self.name):
            return random.choice(NOCKAI_BIRTHDAY_MESSAGES)
        return random.choice(BIRTHDAY_MESSAGES)

    def fill(self, text):
        if self.name:
            return text.replace("{name}", self.name)
        cleaned = (text
                   .replace(", {name}", "")
                   .replace(" {name}", "")
                   .replace("{name} ", "")
                   .replace("{name},", "")
                   .replace("{name}!", "")
                   .replace("{name}", ""))
        return cleaned.strip()

    def set_bubble_text(self, msg):
        wrap = max(220, self.card.winfo_width() - 40) if self.card.winfo_width() > 1 else 300
        self.bubble.config(text=msg, wraplength=wrap, justify="center")
        self.autosize()

    # draggin the wolf around
    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self.drag_start_x
        y = self.root.winfo_y() + event.y - self.drag_start_y
        self.root.geometry(f"+{x}+{y}")

    # load a wolf image, keeps the aspect ratio so they dont get squished
    def set_wolf_image(self, path):
        try:
            from PIL import Image, ImageTk
            full = resource_path(path)
            img = Image.open(full).convert("RGBA")
            img.thumbnail((WOLF_IMAGE_SIZE, WOLF_IMAGE_SIZE), Image.LANCZOS)

            self.wolf_photo = ImageTk.PhotoImage(img)
            self.wolf_label.config(image=self.wolf_photo, text="")
            self.autosize()
        except Exception as e:
            print(f"Error loading image: {e}")
            self.wolf_label.config(text="🐺", image="")

    # the little heart!!
    def show_heart(self):
        heart_char = random.choice(HEARTS)
        img = emoji_to_image(heart_char, size=64)
        if img:
            self.heart_photo = img
            self.heart_label.config(image=self.heart_photo, text="")
        else:
            self.heart_photo = None
            self.heart_label.config(text=heart_char, image="")
        self.autosize()

    def clear_heart(self):
        self.heart_photo = None
        self.heart_label.config(text="", image="")
        self.autosize()

    # they clicked a mood!
    def handle_mood(self, mood):
        if self.is_answered:
            return
        self.is_answered = True

        for b in self.buttons:
            b.config(state="disabled")

        if is_birthday(self.birthday):
            bday = self.fill(self._pick_birthday_message())
            reply = self.fill(random.choice(RESPONSES[mood]))
            msg = f"{bday}\n\n{reply}"
        else:
            msg = self.fill(random.choice(RESPONSES[mood]))

        self.set_bubble_text(msg)
        self.show_heart()

        # mood wolf:
        #   good   → HappyWolf
        #   okay   → NormalWolf
        #   normal → SadWolf
        if USE_IMAGES:
            if mood == "good":
                self.set_wolf_image(IMG_HAPPY)
            elif mood == "okay":
                self.set_wolf_image(IMG_NORMAL)
            elif mood == "normal":
                self.set_wolf_image(IMG_SAD)

    def reset(self):
        self.is_answered = False
        for b in self.buttons:
            b.config(state="normal")
        self.clear_heart()
        self.refresh_greeting()
        if USE_IMAGES:
            self.set_wolf_image(IMG_QUESTION)

    # the settings window
    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.config(bg=self.theme["bg"])
        win.geometry("380x520")
        win.attributes("-topmost", True)

        t = self.theme

        tk.Label(win, text="Your name", bg=t["bg"], fg=t["text"],
                 font=("Calibri", 12)).pack(pady=(16, 4))
        name_var = tk.StringVar(value=self.name)
        tk.Entry(win, textvariable=name_var, font=("Segoe UI", 11),
                 justify="center").pack(padx=24, fill="x")

        tk.Label(win, text="Birthday (MM-DD, e.g. 02-25)", bg=t["bg"], fg=t["text"],
                 font=("Calibri", 12)).pack(pady=(16, 4))
        bday_var = tk.StringVar(value=self.birthday)
        tk.Entry(win, textvariable=bday_var, font=("Segoe UI", 11),
                 justify="center").pack(padx=24, fill="x")

        tk.Label(win, text="Theme colours", bg=t["bg"], fg=t["text"],
                 font=("Calibri", 12)).pack(pady=(16, 4))

        colour_frame = tk.Frame(win, bg=t["bg"])
        colour_frame.pack(pady=4)

        local_theme = dict(self.theme)

        def picky(key, label):
            c = colorchooser.askcolor(color=local_theme[key], title=f"Pick {label}")[1]
            if c:
                local_theme[key] = c

        row1 = tk.Frame(colour_frame, bg=t["bg"])
        row1.pack(pady=2)
        row2 = tk.Frame(colour_frame, bg=t["bg"])
        row2.pack(pady=2)

        for key, label in [("bg", "Background"), ("bubble", "Bubble"), ("text", "Text")]:
            tk.Button(
                row1, text=label, font=("Calibri", 9),
                bg=t["btn_bg"], fg=t["btn_text"],
                relief="flat", bd=0, cursor="hand2", padx=8, pady=4,
                command=lambda k=key, l=label: picky(k, l),
            ).pack(side="left", padx=3)

        for key, label in [("btn_bg", "Button"), ("btn_text", "Button text")]:
            tk.Button(
                row2, text=label, font=("Calibri", 9),
                bg=t["btn_bg"], fg=t["btn_text"],
                relief="flat", bd=0, cursor="hand2", padx=8, pady=4,
                command=lambda k=key, l=label: picky(k, l),
            ).pack(side="left", padx=3)

        def save_and_close():
            self.name = name_var.get().strip()
            self.birthday = bday_var.get().strip()
            self.theme = local_theme

            self.cfg["name"] = self.name
            self.cfg["birthday"] = self.birthday
            self.cfg["theme"] = self.theme
            save_config(self.cfg)

            self.apply_theme()
            self.refresh_greeting()
            self.autosize()
            win.destroy()

        tk.Button(
            win, text="Save",
            bg=t["btn_bg"], fg=t["btn_text"],
            font=("Calibri", 10, "bold"),
            relief="flat", bd=0, cursor="hand2",
            padx=20, pady=8,
            command=save_and_close,
        ).pack(pady=24)

    def apply_theme(self):
        t = self.theme
        self.root.configure(bg=t["bg"])
        self.card.configure(bg=t["bg"])
        self.wolf_label.configure(bg=t["bg"])
        self.bubble.configure(bg=t["bubble"], fg=t["text"])
        self.heart_label.configure(bg=t["bg"])
        self.close_btn.configure(bg=t["btn_bg"], fg=t["btn_text"])
        self.settings_btn.configure(bg=t["btn_bg"])
        self.reset_btn.configure(bg=t["btn_bg"], fg=t["btn_text"],
                                 activebackground=t["bubble"])
        for b in self.buttons:
            b.configure(bg=t["btn_bg"], fg=t["btn_text"],
                        activebackground=t["bubble"])


# go!!
if __name__ == "__main__":
    root = tk.Tk()
    app = WolfApp(root)
    root.mainloop()