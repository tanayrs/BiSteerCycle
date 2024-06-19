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

t1 = g*h*m*sin(phi) + (Vdot*h*m*cos(phi)*tan(theta_R))/(cos(phi)^2 + tan(theta_R)^2)^(1/2) ;

t2 = (I22*V^2*cos(phi)*sin(phi)*tan(theta_F)^2)/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2))...
   - (I33*V^2*cos(phi)*sin(phi)*tan(theta_F)^2)/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2))... 
   + (I22*V^2*cos(phi)*sin(phi)*tan(theta_R)^2)/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2))...
   - (I33*V^2*cos(phi)*sin(phi)*tan(theta_R)^2)/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2)); 

t4 = (V^2*h*m*cos(phi)^2*tan(theta_F))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2))... 
   - (V^2*h*m*cos(phi)^2*tan(theta_R))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2));

t5 = (V^2*h^2*m*cos(phi)*sin(phi)*tan(theta_F)^2)/((df + dr)^2*(cos(phi)^2+ tan(theta_R)^2))...
   + (V^2*h^2*m*cos(phi)*sin(phi)*tan(theta_R)^2)/((df + dr)^2*(cos(phi)^2+ tan(theta_R)^2));

t6 = (V*h*m*phidot*cos(phi)^2*sin(phi)*tan(theta_R))/(cos(phi)^2 + tan(theta_R)^2)^(3/2)...
   - (V*dr*h*m*theta_Rdot*cos(phi)^3)/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(3/2));

t7 = (Vdot*dr*h*m*cos(phi)*tan(theta_F))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(1/2))...
   - (Vdot*dr*h*m*cos(phi)*tan(theta_R))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(1/2));

t8 = (2*I22*V^2*cos(phi)*sin(phi)*tan(theta_F)*tan(theta_R))/((df + dr)^2*(cos(phi)^2+ tan(theta_R)^2))...
   + (2*I33*V^2*cos(phi)*sin(phi)*tan(theta_F)*tan(theta_R))/((df + dr)^2*(cos(phi)^2+ tan(theta_R)^2));

t9 = -(V*dr*h*m*theta_Fdot*cos(phi))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(1/2))...
   + (V*dr*h*m*theta_Fdot*cos(phi)*tan(theta_F)^2)/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(1/2));

t10 = -(2*V^2*h^2*m*cos(phi)*sin(phi)*tan(theta_F)*tan(theta_R))/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2));
            
t11 = - (V*dr*h*m*theta_Rdot*cos(phi)^3*tan(theta_R)^2)/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(3/2));
            
t12 = (V*dr*h*m*phidot*cos(phi)^2*sin(phi)*tan(theta_F))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(3/2))...
    - (V*dr*h*m*phidot*cos(phi)^2*sin(phi)*tan(theta_R))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(3/2));

t13 = -(V*dr*h*m*theta_Rdot*cos(phi)*tan(theta_F)*tan(theta_R)^3)/((df + dr)*(cos(phi)^2 +tan(theta_R)^2)^(3/2))...
    - (V*dr*h*m*theta_Rdot*cos(phi)*tan(theta_F)*tan(theta_R))/((df + dr)*(cos(phi)^2+ tan(theta_R)^2)^(3/2));



t1 = g*h*m*sin(phi) + (Vdot*h*m*cos(phi)*tan(theta_R))/(cos(phi)^2 + tan(theta_R)^2)^(1/2) ;
t22 = (V^2*cos(phi)*sin(phi)*(I22 - I33)*(tan(theta_F)^2 + tan(theta_R)^2))/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2));
t3 = (V*h*m*theta_Rdot*cos(phi)^3)/(cos(theta_R)^2*(cos(phi)^2 + tan(theta_R)^2)^(3/2));
t44 = (V^2*h*m*cos(phi)^2*(tan(theta_F) - tan(theta_R)))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2));
t55 = (V^2*h^2*m*cos(phi)*sin(phi)*(tan(theta_F)^2 + tan(theta_R)^2))/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2));
t66 = (V*h*m*cos(phi)^2*(df*phidot*sin(phi)*tan(theta_R) - dr*theta_Rdot*cos(phi) + dr*phidot*sin(phi)*tan(theta_R)))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(3/2));

t88 = (2*V^2*cos(phi)*sin(phi)*tan(theta_F)*tan(theta_R)*(I22 + I33))/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2));
t10 = -(2*V^2*h^2*m*cos(phi)*sin(phi)*tan(theta_F)*tan(theta_R))/((df + dr)^2*(cos(phi)^2 + tan(theta_R)^2));

t77 = (Vdot*dr*h*m*cos(phi)*(tan(theta_F) - tan(theta_R)))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(1/2));
t99 = (V*dr*h*m*theta_Fdot*cos(phi)*(tan(theta_F)^2 - 1))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(1/2));
t1212 = (V*dr*h*m*phidot*cos(phi)^2*sin(phi)*(tan(theta_F) - tan(theta_R)))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(3/2));

t11 = - (V*dr*h*m*theta_Rdot*cos(phi)^3*tan(theta_R)^2)/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(3/2));
t1313 = -(V*dr*h*m*theta_Rdot*cos(phi)*tan(theta_F)*tan(theta_R)*(tan(theta_R)^2 + 1))/((df + dr)*(cos(phi)^2 + tan(theta_R)^2)^(3/2));

exp_org = t1+t2+t3+t4+t5+t6+t7+t8+t9+t10+t11+t12+t13;
exp_simple = t1+t22+t3+t44+t55+t66+t77+t88+t99+t10+t11+t1212+t1313;

latex(exp_simple)