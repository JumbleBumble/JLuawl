import customtkinter as ctk
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
import luawl
import os
import json
import urllib.request
from PIL import Image, ImageTk
import io
from io import BytesIO




#Root Setup
root = ctk.CTk()
root.geometry("650x500")
root.title("JLuawl")
root.attributes("-topmost", False)




#//ANCHOR API KEY & ICON SETUP ---------------------------------------
def API_event():
        global api_key
        dialog = ctk.CTkInputDialog(text="Enter your API Key:",button_fg_color="black",button_hover_color='grey', title="API Key")
        text = dialog.get_input()
        api_key = text
        luawl.luawl_token = text
        with open(APIKey_path, 'w') as f:
            json.dump({"APIKey": text}, f)


local_appdata_path = os.getenv('LOCALAPPDATA')
folder_path = os.path.join(local_appdata_path, 'JLuawl')
APIKey_path = os.path.join(folder_path, 'APIKey.json')

if not os.path.exists(folder_path):
    os.makedirs(folder_path)


if not os.path.exists(APIKey_path):
    API_event()

if os.path.exists(APIKey_path):
    with open(APIKey_path, 'r') as f:
        api_key_dict = json.load(f)
        api_key = api_key_dict.get('APIKey')

if api_key:
    luawl.luawl_token = api_key




image_path = os.path.join(folder_path, 'JLuawlFav.ico')
if not os.path.exists(image_path):
    with urllib.request.urlopen('https://jumblescripts.com/JLuawlFav.ico') as u:
                    raw_data = u.read()
                    im = Image.open(io.BytesIO(raw_data))
                    im.save(image_path)  

if os.path.exists(image_path):
    root.iconbitmap(image_path)


#//ANCHOR COLORS ---------------------------------------
TopBarFGColor = '#0F3F5F'       
BackFGColor = '#0A1929'        
ButtonFGColor = '#4d5e73'      
ButtonBCColor = '#0F3F5F'       
ButtonTextColor = 'white'     
ButtonBW = 2



#Configuring Root
root.configure(fg_color=BackFGColor)
root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=1)
root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=1)
root.rowconfigure(2,weight=1)
root.rowconfigure(3,weight=1)
root.rowconfigure(4,weight=1)


#//ANCHOR UTILITY WINDOWS ----------------------------------------
def CloseWindow(self):
    self.withdraw()

class NotificationWindow(ctk.CTkToplevel):
    def __init__(self,text,nclass, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global Scriptentry
        self.anchor = ctk.SE
        if nclass == 'Warning':
            self.title('Warning')
            self.label = ctk.CTkLabel(self,text_color='red', text=text)
        else:
            self.title('Success')
            self.label = ctk.CTkLabel(self,text_color='green', text=text)
        self.label.pack()
        self.okbutton = ctk.CTkButton(self,text='Ok',fg_color="black",hover_color='grey',command = lambda: CloseWindow(self))
        self.okbutton.pack()
        NewLen = len(text) * 5
        NewWidth=100 + NewLen
        self.geometry(f"{NewWidth}x50")
        self.attributes("-topmost", True)
        self.focus_force()
        self.lift()





#//ANCHOR INFO WINDOWS ----------------------------------------

#Displays User Info
class UserInfo(ctk.CTkScrollableFrame):
    def __init__(self, master,table_list, **kwargs):
        super().__init__(master, **kwargs)
        try:
            for i,v in enumerate(table_list):
                self.label = ctk.CTkLabel(self,text=table_list[i])
                self.label.pack()
        except Exception as e:
             NotificationWindow(text=f'Whitelist Information Error: {e} (Is your API Token Valid? / Server Connection Error)',nclass='Warning')




#WHITELIST INFORMATION WINDOW
class WhitelistInfoWin(ctk.CTkToplevel):
    def __init__(self, whitelist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title('Whitelist Information')
        self.configure(fg_color=TopBarFGColor)
        whitelist_json = json.loads(whitelist)
        font = ('Segoe UI',20)
        self.infolabel = ctk.CTkLabel(self,font=font, text='Whitelist Information')
        self.infolabel.pack(pady=5)
        whitelist_list = [[key, str(value)] for key, value in whitelist_json.items()]
        my_frame = UserInfo(master=self,table_list = whitelist_list, width=400, height=200,fg_color=BackFGColor,border_color=ButtonFGColor,border_width=2)
        my_frame.pack()
        self.attributes("-topmost", True)
        self.focus_force()
        self.lift()




#Window that shows whitelist options
class WhiteListWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global Scriptentry
        global Trialentro
        global IDentry
        self.configure(fg_color=BackFGColor)
        key = IDentry.get()
        if key != '':
            self.geometry("200x150")
            self.title('Whitelist')
            Scriptentry = ctk.CTkEntry(self, placeholder_text="Script ID")
            Scriptentry.pack(pady=5)
            Trialentro = ctk.CTkEntry(self, placeholder_text="Trial Time (Optional)")
            Trialentro.pack()
            ScriptWhitelistbutton = ctk.CTkButton(self, text="Whitelist to script",text_color=ButtonTextColor,fg_color=ButtonFGColor,border_color=ButtonBCColor,border_width=ButtonBW,hover_color='grey', command= lambda: WhitelistScript(self,'SID'))
            ScriptWhitelistbutton.pack(pady=5)
            Whitelistbutton = ctk.CTkButton(self, text="Universal Whitelist",text_color=ButtonTextColor,fg_color=ButtonFGColor,border_color=ButtonBCColor,border_width=ButtonBW,hover_color='grey', command= lambda: WhitelistScript(self,'Universal'))
            Whitelistbutton.pack()
            self.attributes("-topmost", True)
            self.focus_force()
            self.lift()

            #Alternate theme for the WhiteListWindow buttons
            #ScriptWhitelistbutton = ctk.CTkButton(self, text="Whitelist to script",text_color=ButtonTextColor,fg_color=BackFGColor,border_color=ButtonFGColor,border_width=ButtonBW,hover_color='grey', command= lambda: WhitelistScript(self,'SID'))
            #Whitelistbutton = ctk.CTkButton(self, text="Universal Whitelist",text_color=ButtonTextColor,fg_color=BackFGColor,border_color=ButtonFGColor,border_width=ButtonBW,hover_color='grey', command= lambda: WhitelistScript(self,'Universal'))
        else:
             self.withdraw()
             NotificationWindow(text=f'Whitelist Error: Blank ID',nclass='Warning')



#Window that displays all keys
class KeyWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1200x700")
        self.title('Key List')
        self.configure(fg_color=BackFGColor)
        table_json = luawl.get_all_keys()
        font = ('Segoe UI',20)
        self.infolabel = ctk.CTkLabel(self,font=font, text='All Keys')
        self.infolabel.pack(pady=2)
        tree = ttk.Treeview(self,height=30,show='headings')
        tree.pack()
        columns = list(table_json[0].keys())
        tree["columns"] = columns
        for column in columns:
            if column != '':
                tree.heading(column, text=column)
                tree.column(column, width=Font().measure(column) + 20)
        try:
            for i,v in enumerate(table_json):
                tree.insert("", "end", values=list(v.values()))
        except Exception as e:
             NotificationWindow(text=f'Keys Error: {e}',nclass='Warning')

        def copy_to_clipboard():
            selected_item = tree.selection()
            if selected_item:
                values = tree.item(selected_item)['values']
                if values:
                    tcolumns = tree['columns']
                    tcolumn_values = [f"{column}: {value}" for column, value in zip(tcolumns, values)]
                    clipboard_value = (str(tcolumn_values))
                    root.clipboard_clear()
                    root.clipboard_append(clipboard_value)
                    NotificationWindow(text=f'Values Copied!',nclass='W')
   
        tree.bind("<<TreeviewSelect>>", lambda event: copy_to_clipboard())    
        self.attributes("-topmost", True)
        self.focus_force()
        self.lift()




#//ANCHOR STORED VARIABLES ----------------------------------------
api_key = None
ScriptID = None


#//ANCHOR BUTTON FUNCTIONS ----------------------------------------
#Displays a Users whitelist info
def Lookup():
    global IDentry
    key = IDentry.get()
    try:
        whitelist = luawl.get_whitelist(key)
    except Exception as e:
        NotificationWindow(text=f'ID Error: {e}',nclass='Warning')
    if 'whitelist' in locals():
        whitelist = str(whitelist)
        WhitelistInfoWin(whitelist)




#Handles whitelisting for WhiteListWindow
def WhitelistScript(main,SID):
    global Scriptentry
    global IDentry
    global Trialentro
    if SID == 'SID':
        Trialentry = Trialentro.get()
        key = IDentry.get()
        ScriptID = Scriptentry.get()
        if ScriptID:
            if Trialentry != '' and int(Trialentry):
                try:
                    luawl.add_whitelist(key,int(Trialentry),ScriptID)
                except Exception as e:
                    NotificationWindow(text=f'Whitelist Error: {e}',nclass='Warning')
                main.attributes("-topmost", False)
                NotificationWindow(text=f'Whitelisted {key} to Script ID: {ScriptID} for {Trialentry} Hours!',nclass='W')
            else:
                try:
                    luawl.add_whitelist(key,wl_script_id=ScriptID)
                except Exception as e:
                    NotificationWindow(text=f'Whitelist Error: {e}',nclass='Warning')
                main.attributes("-topmost", False)
                NotificationWindow(text=f'Whitelisted {key} to Script ID: {ScriptID}',nclass='W')
    else:
        Trialentry = Trialentro.get()
        key = IDentry.get()
        if Trialentry != '' and int(Trialentry):
            try:
                luawl.add_whitelist(key,trial_hours=int(Trialentry))
            except Exception as e:
                    NotificationWindow(text=f'Whitelist Error: {e}',nclass='Warning')
            main.attributes("-topmost", False)
            NotificationWindow(text=f'Universal Whitelist Added to {key} for {Trialentry} Hours!',nclass='W')
        else:
            try:
                    luawl.add_whitelist(key)
            except Exception as e:
                NotificationWindow(text=f'Whitelist Error: {e}',nclass='Warning')
            main.attributes("-topmost", False)
            NotificationWindow(text=f'Universal Whitelist Added to {key}',nclass='W')




def Blacklist():
    global IDentry
    key = IDentry.get()
    try:
            if key != '':
                luawl.add_blacklist(key)
                NotificationWindow(text=f'Blacklist Added',nclass='W')
            else:
                NotificationWindow(text=f'Blacklist Error: Blank ID',nclass='Warning')
    except Exception as e:
            NotificationWindow(text=f'Blacklist Error: {e}',nclass='Warning')




def Unblacklist():
    global IDentry
    key = IDentry.get()
    try:
            if key != '':
                luawl.remove_blacklist(key)
                NotificationWindow(text=f'Unblacklisted!',nclass='W')
            else:
                NotificationWindow(text=f'Unblacklist Error: Blank ID',nclass='Warning')
    except Exception as e:
            NotificationWindow(text=f'Unblacklist Error: {e}',nclass='Warning')




def DelWhitelist():
    global IDentry
    key = IDentry.get()
    try:
            if key != '':
                luawl.delete_whitelist(key)
                NotificationWindow(text=f'Whitelist Deleted!',nclass='W')
            else:
                NotificationWindow(text=f'Whitelist Delete Error: Blank ID',nclass='Warning')
    except Exception as e:
            NotificationWindow(text=f'Whitelist Delete Error: {e}',nclass='Warning')




def RemoveCooldown():
    global IDentry
    key = IDentry.get()
    try:
            if key != '':
                luawl.remove_cooldown(key)
                NotificationWindow(text=f'Cooldown Removed!',nclass='W')
            else:
                NotificationWindow(text=f'Cooldown Remove Error: Blank ID',nclass='Warning')
    except Exception as e:
            NotificationWindow(text=f'Cooldown Remove Error: {e}',nclass='Warning')




def ResetHWID():
    global IDentry
    key = IDentry.get()
    try:
            if key != '':
                luawl.reset_hwid(key)
                NotificationWindow(text=f'HWID Reset!',nclass='W')
            else:
                NotificationWindow(text=f'HWID Reset Error: Blank ID',nclass='Warning')
    except Exception as e:
            NotificationWindow(text=f'HWID Reset Error: {e}',nclass='Warning')


#//ANCHOR INTERFACE ----------------------------------------

#Is basically the topbar color of the GUI that holds some stuff
MainFrame = ctk.CTkFrame(root,height=100,width=300,fg_color=TopBarFGColor,bg_color=TopBarFGColor)
MainFrame.grid(column = 0, row = 0,columnspan=2,sticky="nsew")
MainFrame.columnconfigure(0,weight=1)
MainFrame.rowconfigure(0,weight=1)
MainFrame.rowconfigure(1,weight=1)

#Top Title
LuawlLabelStyle = ('Segoe UI',20)
Luawllabel = ctk.CTkLabel(MainFrame,font=LuawlLabelStyle, text="JLuawl Lua Guard Desktop", fg_color="transparent")
Luawllabel.grid(column = 0, row = 0,pady=3)

#API Change button located in corner
APIChangebutton = ctk.CTkButton(root,height=10,width=10, text="Change API Token",fg_color="black",hover_color='grey',bg_color=TopBarFGColor, command = API_event)
APIChangebutton.grid(column = 0, row = 0,pady=5,padx=15,sticky="nw")

#Entry box for ID or Keys
IDentry = ctk.CTkEntry(MainFrame,width=310, placeholder_text="Discord ID / Key")
IDentry.grid(column = 0, row = 1,columnspan=2,pady=12,sticky="n")

#Displays WhitelistInfoWin
Lookupbutton = ctk.CTkButton(root,height=70, text="Whitelist information",text_color=ButtonTextColor,fg_color=ButtonFGColor,border_color=ButtonBCColor,border_width=ButtonBW,hover_color='grey', command = Lookup)
Lookupbutton.grid(column = 0, row = 1,pady=15,padx=15,sticky="nsew")


#Opens WhiteListWindow which contains whitelist options
Whitelistbutton = ctk.CTkButton(root,height=70, text="Whitelist",text_color=ButtonTextColor,fg_color=ButtonFGColor,border_color=ButtonBCColor,border_width=ButtonBW,hover_color='grey', command = lambda: WhiteListWindow())
Whitelistbutton.grid(column = 1, row = 1,pady=15,padx=15,sticky="nsew")


Blacklistbutton = ctk.CTkButton(root,height=70, text="Blacklist",text_color=ButtonTextColor,fg_color=ButtonFGColor,border_color=ButtonBCColor,border_width=ButtonBW,hover_color='grey', command = Blacklist)
Blacklistbutton.grid(column = 1, row = 2,pady=15,padx=15,sticky="nsew")


Unblacklistbutton = ctk.CTkButton(root,height=70, text="Unblacklist",text_color=ButtonTextColor,fg_color=ButtonFGColor,border_color=ButtonBCColor,border_width=ButtonBW,hover_color='grey', command = Unblacklist) 
Unblacklistbutton.grid(column = 0, row = 2,pady=15,padx=15,sticky="nsew")


Delwhitelistbutton = ctk.CTkButton(root,height=70, text="Delete Whitelist",text_color=ButtonTextColor,fg_color=ButtonFGColor,border_color=ButtonBCColor,border_width=ButtonBW,hover_color='grey',command=DelWhitelist) 
Delwhitelistbutton.grid(column = 1, row = 3,pady=15,padx=15,sticky="nsew")


RemoveCooldownbutton = ctk.CTkButton(root,height=70, text="Remove Cooldown",text_color=ButtonTextColor,fg_color=ButtonFGColor,border_color=ButtonBCColor,border_width=ButtonBW,hover_color='grey',command=RemoveCooldown) 
RemoveCooldownbutton.grid(column = 0, row = 3,pady=15,padx=15,sticky="nsew")


ResetHWIDbutton = ctk.CTkButton(root,height=70, text="Reset HWID",text_color=ButtonTextColor,fg_color=ButtonFGColor,border_color=ButtonBCColor,border_width=ButtonBW,hover_color='grey', command = ResetHWID)
ResetHWIDbutton.grid(column = 1, row = 4,pady=15,padx=15,sticky="nsew")


#Opens up the Keys window
Keysbutton = ctk.CTkButton(root,height=70, text="Keys",text_color=ButtonTextColor,fg_color=ButtonFGColor,border_color=ButtonBCColor,border_width=ButtonBW,hover_color='grey', command = KeyWindow)
Keysbutton.grid(column = 0, row = 4,pady=15,padx=15,sticky="nsew")


ctk.set_appearance_mode("dark")
root.mainloop()
