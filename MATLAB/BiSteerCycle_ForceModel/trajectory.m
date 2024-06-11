function heading = trajectory(x,y)


%psidot = (V*sin(theta_F - theta_R))/(cos(theta_F)*(df + dr))



 x_2 = x;
 y_2 = y;

 x_2(end+1) = 0;
 y_2(end+1) = 0;

 x_2 = circshift(x_2,1);
 y_2 = circshift(y_2,1);

 x(end+1) = 0;
 y(end+1) = 0;

 psi = atan((y_2-y)./(x_2-x));


 heading = psi;
 heading(1)=heading(2);
 heading(end) = [];


end