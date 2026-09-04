import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import json, random, time, math, subprocess, os

BG='#07060b'; CARD='#100d16'; CARD2='#15101d'; BORDER='#2b203b'; TEXT='#f5f3f8'; MUTED='#aaa2b5'; PURPLE='#8f2cff'; PURPLE2='#b95cff'; GREEN='#42d47a'
DATA=Path.home()/'VynnifyAimTweaks'; DATA.mkdir(exist_ok=True); PROFILE=DATA/'profile.json'

class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title('Vynnify Aim Tweaks'); self.geometry('1180x760'); self.minsize(980,650); self.configure(bg=BG)
        self.overrideredirect(False); self.reaction_start=None; self.times=[]
        self.setup_style(); self.build_shell(); self.show('Dashboard')
    def setup_style(self):
        s=ttk.Style(self); s.theme_use('clam'); s.configure('TNotebook',background=BG); s.configure('TButton',background=PURPLE,foreground='white',padding=(15,9),font=('Segoe UI',10,'bold')); s.map('TButton',background=[('active',PURPLE2)]); s.configure('TCombobox',fieldbackground=CARD2,background=CARD2,foreground=TEXT); s.configure('TEntry',fieldbackground=CARD2,foreground=TEXT)
    def txt(self,p,t,sz=10,c=TEXT,b=False): return tk.Label(p,text=t,bg=p.cget('bg'),fg=c,font=('Segoe UI',sz,'bold' if b else 'normal'))
    def card(self,p,title,desc=None):
        f=tk.Frame(p,bg=CARD,highlightbackground=BORDER,highlightthickness=1); f.pack(fill='x',pady=7)
        self.txt(f,title,15,TEXT,True).pack(anchor='w',padx=18,pady=(15,3))
        if desc:self.txt(f,desc,9,MUTED).pack(anchor='w',padx=18,pady=(0,14))
        return f
    def build_shell(self):
        top=tk.Frame(self,bg='#050408',height=72); top.pack(fill='x'); top.pack_propagate(False)
        tk.Label(top,text='V',bg='#050408',fg=PURPLE2,font=('Segoe UI',32,'bold')).pack(side='left',padx=(24,3)); tk.Label(top,text='YNN',bg='#050408',fg='white',font=('Segoe UI',25,'bold')).pack(side='left'); tk.Label(top,text='AIM TWEAKS',bg='#050408',fg=PURPLE2,font=('Segoe UI',11,'bold')).pack(side='left',padx=12)
        self.status=tk.Label(top,text='● READY',bg='#050408',fg=GREEN,font=('Segoe UI',9,'bold')); self.status.pack(side='right',padx=28)
        body=tk.Frame(self,bg=BG); body.pack(fill='both',expand=True)
        self.nav=tk.Frame(body,bg='#0a080e',width=210); self.nav.pack(side='left',fill='y'); self.nav.pack_propagate(False)
        self.content=tk.Frame(body,bg=BG); self.content.pack(side='right',fill='both',expand=True,padx=24,pady=22)
        self.buttons={}
        for name,icon in [('Dashboard','⌂'),('Sensitivity','◎'),('Aim Trainer','◉'),('Windows Tweaks','⚙'),('Profiles','☷'),('About','ⓘ')]:
            b=tk.Button(self.nav,text=f'  {icon}  {name}',anchor='w',bg='#0a080e',fg=MUTED,activebackground='#21142e',activeforeground='white',relief='flat',bd=0,font=('Segoe UI',10,'bold'),command=lambda n=name:self.show(n)); b.pack(fill='x',padx=10,pady=3,ipady=9); self.buttons[name]=b
        self.txt(self.nav,'VYNNIFY',9,PURPLE2,True).pack(side='bottom',pady=(0,2)); self.txt(self.nav,'OPTIMIZE. PRACTICE. IMPROVE.',7,MUTED).pack(side='bottom',pady=(0,18))
    def clear(self):
        for w in self.content.winfo_children(): w.destroy()
    def select(self,name):
        for n,b in self.buttons.items(): b.config(bg='#21142e' if n==name else '#0a080e',fg='white' if n==name else MUTED)
    def show(self,name):
        self.clear(); self.select(name); getattr(self,'page_'+name.lower().replace(' ','_'))()
    def heading(self,title,sub):
        self.txt(self.content,title,28,TEXT,True).pack(anchor='w'); self.txt(self.content,sub,10,MUTED).pack(anchor='w',pady=(2,18))
    def page_dashboard(self):
        self.heading('Dashboard','Tune your settings, train your reactions, and apply safe Windows optimizations.')
        row=tk.Frame(self.content,bg=BG); row.pack(fill='x')
        for t,d in [('ZERO DELAY','Lower perceived input latency'),('BETTER PERFORMANCE','Cleaner Windows setup'),('OPTIMIZED SYSTEM','Reversible system options'),('CUSTOM TWEAKS','Save your own profile')]:
            f=tk.Frame(row,bg=CARD,highlightbackground=BORDER,highlightthickness=1); f.pack(side='left',fill='both',expand=True,padx=5); self.txt(f,t,11,PURPLE2,True).pack(anchor='w',padx=14,pady=(15,3)); self.txt(f,d,8,MUTED).pack(anchor='w',padx=14,pady=(0,15))
        self.card(self.content,'Quick Start','Everything here is user-controlled. No aim automation or game-memory modification.')
        q=tk.Frame(self.content,bg=CARD); q.pack(fill='x',pady=7)
        for t,cmd in [('Sensitivity','Sensitivity'),('Reaction Trainer','Aim Trainer'),('Safe Windows Tweaks','Windows Tweaks')]: ttk.Button(q,text=t,command=lambda c=cmd:self.show(c)).pack(side='left',padx=14,pady=18)
    def page_sensitivity(self):
        self.heading('Sensitivity','Calculate eDPI and save your Fortnite mouse setup.')
        f=self.card(self.content,'Mouse Setup','eDPI = DPI × X sensitivity as a decimal.')
        fields=[('DPI','800'),('X Sensitivity (%)','8'),('Y Sensitivity (%)','8')]; self.entries={}
        for i,(n,v) in enumerate(fields):
            self.txt(f,n,9,MUTED).grid(row=i,column=0,sticky='w',padx=18,pady=8); e=tk.Entry(f,bg=CARD2,fg=TEXT,insertbackground=TEXT,relief='flat',font=('Segoe UI',11)); e.insert(0,v); e.grid(row=i,column=1,sticky='ew',padx=18,pady=8); self.entries[n]=e
        f.columnconfigure(1,weight=1); ttk.Button(f,text='Calculate eDPI',command=self.calc).grid(row=3,column=1,sticky='w',padx=18,pady=14)
        self.result=self.txt(f,'eDPI: —',16,PURPLE2,True); self.result.grid(row=4,column=0,columnspan=2,sticky='w',padx=18,pady=(0,16))
    def calc(self):
        try:self.result.config(text=f"eDPI: {float(self.entries['DPI'].get())*float(self.entries['X Sensitivity (%)'].get())/100:.1f}")
        except:messagebox.showerror('Vynnify','Enter valid numbers.')
    def page_aim_trainer(self):
        self.heading('Aim Trainer','Simple reaction drills you can practice without automating Fortnite input.')
        self.target=tk.Button(self.content,text='START',command=self.start_reaction,bg=CARD2,fg=TEXT,activebackground=PURPLE,activeforeground='white',relief='flat',font=('Segoe UI',22,'bold'),height=8,width=30); self.target.pack(pady=30)
        self.score=self.txt(self.content,'Best: —   Average: —',13,PURPLE2,True); self.score.pack()
    def start_reaction(self): self.target.config(text='WAIT...',bg=CARD2,command=lambda:None); self.after(random.randint(800,2200),self.arm)
    def arm(self): self.reaction_start=time.perf_counter(); self.target.config(text='CLICK!',bg=PURPLE,command=self.finish)
    def finish(self):
        if self.reaction_start is None:return
        ms=(time.perf_counter()-self.reaction_start)*1000; self.times.append(ms); self.score.config(text=f'Best: {min(self.times):.0f} ms   Average: {sum(self.times)/len(self.times):.0f} ms'); self.target.config(text='START',bg=CARD2,command=self.start_reaction); self.reaction_start=None
    def page_windows_tweaks(self):
        self.heading('Windows Tweaks','Only reversible, user-level settings are offered here.')
        f=self.card(self.content,'Gaming & Responsiveness','Apply conservative Windows settings; restart/sign out if needed.')
        self.gamemode=tk.BooleanVar(value=True); self.anim=tk.BooleanVar(value=False)
        for text,var in [('Keep Windows Game Mode enabled',self.gamemode),('Reduce common UI animations',self.anim)]: tk.Checkbutton(f,text=text,variable=var,bg=CARD,fg=TEXT,activebackground=CARD,activeforeground=TEXT,selectcolor=CARD2,font=('Segoe UI',10)).pack(anchor='w',padx=18,pady=6)
        ttk.Button(f,text='Apply Safe Settings',command=self.apply).pack(anchor='w',padx=18,pady=15)
        ttk.Button(self.content,text='Open Windows Game Mode',command=lambda:subprocess.Popen('start ms-settings:gaming-gamemode',shell=True)).pack(anchor='w',pady=10)
    def apply(self):
        if os.name!='nt':messagebox.showinfo('Vynnify','These Windows settings can only be applied on Windows.');return
        try:
            import winreg
            k=winreg.CreateKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\GameBar'); winreg.SetValueEx(k,'AutoGameModeEnabled',0,winreg.REG_DWORD,1 if self.gamemode.get() else 0); k.Close()
            messagebox.showinfo('Vynnify','Safe settings applied. Restart or sign out if Windows does not update immediately.')
        except Exception as e:messagebox.showerror('Vynnify',str(e))
    def page_profiles(self):
        self.heading('Profiles','Save your sensitivity setup locally on this PC.')
        f=self.card(self.content,'Current Profile'); self.name=tk.Entry(f,bg=CARD2,fg=TEXT,insertbackground=TEXT,relief='flat',font=('Segoe UI',11)); self.name.insert(0,'Vynnify Default'); self.name.pack(fill='x',padx=18,pady=15)
        ttk.Button(f,text='Save Profile',command=self.save).pack(side='left',padx=18,pady=(0,15)); ttk.Button(f,text='Load Profile',command=self.load).pack(side='left',pady=(0,15)); self.pstatus=self.txt(f,'',9,MUTED); self.pstatus.pack(anchor='w',padx=18,pady=(0,12))
    def save(self):
        data={'name':self.name.get()};
        if hasattr(self,'entries'): data.update({k:v.get() for k,v in self.entries.items()})
        PROFILE.write_text(json.dumps(data,indent=2)); self.pstatus.config(text='Profile saved.')
    def load(self):
        try:
            d=json.loads(PROFILE.read_text()); self.name.delete(0,'end'); self.name.insert(0,d.get('name','Vynnify Default')); self.pstatus.config(text='Profile loaded. Open Sensitivity to view values.')
        except:messagebox.showinfo('Vynnify','No saved profile found.')
    def page_about(self):
        self.heading('About Vynnify Aim Tweaks','Built for legitimate practice and PC optimization.')
        f=self.card(self.content,'Vynnify','Optimize. Practice. Improve.'); self.txt(f,'This app does not automate aiming, recoil, clicks, game memory, or anti-cheat bypasses.',10,MUTED).pack(anchor='w',padx=18,pady=(0,16))
        self.txt(self.content,'Version 2.0',9,MUTED).pack(anchor='w',pady=10)

if __name__=='__main__': App().mainloop()
