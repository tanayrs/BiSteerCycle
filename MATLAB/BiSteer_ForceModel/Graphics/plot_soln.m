function plot_soln(soln,start,stop,p)

disp('plotting....')

close all

tarray = linspace(start, stop, 100000);
zarray = deval(soln,tarray);

time = soln.x;
z    = soln.y;

control_array = zeros(length(time),4);

for i = 1:length(time)

    [Tf0, Tr0, ~, ~, theta_Fdot0, theta_Rdot0] = controller_bisteer3D(time(i),z(:,i),p);

    control_array(i,1) = Tf0;
    control_array(i,2) = Tr0;
    control_array(i,3) = theta_Fdot0;
    control_array(i,4) = theta_Rdot0;
    
end




x_array      = zarray(1,:);
y_array      = zarray(2,:);
V_array      = zarray(3,:);
phi_array    = zarray(5,:);
phidot_array = zarray(6,:);
theta_Farray = zarray(7,:);
theta_Rarray = zarray(8,:);

Tf           = control_array(:,1);
Tr           = control_array(:,2);
theta_Fdot   = control_array(:,3);
theta_Rdot   = control_array(:,4);


V0      = V_array(1);
dV_array = V_array-V0;


figure(1)
%subplot(1,2,1)
hold on
plot(x_array,y_array);
plot(x_array(1),y_array(1),'b.',MarkerSize=13)
plot(x_array(end),y_array(end),'r.',MarkerSize=13)
legend('','start','end')
title('Trajectory')
xlabel('x')
ylabel('y')
axis equal
movegui('northwest')


figure(2)
%subplot(1,2,2)
plot(tarray,rad2deg(phi_array));
title('lean angle')
xlabel('t');
ylabel('$\phi$ in degrees')
movegui('southwest')

%{
figure(3)
plot(tarray,V_array);
%}

%
figure(3)
%subplot(1,3,3)
plot(tarray,V_array);
title('$ V_R $')
xlabel('t');
ylabel('$\ V$ in m/s')
movegui('north')
%}

%{
figure(4)
plot(tarray,phidot_array)
title('lean rate')
%}


figure(7)
subplot(3,1,1)
hold on
plot(time,Tf,'r');


subplot(3,1,1)
plot(time,Tr,'b')
title('$ T $')
ylabel('thrust in N')
legend('Thrust front','Thrust rear');

subplot(3,1,2)
hold on
plot(time,rad2deg(theta_Fdot),'r')

subplot(3,1,2)
plot(time,rad2deg(theta_Rdot),'b')
title('$ \theta  dot $')
ylabel('steer rate in deg/s')
legend('steer front','steer rear');


subplot(3,1,3)
hold on
plot(tarray,rad2deg(theta_Farray),'r')
plot(tarray,rad2deg(theta_Rarray),'b')
title('$ \theta steer angles $')
ylabel('steer angle in degrees')
legend('front', 'rear')
movegui('south')






end