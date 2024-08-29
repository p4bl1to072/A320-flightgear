@echo off
start /B cmd /C "fgfs --aircraft=A320neo-PW --generic=socket,out,60,127.0.0.1,8040,udp,EFIS_UDP_OUT --httpd=8080 --enable-fullscreen"
start /B cmd /C "activate cockpit_environement && python D:\DocumentosHDD\UNIVERSIDAD\TFG\Ordenador_simulador\Python_out2.py"
pause