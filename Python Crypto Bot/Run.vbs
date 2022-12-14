Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run chr(34) & "Terminal_AutoTrading.cmd" & Chr(34), 0
Set WshShell = Nothing

Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run chr(34) & "Terminal_TradingInfo.cmd" & Chr(34), 0
Set WshShell = Nothing
