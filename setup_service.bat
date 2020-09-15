call nssm.exe install mis_system_cons_service "%cd%\run_server.bat"
call nssm.exe set mis_system_cons_service AppStdout "%cd%\logs\mis_system_cons_service.log"
call nssm.exe set mis_system_cons_service AppStderr "%cd%\logs\mis_system_cons_service.log"
call sc start mis_system_cons_service
rem call nssm.exe edit mis_system_cons_service