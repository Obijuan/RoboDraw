%%------------------------------------------------------------------
%% (c) Juan Gonzalez-Gomez (Obijuan)  juan@iearobotics.com
%% Sep-28th-2012
%%------------------------------------------------------------------
%% Homogeneous matrix. Translation along the x axis

function T=Trasx(l)

T = [1  0  0  l;
     0  1  0  0;
     0  0  1  0;
     0  0  0  1];
     
