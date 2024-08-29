@echo off
start /B cmd /C "fgfs --aircraft=A320neo-PW --generic=socket,in,60,127.0.0.1,8000,udp,EFIS_UDP_IN_prueba4 --generic=socket,out,60,127.0.0.1,8040,udp,EFIS_UDP_OUT2 --httpd=8080 --enable-fullscreen --log-dir="D:\DocumentosHDD\UNIVERSIDAD\TFG\Ordenador_simulador\Nasal_logs" "
start /B cmd /C "activate cockpit_environement && python D:\DocumentosHDD\UNIVERSIDAD\TFG\Ordenador_simulador\Python_out9.py"
pause