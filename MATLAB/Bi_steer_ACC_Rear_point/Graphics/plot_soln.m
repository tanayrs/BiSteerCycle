function plot_soln(soln,start,stop,p)

disp('plotting....')

close all

tarray = linspace(start, stop, 100000);
zarray = deval(soln,tarray);

time = soln.x;
z    = soln.y;

control_array = zeros(length(time),4);

for i = 1:length(time)

    [Vfdot0, Vdot0, theta_Fdot0, theta_Rdot0] = controller_test(time(i),z(:,i),p);

    control_array(i,1) = Vfdot0;
    control_array(i,2) = Vdot0;
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

Vfdot        = control_array(:,1);
Vdot         = control_array(:,2);
theta_Fdot   = control_array(:,3);
theta_Rdot   = control_array(:,4);


V0      = V_array(1);
dV_array = V_array-V0;


figure(1)
%subplot(1,2,1)
hold on
plot(x_array,y_array);
plot(x_array(1),y_array(1),'b.',LineWidth=1.5)
plot(x_array(end),y_array(end),'r.',LineWidth=1.5)
legend('','start','end')
title('Trajectory')
xlabel('x')
ylabel('y')
axis equal
movegui('northwest')


figure(2)
subplot(2,1,1)
plot(tarray,rad2deg(phi_array),'LineWidth',1.5);
title('lean angle')
xlabel('$time(t)$');
ylabel('$\phi$ in degrees')
subplot(2,1,2)
plot(tarray,rad2deg(phidot_array),'LineWidth',1.5);
title('lean rate')
xlabel('$time(t)$');
ylabel('$\dot{\phi}$ in degrees')

movegui('southwest')

%{
figure(3)
plot(tarray,V_array);
%}

%
figure(3)
subplot(2,1,1)
plot(tarray,V_array,"LineWidth",1.5);
title('$ V_R $')
xlabel('$time(t)$');
ylabel('$\ V$ in m/s')

subplot(2,1,2)
hold on
plot(time,Vdot,'b','LineWidth',1.5);
plot(time,Vfdot,'r','LineWidth',1.5);
title('$ \dot{V} $ vs t')
xlabel('$time(t)$')
ylabel('acc in m/s2')
legend('acc rear','acc front');
movegui('north')
%}

%{
figure(4)
plot(tarray,phidot_array)
title('lean rate')
%}


figure(7)
%}
subplot(2,1,1)
hold on
plot(time,rad2deg(theta_Fdot),'r','LineWidth',1.5)
plot(time,rad2deg(theta_Rdot),'b','LineWidth',1.5)
title('$ \dot{\theta} $ vs t')
xlabel('$time(t)$')
ylabel('steer rate in deg/s')
legend('\theta_F','\theta_R');


subplot(2,1,2)
hold on
plot(tarray,rad2deg(theta_Farray),'r','LineWidth',1.5)
plot(tarray,rad2deg(theta_Rarray),'b','LineWidth',1.5)
title('$ \theta $ steer angles vs t')
xlabel('$time(t)$')
ylabel('steer angle in degrees')
legend('\theta_F', '\theta_R')
movegui('south')






end