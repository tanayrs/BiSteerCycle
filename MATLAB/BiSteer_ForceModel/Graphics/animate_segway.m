function animate(soln,tend,speed)


R=eye(2);
l=0.15;

t=0.006; %pendulum thickness
p=[t*ones(1,10);linspace(-0.01,l,10)]';%[0,l]';
p1=[-t*ones(1,10);linspace(-0.01,l,10)]';
base=[linspace(-t,t,10);-0.01*ones(1,10)]';
top=[linspace(-t,t,10);l*ones(1,10)]';
%{
driver_low=[linspace(-4*t,4*t,10);0.1*ones(1,10)]';
driver_top=[linspace(-4*t,4*t,10);0.035*ones(1,10)]';
driver_left=[4*t*ones(1,10);linspace(0.035,0.1,10)]';
driver_right=[-4*t*ones(1,10);linspace(0.035,0.1,10)]';
%}


figure(10)
%movegui("north")
figure(11)
%movegui("north")
%i=1;


radious=0.04;
wheel_thickness=0.008;
ground=[linspace(-0.5,0.5,10);-radious*ones(1,10)]';
theta_c=0:0.02:2*pi;   %angle arry for circle
wheel=radious*[cos(theta_c);sin(theta_c)]';
wheel_inner=(radious-wheel_thickness)*[cos(theta_c);sin(theta_c)]';
spoke=[linspace(-radious+wheel_thickness,radious-wheel_thickness,10);zeros(1,10)]';


s0=spoke;
s45=spoke*[cos(pi/4),-sin(pi/4);sin(pi/4),cos(pi/4)];
s90=spoke*[cos(pi/2),-sin(pi/2);sin(pi/2),cos(pi/2)];
s135=spoke*[cos(3*pi/4),-sin(3*pi/4);sin(3*pi/4),cos(3*pi/4)];





tic
t1=toc*speed;

while t1<tend

    clf


    z=deval(soln,t1);
    theta=z(1);
    phi=z(2);
    
    x=-radious*phi;

    
    c=[x,0];
    R=[cos(theta),-sin(theta);sin(theta),cos(theta)]';  %lean angle matrix
    R_phi=[cos(phi),-sin(phi);sin(phi),cos(phi)]';   %wheel rotation matrix  %theta+phi
    %R_phi=R_phi/norm(R_phi);


    %drawing wheel and spokes 
    wheel_d=wheel*R_phi;
    wheel_inner_d=wheel_inner*R_phi;
    s_0=s0*R_phi;
    s_45=s45*R_phi;
    s_90=s90*R_phi;
    s_135=s135*R_phi;

    %p1=c'+p;



    r=p*R;
    r1=p1*R;
    base_d=base*R;
    top_d=top*R;

    %{
    driver_rightd=driver_right*R;
    driver_leftd=driver_left*R;
    driver_topd=driver_top*R;
    driver_lowd=driver_low*R;
    %}



    %figure(3)
    hold on

    %plot(r(1),r(2),'r.',MarkerSize=30);
    %quiver(c(1),0,r(1),r(2),'b',LineWidth=2,ShowArrowHead='off')
    plot(c(1)+r(:,1),r(:,2),'b',LineWidth=1.5)
    plot(c(1)+r1(:,1),r1(:,2),'b',LineWidth=1.5)
    plot(c(1)+base_d(:,1),base_d(:,2),'b',LineWidth=1.5)
    plot(c(1)+top_d(:,1),top_d(:,2),'b',LineWidth=1.5)

    %{
    plot(c(1)+driver_rightd(:,1),driver_rightd(:,2),'b',LineWidth=1.5)
    plot(c(1)+driver_leftd(:,1),driver_leftd(:,2),'b',LineWidth=1.5)
    plot(c(1)+driver_lowd(:,1),driver_lowd(:,2),'b',LineWidth=1.5)
    plot(c(1)+driver_topd(:,1),driver_topd(:,2),'b',LineWidth=1.5)
    %}
    

    plot(c(1)+wheel_d(:,1),wheel_d(:,2),'r',LineWidth=1.5)
    plot(c(1)+wheel_inner_d(:,1),wheel_inner_d(:,2),'k',LineWidth=1.5)
    plot(c(1)+s_0(:,1),s_0(:,2),'b',LineWidth=1.5)
    plot(c(1)+s_45(:,1),s_45(:,2),'k',LineWidth=1.5)
    plot(c(1)+s_90(:,1),s_90(:,2),'b',LineWidth=1.5)
    plot(c(1)+s_135(:,1),s_135(:,2),'k',LineWidth=1.5)
    plot(c(1)+ground(:,1),ground(:,2),'k',LineWidth=1.5)
    
    axis equal
    %axis([-0.05 0.05 0 0.2]);
    limit1=max(c(1)+wheel(:,1));
    limit2=min(c(1)+wheel(:,1));
    %limit1=norm(limit1);
    %limit2=norm(limit2);

    %limit=max([limit1,limit2])

   


    axis([limit2-0.1 limit1+0.1 -0.05 l+0.05]);
    ylabel('$y$')
    xlabel('$x$')
   
    drawnow
    
    t1=toc*speed;



end





end