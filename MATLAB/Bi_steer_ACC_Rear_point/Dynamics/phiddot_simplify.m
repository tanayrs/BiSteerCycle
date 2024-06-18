clc;
clear;

syms m I11 I22 I33 positive
syms dr df h positive


syms kf kr positive

syms    x    y    psi    phi    theta_R    theta_F real
syms xdot ydot psidot phidot theta_Rdot theta_Fdot real

syms Tr   Tf                         real
syms V  Vdot vFscalar  Vf Vfdot      real
syms Nf Nr Nfg Nrg g                 real 
syms phiddot psiddot                 real


%{

phiddot = (g*h*m*sin(phi) 

            + (Vdot*h*m*cos(phi)*tan(theta_R))/(cos(phi)^2 + tan(theta_R)^2)^(1/2)
             
            + (I22*V^2*cos(phi)*sin(phi)*tan(theta_F)^2)/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2)) 
            - (I33*V^2*cos(phi)*sin(phi)*tan(theta_F)^2)/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2)) 
            + (I22*V^2*cos(phi)*sin(phi)*tan(theta_R)^2)/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2)) 
            - (I33*V^2*cos(phi)*sin(phi)*tan(theta_R)^2)/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2)) 
            
            + (V*h*m*theta_Rdot*cos(phi)^3)/(cos(theta_R)^2*(cos(phi)^2 + tan(theta_R)^2)^(3/2)) 
            
            + (V^2*h*m*cos(phi)^2*tan(theta_F))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)) 
            - (V^2*h*m*cos(phi)^2*tan(theta_R))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)) 
            
            + (V^2*h^2*m*cos(phi)*sin(phi)*tan(theta_F)^2)/((df + dr)^2*(cos(phi)^2+ tan(theta_R)^2)) 
            + (V^2*h^2*m*cos(phi)*sin(phi)*tan(theta_R)^2)/((df + dr)^2*(cos(phi)^2+ tan(theta_R)^2)) 
            
            + (V*h*m*phidot*cos(phi)^2*sin(phi)*tan(theta_R))/(cos(phi)^2 + tan(theta_R)^2)^(3/2) 
            - (V*dr*h*m*theta_Rdot*cos(phi)^3)/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(3/2))
             
            + (Vdot*dr*h*m*cos(phi)*tan(theta_F))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(1/2)) 
            - (Vdot*dr*h*m*cos(phi)*tan(theta_R))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(1/2)) 
            
            - (2*I22*V^2*cos(phi)*sin(phi)*tan(theta_F)*tan(theta_R))/((df + dr)^2*(cos(phi)^2+ tan(theta_R)^2)) 
            + (2*I33*V^2*cos(phi)*sin(phi)*tan(theta_F)*tan(theta_R))/((df + dr)^2*(cos(phi)^2+ tan(theta_R)^2)) 
            
            + (V*dr*h*m*theta_Fdot*cos(phi))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(1/2)) 
            + (V*dr*h*m*theta_Fdot*cos(phi)*tan(theta_F)^2)/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(1/2)) 
            
            - (2*V^2*h^2*m*cos(phi)*sin(phi)*tan(theta_F)*tan(theta_R))/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2)) 
            
            - (V*dr*h*m*theta_Rdot*cos(phi)^3*tan(theta_R)^2)/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(3/2)) 
            
            + (V*dr*h*m*phidot*cos(phi)^2*sin(phi)*tan(theta_F))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(3/2)) 
            - (V*dr*h*m*phidot*cos(phi)^2*sin(phi)*tan(theta_R))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(3/2))
             
            - (V*dr*h*m*theta_Rdot*cos(phi)*tan(theta_F)*tan(theta_R)^3)/((df + dr)*(cos(phi)^2 +tan(theta_R)^2)^(3/2)) 
            - (V*dr*h*m*theta_Rdot*cos(phi)*tan(theta_F)*tan(theta_R))/((df + dr)*(cos(phi)^2+ tan(theta_R)^2)^(3/2))) 
            
            /(m*h^2 + I11)








%}



t1 = (I22*V^2*cos(phi)*sin(phi)*tan(theta_F)^2)/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2))...
   - (I33*V^2*cos(phi)*sin(phi)*tan(theta_F)^2)/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2))... 
   + (I22*V^2*cos(phi)*sin(phi)*tan(theta_R)^2)/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2))...
   - (I33*V^2*cos(phi)*sin(phi)*tan(theta_R)^2)/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2)); 

t11 = (V^2*cos(phi)*sin(phi)*(I22 - I33)*(tan(theta_F)^2 + tan(theta_R)^2))/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2));
 

