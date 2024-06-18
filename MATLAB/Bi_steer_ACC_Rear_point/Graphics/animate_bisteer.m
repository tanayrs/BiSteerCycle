function animate_bisteer(soln,tstart,tend,p,speed,save)

df=p.df; dr=p.dr; m=p.m; I11=p.I11; I22=p.I22; I33=p.I33; g=p.g; %h=p.h;

h = 0.1;

i=1;

%%
%wheel

R = 0.02;
theta_vec = 0:0.02:2*pi;   %angle arry for circle
theta_vec = theta_vec';

wheel.x = R*cos(theta_vec);
wheel.y = R*zeros(length(theta_vec),1);
wheel.z = R*sin(theta_vec) + R;


%%
sprokR1.x  = zeros(1,10);
sprokR1.y  = zeros(1,10);
sprokR1.z  = linspace(0,2*R,10);

sprokR2.x = linspace(-R,R,10);
sprokR2.y = zeros(1,10);
sprokR2.z = R*ones(1,10);

sprokR3.x  = -cos(pi/4)*linspace(-R,R,10);
sprokR3.y  = zeros(1,10);
sprokR3.z  = linspace(R*(1-cos(pi/4)),R*(1+cos(pi/4)),10);

sprokR4.x  = cos(-pi/4)*linspace(-R,R,10);
sprokR4.y  = zeros(1,10);
sprokR4.z  = linspace(R*(1-cos(pi/4)),R*(1+cos(pi/4)),10);

sprokF1.x  = zeros(1,10);
sprokF1.y  = zeros(1,10);
sprokF1.z  = linspace(0,2*R,10);

sprokF2.x = linspace(-R,R,10);
sprokF2.y = zeros(1,10);
sprokF2.z = R*ones(1,10);

sprokF3.x  = -cos(pi/4)*linspace(-R,R,10);
sprokF3.y  = zeros(1,10);
sprokF3.z  = linspace(R*(1-cos(pi/4)),R*(1+cos(pi/4)),10);

sprokF4.x  = cos(-pi/4)*linspace(-R,R,10);
sprokF4.y  = zeros(1,10);
sprokF4.z  = linspace(R*(1-cos(pi/4)),R*(1+cos(pi/4)),10);



%%
frame.rod.z = linspace(R,h,10)';
frame.rod.x = zeros(10,1);
frame.rod.y = zeros(10,1);

frame.bar.x = linspace(0,(df+dr),10)';
frame.bar.y = zeros(10,1);
frame.bar.z = h*ones(10,1);

frame.bar_20.x = linspace(0,0.5*(df+dr),10)';
frame.bar_20.y = zeros(10,1);
frame.bar_20.z = linspace(2.3*R,h,10)';


wheel_R = wheel;
wheel_F = wheel;
%wheel_F.x = wheel_F.x + (df+dr);


frame.rod_R = frame.rod;
frame.rod_F = frame.rod;
frame.rod_F.z = linspace(R,1.1*h,10)';
frame.rod_F.x = frame.rod.x + (df+dr);

frame.handle.x = zeros(5,1);
frame.handle.y = linspace(-R,R,5)';
frame.handle.z = 1.1*h*ones(5,1);

%{

plot3(wheel_R.x,wheel_R.y,wheel_R.z)
hold on
plot3(wheel_F.x,wheel_F.y,wheel_F.z)
plot3(frame.rod_R.x,frame.rod_R.y,frame.rod_R.z)
plot3(frame.rod_F.x,frame.rod_F.y,frame.rod_F.z)
plot3(frame.bar.x,frame.bar.y,frame.bar.z)

%}

path_R.x = soln.y(1,:)';
path_R.y = soln.y(2,:)';
path_R.z = zeros(length(soln.x),1);

path_F.x = path_R.x + cos(soln.y(4,:)')*(df+dr);
path_F.y = path_R.y + sin(soln.y(4,:)')*(df+dr);
path_F.z = zeros(length(soln.x),1);


%figure(10)
%movegui("northeast")
figure(11)
movegui("northeast")
%i=1;



%{
s0=spoke;
s45=spoke*[cos(pi/4),-sin(pi/4);sin(pi/4),cos(pi/4)];
s90=spoke*[cos(pi/2),-sin(pi/2);sin(pi/2),cos(pi/2)];
s135=spoke*[cos(3*pi/4),-sin(3*pi/4);sin(3*pi/4),cos(3*pi/4)];

%}



tic
persistent prev_t1

prev_t1 = 0;
lr = 0;
lf = 0;

t1=tstart;%+toc*speed;

while t1<tend
    figure(11)
    dt = t1-prev_t1;
    clf
    

   %z0 = [x0,y0,V0,psi0,phi0,phidot0,theta_R0,theta_F0]';

    z  = deval(soln,t1);

    


    x     = z(1);
    y     = z(2);
    Vr    = z(3);
    
    psi   = z(4);
    %psi=0;
    phi   = z(5);
    %phi = 0;
    
    theta_F = z(7);
    theta_R = z(8);
    %theta_F = deg2rad(30);

    
    Vf    = Vr*(sqrt((cos(phi)^2 + tan(theta_F)^2)/(cos(phi^2)+ tan(theta_R)^2)));
    
    %Vf = Vr;


    %%

    lr = lr + Vr*dt;
    lf = lf + Vf*dt;
    rot_R = 0.5*lr/R;
    rot_F = 0.5*lf/R;









    %%

    sprokR1_1     = rot_y(sprokR1,rot_R);
    sprokR2_1     = rot_y(sprokR2,rot_R);
    sprokR3_1     = rot_y(sprokR3,rot_R);
    sprokR4_1     = rot_y(sprokR4,rot_R);


    sprokF1_1     = rot_y(sprokF1,rot_F);
    sprokF2_1     = rot_y(sprokF2,rot_F);
    sprokF3_1     = rot_y(sprokF3,rot_F);
    sprokF4_1     = rot_y(sprokF4,rot_F);





    sprokeR1_2    = lean_head(theta_R,phi,psi,sprokR1_1);
    sprokeR2_2    = lean_head(theta_R,phi,psi,sprokR2_1);
    sprokeR3_2    = lean_head(theta_R,phi,psi,sprokR3_1);
    sprokeR4_2    = lean_head(theta_R,phi,psi,sprokR4_1);

    sprokeF1_2    = lean_head(theta_F,phi,psi,sprokF1_1);
    sprokeF2_2    = lean_head(theta_F,phi,psi,sprokF2_1);
    sprokeF3_2    = lean_head(theta_F,phi,psi,sprokF3_1);
    sprokeF4_2    = lean_head(theta_F,phi,psi,sprokF4_1);


    wheel_R1      = lean_head(theta_R,phi,psi,wheel_R);
    wheel_F1      = lean_head(theta_F,phi,psi,wheel_R);
    handle_1      = lean_head(theta_F,phi,psi,frame.handle);



    frame.rod_R1  = lean_head(0,phi,psi,frame.rod_R);
    frame.rod_F1  = lean_head(0,phi,psi,frame.rod_F);
    frame.bar1    = lean_head(0,phi,psi,frame.bar);
    frame.bar_2   = lean_head(0,phi,psi,frame.bar_20);

    sprokeR1_2   = my_translate(sprokeR1_2,x,y,0);
    sprokeR2_2   = my_translate(sprokeR2_2,x,y,0);
    sprokeR3_2   = my_translate(sprokeR3_2,x,y,0);
    sprokeR4_2   = my_translate(sprokeR4_2,x,y,0);
    
    sprokeF1_2   = my_translate(sprokeF1_2,x+(df+dr)*cos(psi),y+(df+dr)*sin(psi),0);
    sprokeF2_2   = my_translate(sprokeF2_2,x+(df+dr)*cos(psi),y+(df+dr)*sin(psi),0);
    sprokeF3_2   = my_translate(sprokeF3_2,x+(df+dr)*cos(psi),y+(df+dr)*sin(psi),0);
    sprokeF4_2   = my_translate(sprokeF4_2,x+(df+dr)*cos(psi),y+(df+dr)*sin(psi),0);


    wheel_R2     = my_translate(wheel_R1,x,y,0);
    wheel_F2     = my_translate(wheel_F1,x+(df+dr)*cos(psi),y+(df+dr)*sin(psi),0);
    handle_2     = my_translate(handle_1,x+(df+dr)*cos(psi),y+(df+dr)*sin(psi),0);

    frame.rod_R2 = my_translate(frame.rod_R1,x,y,0);
    frame.rod_F2 = my_translate(frame.rod_F1,x,y,0);
    frame.bar2   = my_translate(frame.bar1,x,y,0);
    frame.bar_3  = my_translate(frame.bar_2,x,y,0);

    
   
    hold on
    grid on

    plot3(path_R.x,path_R.y,path_R.z,'b',LineWidth=0.1)
    plot3(path_F.x,path_F.y,path_F.z,'r',LineWidth=0.1)
%%

    min_x = min([min(wheel_R2.x),min(wheel_F2.x),min(frame.bar2.x),min(frame.rod_R2.x),min(frame.rod_F2.x)]);
    max_x = max([max(wheel_R2.x),max(wheel_F2.x),max(frame.bar2.x),max(frame.rod_R2.x),max(frame.rod_F2.x)]);

    
    min_y = min([min(wheel_R2.y),min(wheel_F2.y),min(frame.bar2.y),min(frame.rod_R2.y),min(frame.rod_F2.y)]);
    max_y = max([max(wheel_R2.y),max(wheel_F2.y),max(frame.bar2.y),max(frame.rod_R2.y),max(frame.rod_F2.y)]);
    
    delta_x = (max_x - min_x);
    delta_y = (max_y - min_y);

    delta_z = 0.3;

    x0 = min_x + delta_x/2;
    y0 = min_y + delta_y/2;

    min_x = x0 - delta_z/2;
    max_x = x0 + delta_z/2;

    min_y = y0 - delta_z/2;
    max_y = y0 + delta_z/2;

    %% plane
    x_plane = linspace(min_x,max_x);
    y_plane = linspace(min_y,max_y);

    [X,Y]   = meshgrid(x_plane,y_plane);
    Z       = zeros(size(X));


    surf(X,Y,Z,'EdgeColor','none','FaceColor',[0.9,0.9,0.9]);
    
    
    


%% plotting

    


    plot3(wheel_R2.x,wheel_R2.y,wheel_R2.z,'b',LineWidth=1.5)
    plot3(wheel_F2.x,wheel_F2.y,wheel_F2.z,'r',LineWidth=1.5)
    plot3(handle_2.x,handle_2.y,handle_2.z,'r',LineWidth=1.5)

    plot3(sprokeR1_2.x,sprokeR1_2.y,sprokeR1_2.z,'k',LineWidth=1)
    plot3(sprokeR2_2.x,sprokeR2_2.y,sprokeR2_2.z,'k',LineWidth=1)
    plot3(sprokeR3_2.x,sprokeR3_2.y,sprokeR3_2.z,'k',LineWidth=1)
    plot3(sprokeR4_2.x,sprokeR4_2.y,sprokeR4_2.z,'k',LineWidth=1)

    plot3(sprokeF1_2.x,sprokeF1_2.y,sprokeF1_2.z,'k',LineWidth=1.1)
    plot3(sprokeF2_2.x,sprokeF2_2.y,sprokeF2_2.z,'k',LineWidth=1.1)
    plot3(sprokeF3_2.x,sprokeF3_2.y,sprokeF3_2.z,'k',LineWidth=1.1)
    plot3(sprokeF4_2.x,sprokeF4_2.y,sprokeF4_2.z,'k',LineWidth=1.1)

    plot3(frame.rod_R2.x,frame.rod_R2.y,frame.rod_R2.z,'k',LineWidth=1.2)
    plot3(frame.rod_F2.x,frame.rod_F2.y,frame.rod_F2.z,'k',LineWidth=1.2)
    plot3(frame.bar2.x,frame.bar2.y,frame.bar2.z,'k',LineWidth=1.2)
    %plot3(frame.bar_3.x,frame.bar_3.y,frame.bar_3.z,'k',LineWidth=1.2)
    
   
    axis equal
    
    xlim([min_x, max_x]);
    ylim([min_y, max_y]);
    zlim([0,delta_z]);

    xlabel('x');
    ylabel('y');
    zlabel('z');
   
    view(-60,30)

    
    drawnow
    
    
    
   
    if save
        F(i) = getframe(gcf);
    end
    i=i+1;

    prev_t1 = t1;
    t1=tstart+toc*speed;




end


hold off
    if save
        filename = 'bisteer.avi';
        writerObj = VideoWriter(filename);
        writerObj.FrameRate = 30;
        % set the seconds per image
        % open the video writer
        open(writerObj);
        % write the frames to the video
        for i=1:length(F)
            % convert the image to a frame
            frame = F(i) ;    
            writeVideo(writerObj, frame);
        end
        % close the writer object
        close(writerObj);
    end



end





%{
function wheel_steered = steer(wheel,theta)

    R = [cos(theta), -sin(theta), 0
         sin(theta),  cos(theta), 0
                  0,           0, 1];





end

%}


function object_return = lean_head(theta,phi,psi,object)

    R_psi = [cos(psi), -sin(psi), 0;
             sin(psi),  cos(psi), 0;
                    0,         0, 1];

    R_phi = [1,        0,         0;
             0, cos(phi), -sin(phi);
             0, sin(phi),  cos(phi)];

    R_theta = [cos(theta), -sin(theta), 0;
               sin(theta),  cos(theta), 0;
                    0,         0,   1];


    R = R_psi*R_phi*R_theta;

    object1 = R*[object.x';object.y';object.z'];

    object_return.x = object1(1,:)';
    object_return.y = object1(2,:)';
    object_return.z = object1(3,:)';

end

function object_translated = my_translate(object,x,y,z)

object_translated.x = object.x + x;
object_translated.y = object.y + y;
object_translated.z = object.z + z;



end

function object_return = rot_y(object,rot_angle)

    

    object1 = my_translate(object,0,0,-0.02);


    theta = rot_angle;


    R = [  cos(theta), 0, sin(theta);
                0,     1,     0;
          -sin(theta), 0, cos(theta)];
    

    object1 = R*[object1.x',object1.y',object1.z']';
    object2.x = object1(1,:);
    object2.y = object1(2,:);
    object2.z = object1(3,:);
    object3 = my_translate(object2,0,0,0.02);

    object_return.x = object3.x';
    object_return.y = object3.y';
    object_return.z = object3.z';

end

