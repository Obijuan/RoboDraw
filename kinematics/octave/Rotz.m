%%------------------------------------------------------------------
%% (c) Juan Gonzalez-Gomez (Obijuan)  juan@iearobotics.com
%% Abril-2012
%%------------------------------------------------------------------
%% Matriz homogenea de rotacion alrededor del eje z
%% Angulo a en radianes
function T=Rotz(a)

ca = cos(a);
sa = sin(a);

T = [ ca -sa  0  0;
      sa  ca  0  0;
      0  0    1  0;
      0  0    0  1];
