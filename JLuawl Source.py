import customtkinter as ctk
import tkinter as tk
import luawl
import os
import json
import urllib
from urllib import request
from PIL import Image, ImageTk
import io
from io import BytesIO

root = ctk.CTk()
root.geometry("200x310")
root.title("JLuawl")
root.attributes("-topmost", False)
api_key = None
ScriptID = None

local_appdata_path = os.getenv("LOCALAPPDATA")
folder_path = os.path.join(local_appdata_path, "JLuawl")
file_path = os.path.join(folder_path, "APIKey.json")
image_path = os.path.join(folder_path, "JLuawlFav.ico")

def API_event():
    global api_key
    dialog = ctk.CTkInputDialog(
        text="Enter your API Key:",
        button_fg_color="black",
        button_hover_color="grey",
        title="API Key",
    )
    text = dialog.get_input()
    api_key = text
    luawl.luawl_token = text
    with open(file_path, "w") as f:
        json.dump({"APIKey": text}, f)
        print(f"'{file_path}' has been created.")

class MyFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, table_list, **kwargs):

        super().__init__(master, **kwargs)

        try:

            for i, v in enumerate(table_list):
                self.label = ctk.CTkLabel(self, text=table_list[i])
                self.label.pack()

        except Exception as e:

            NotificationWindow(
                text=f"Whitelist Information Error: {e} (Is your API Token Valid? / Server Connection Error)",
                nclass="Warning",
            )


class KeysFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, table_list, **kwargs):

        super().__init__(master, **kwargs)

        try:

            for i, v in enumerate(table_list):
                font = ("Impact", 10)
                self.label = ctk.CTkLabel(self, font=font, text=table_list[i])
                self.label.pack()

        except Exception as e:

            NotificationWindow(
                text=f"Keys Error: {e} (Is your API Token Valid? / Server Connection Error)",
                nclass="Warning",
            )


# ---------------------------------CLOSEWINDOW & NOTIF


def CloseWindow(self):
    self.withdraw()


class NotificationWindow(ctk.CTkToplevel):
    def __init__(self, text, nclass, *args, **kwargs):

        super().__init__(*args, **kwargs)

        global Scriptentry
        # self.geometry("300x50")

        self.anchor = ctk.SE

        if nclass == "Warning":
            self.title("Warning")
            self.label = ctk.CTkLabel(self, text_color="red", text=text)
        else:

            self.title("Success")
            self.label = ctk.CTkLabel(self, text_color="green", text=text)

        self.label.pack()
        self.okbutton = ctk.CTkButton(
            self,
            text="Ok",
            fg_color="black",
            hover_color="grey",
            command=lambda: CloseWindow(self),
        )
        self.okbutton.pack()
        NewLen = len(text) * 5
        NewWidth = 100 + NewLen

        self.geometry(f"{NewWidth}x50")
        self.attributes("-topmost", True)
        self.focus_force()
        self.lift()


# --------------------------------WHITELIST INFORMATION WINDOW
class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, whitelist, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.geometry("400x300")
        self.title("Whitelist Information")
        table_json = json.loads(whitelist)
        font = ("Trebuchet MS", 12)

        self.infolabel = ctk.CTkLabel(self, font=font, text="Whitelist Information")

        self.infolabel.pack(pady=5)

        discordid = table_json["discord_id"]
        avatarid = table_json["discord_avatar"]
        ThumbURL = f"https://cdn.discordapp.com/avatars/{discordid}/{avatarid}"
        headers = {
            "Authorization": "Bot MTEwNTU5MjYzMDI2MTMzNDA3Ng.GRAHIf.c5WvFABbSp43weUn37TTLnIzN_diJmZOnN95_c", # i think you leaked your token.
            "User-Agent": "MyDiscordBot/1.0",
        }
        req = request.Request(ThumbURL, headers=headers)
        try:
            with request.urlopen(req) as u:
                raw_data = u.read()
                im = Image.open(io.BytesIO(raw_data))
                my_image = ctk.CTkImage(light_image=im, dark_image=im, size=(100, 100))

                avatarlabel = ctk.CTkLabel(self, image=my_image, text="")
                avatarlabel.pack()
        except Exception as e:
            print(e)
        table_list = [[key, str(value)] for key, value in table_json.items()]
        my_frame = MyFrame(master=self, table_list=table_list, width=400, height=200)
        my_frame.pack()
        self.attributes("-topmost", True)
        self.focus_force()
        self.lift()


IDentry = ctk.CTkEntry(root, placeholder_text="Discord ID / Key")
IDentry.pack(pady=5)


def Lookup():
    global IDentry
    key = IDentry.get()
    try:
        whitelist = luawl.get_whitelist(key)
    except Exception as e:
        NotificationWindow(text=f"ID Error: {e}", nclass="Warning")
    if "whitelist" in locals():
        whitelist = str(whitelist)
        ToplevelWindow(whitelist)


Lookupbutton = ctk.CTkButton(
    root,
    text="Whitelist information",
    fg_color="black",
    hover_color="grey",
    command=Lookup,
)
Lookupbutton.pack(pady=5)

def WhitelistScript(main, SID):
    global Scriptentry
    global IDentry
    global Trialentro
    if SID == "SID":
        Trialentry = Trialentro.get()
        key = IDentry.get()
        ScriptID = Scriptentry.get()
        if ScriptID:
            if Trialentry != "" and int(Trialentry):
                try:
                    luawl.add_whitelist(key, int(Trialentry), ScriptID)
                except Exception as e:
                    NotificationWindow(text=f"Whitelist Error: {e}", nclass="Warning")
                main.attributes("-topmost", False)
                NotificationWindow(
                    text=f"Whitelisted {key} to Script ID: {ScriptID} for {Trialentry} Hours!",
                    nclass="W",
                )
            else:
                try:
                    luawl.add_whitelist(key, wl_script_id=ScriptID)
                except Exception as e:
                    NotificationWindow(text=f"Whitelist Error: {e}", nclass="Warning")
                main.attributes("-topmost", False)
                NotificationWindow(
                    text=f"Whitelisted {key} to Script ID: {ScriptID}", nclass="W"
                )
    else:
        Trialentry = Trialentro.get()
        key = IDentry.get()
        if Trialentry != "" and int(Trialentry):
            try:
                luawl.add_whitelist(key, trial_hours=int(Trialentry))
            except Exception as e:
                NotificationWindow(text=f"Whitelist Error: {e}", nclass="Warning")
            main.attributes("-topmost", False)
            NotificationWindow(
                text=f"Universal Whitelist Added to {key} for {Trialentry} Hours!",
                nclass="W",
            )
        else:
            try:
                luawl.add_whitelist(key)
            except Exception as e:
                NotificationWindow(text=f"Whitelist Error: {e}", nclass="Warning")
            main.attributes("-topmost", False)
            NotificationWindow(text=f"Universal Whitelist Added to {key}", nclass="W")


class WhiteListWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global Scriptentry
        global Trialentro
        global IDentry
        key = IDentry.get()
        if key != "":
            self.geometry("200x150")
            self.title("Whitelist")
            Scriptentry = ctk.CTkEntry(self, placeholder_text="Script ID")
            Scriptentry.pack(pady=5)
            Trialentro = ctk.CTkEntry(self, placeholder_text="Trial Time (Optional)")
            Trialentro.pack()
            ScriptWhitelistbutton = ctk.CTkButton(
                self,
                text="Whitelist to script",
                fg_color="black",
                hover_color="grey",
                command=lambda: WhitelistScript(self, "SID"),
            )
            ScriptWhitelistbutton.pack(pady=5)
            Whitelistbutton = ctk.CTkButton(
                self,
                text="Universal Whitelist",
                fg_color="black",
                hover_color="grey",
                command=lambda: WhitelistScript(self, "Universal"),
            )
            Whitelistbutton.pack()
            self.attributes("-topmost", True)
            self.focus_force()
            self.lift()
        else:
            self.withdraw()
            NotificationWindow(text=f"Whitelist Error: Blank ID", nclass="Warning")

def Blacklist():
    global IDentry
    key = IDentry.get()
    try:
        if key != "":
            luawl.add_blacklist(key)
            NotificationWindow(text=f"Blacklist Added", nclass="W")
        else:
            NotificationWindow(text=f"Blacklist Error: Blank ID", nclass="Warning")
    except Exception as e:
        NotificationWindow(text=f"Blacklist Error: {e}", nclass="Warning")

def Unblacklist():
    global IDentry
    key = IDentry.get()
    try:
        if key != "":
            luawl.remove_blacklist(key)
            NotificationWindow(text=f"Unblacklisted!", nclass="W")
        else:
            NotificationWindow(text=f"Unblacklist Error: Blank ID", nclass="Warning")
    except Exception as e:
        NotificationWindow(text=f"Unblacklist Error: {e}", nclass="Warning")

def DelWhitelist():
    global IDentry
    key = IDentry.get()
    try:
        if key != "":
            luawl.delete_whitelist(key)
            NotificationWindow(text=f"Whitelist Deleted!", nclass="W")
        else:
            NotificationWindow(
                text=f"Whitelist Delete Error: Blank ID", nclass="Warning"
            )
    except Exception as e:
        NotificationWindow(text=f"Whitelist Delete Error: {e}", nclass="Warning")

def RemoveCooldown():
    global IDentry
    key = IDentry.get()
    try:
        if key != "":
            luawl.remove_cooldown(key)
            NotificationWindow(text=f"Cooldown Removed!", nclass="W")
        else:
            NotificationWindow(
                text=f"Cooldown Remove Error: Blank ID", nclass="Warning"
            )
    except Exception as e:
        NotificationWindow(text=f"Cooldown Remove Error: {e}", nclass="Warning")

Whitelistbutton = ctk.CTkButton(
    root,
    text="Whitelist",
    fg_color="black",
    hover_color="grey",
    command=lambda: WhiteListWindow(),
)
Whitelistbutton.pack()

Blacklistbutton = ctk.CTkButton(
    root, text="Blacklist", fg_color="black", hover_color="grey", command=Blacklist
)
Blacklistbutton.pack(pady=5)

Blacklistbutton = ctk.CTkButton(
    root, text="Unblacklist", fg_color="black", hover_color="grey", command=Unblacklist
)
Blacklistbutton.pack()

RemoveCooldownbutton = ctk.CTkButton(
    root,
    text="Remove Cooldown",
    fg_color="black",
    hover_color="grey",
    command=RemoveCooldown,
)
RemoveCooldownbutton.pack()

Delwhitelistbutton = ctk.CTkButton(
    root,
    text="Delete Whitelist",
    fg_color="black",
    hover_color="grey",
    command=DelWhitelist,
)
Delwhitelistbutton.pack(pady=5)

# --------------------------------WHITELIST INFORMATION WINDOW
class KeyWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1900x950")
        self.title("Key List")
        table_json = luawl.get_all_keys()
        font = ("Trebuchet MS", 12)
        self.infolabel = ctk.CTkLabel(self, font=font, text="All Keys")
        self.infolabel.pack(pady=2)
        
        try:
            my_frame = KeysFrame(
                master=self, table_list=table_json, width=1900, height=850
            )
            my_frame.pack()
        except Exception as e:
            NotificationWindow(text=f"Keys Error: {e}", nclass="Warning")
        
        self.attributes("-topmost", True)
        self.focus_force()
        self.lift()


Keysbutton = ctk.CTkButton(
    root, text="Keys", fg_color="black", hover_color="grey", command=KeyWindow
)
Keysbutton.pack(pady=5)

APIChangebutton = ctk.CTkButton(
    root,
    text="Change API Token",
    fg_color="black",
    hover_color="grey",
    command=API_event,
)
APIChangebutton.pack()

ctk.set_appearance_mode("dark")
root.mainloop()

if __name__ == '__main__':
    # Make it run on start because why not.

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"'{folder_path}' has been created.")

    if not os.path.exists(file_path):
        API_event()

    if os.path.exists(file_path):

        with open(file_path, "r") as f:
            api_key_dict = json.load(f)
            api_key = api_key_dict.get("APIKey")

    if api_key:
        luawl.luawl_token = api_key
    else:
        print("No API key found.")

    if not os.path.exists(image_path):

        with request.urlopen("https://jumblescripts.com/JLuawlFav.ico") as u:
            raw_data = u.read()
            im = Image.open(io.BytesIO(raw_data))
            im.save(image_path)

    if os.path.exists(image_path):
        root.iconbitmap(image_path)
