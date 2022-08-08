#define APP "BoardCommunication"
#define VERSION "1.0.0.0"

#define Source "E:\python\BoardCommunication\dist"
#define Destination "C:\Program Files\BoardCommunication"
#define MyAppIcoName "E:\python\BoardCommunication\Resources\icon.png"

[Setup]
AppId={{6476CA3E-6724-4BB6-9352-335193147A25}
AppName={#APP}
AppVersion={#VERSION}
;AppVerName={#MyAppName} {#MyAppVersion}
DefaultDirName={#Destination}
DisableDirPage=false
DefaultGroupName={#APP}
DisableProgramGroupPage=yes
OutputBaseFilename={#APP}
AllowRootDirectory=true
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: {#Source}\*; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs overwritereadonly; 

[Icons]
Name: "{autodesktop}\BoardCommunication"; Filename: "{app}\BoardCommunication.exe"; WorkingDir: "{app}"

