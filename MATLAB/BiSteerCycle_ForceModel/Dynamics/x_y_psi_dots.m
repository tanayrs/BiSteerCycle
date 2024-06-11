function out1 = x_y_psi_dots(V,df,dr,phi,psi,theta_F,theta_R)
%X_Y_PSI_DOTS
%    OUT1 = X_Y_PSI_DOTS(V,DF,DR,PHI,PSI,theta_F,theta_R)

%    This function was generated by the Symbolic Math Toolbox version 23.2.
%    21-May-2024 08:06:01

t2 = cos(phi);
t3 = cos(psi);
t4 = sin(psi);
t5 = tan(theta_R);
t6 = t2.^2;
t7 = t5.^2;
t8 = t6+t7;
t9 = 1.0./sqrt(t8);
out1 = [V.*t9.*(t2.*t3-t4.*t5);V.*t9.*(t2.*t4+t3.*t5);-(V.*t9.*(t5-tan(theta_F)))./(df+dr)];
end
