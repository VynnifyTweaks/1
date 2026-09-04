#define MyAppName "Vynnify Aim Tweaks"
#define MyAppVersion "2.0.0"
#define MyAppExeName "Vynnify Aim Tweaks.exe"
[Setup]
AppId={{B7A2C6B0-DA8D-4B35-8E1E-9D0E5B8E11A1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\Vynnify Aim Tweaks
DefaultGroupName={#MyAppName}
OutputBaseFilename=Vynnify_Aim_Tweaks_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=vynnify.ico
[Files]
Source: "dist\Vynnify Aim Tweaks.exe"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{group}\Vynnify Aim Tweaks"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Vynnify Aim Tweaks"; Filename: "{app}\{#MyAppExeName}"
[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Vynnify Aim Tweaks"; Flags: nowait postinstall skipifsilent
