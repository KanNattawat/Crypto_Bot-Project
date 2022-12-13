Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run chr(34) & "Terminal_1.cmd" & Chr(34), 0
Set WshShell = Nothing

Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run chr(34) & "Terminal_2.cmd" & Chr(34), 0
Set WshShell = Nothing