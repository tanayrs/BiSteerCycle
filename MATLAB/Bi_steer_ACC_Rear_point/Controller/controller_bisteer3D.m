function [Vfdot,Vdot, theta_Fdot, theta_Rdot] = controller_bisteer3D(t,z,p)

%z0 = [x0, y0, V0, psi0, phi0, phidot0, theta_R0, theta_F0]';
%psidot = (V*sin(theta_F - theta_R))/(cos(theta_F)*(df + dr))



x   = z(1);
y   = z(2);
V   = z(3);
psi = z(4);
phi = z(5);
phidot = z(6);
theta_F = z(7);
theta_R = z(8);


%{
if norm(phi) > deg2rad(2)

    state_ref = p.ref_phi;
    K = p.K_phi;
    disp('phi')
end


if norm(phi) < deg2rad(2)
    state_ref = p.ref_theta_F;
    K = p.K_theta_F;
    %disp('V')
    %{
    if norm(V) < 0.025
        state_ref = p.ref_theta_F;
        K = p.K_theta_F;
        disp('F')
    end
    %}
end

%}

if t >= 0 && t<=10

    state_ref = p.ref_1;
    K = p.K_1;

end

%
if t >10 && t <=20
     state_ref = p.ref_2;
     K = p.K_2;
end

%

if t> 20 && t <=30

    state_ref = p.ref_3;
    K = p.K_3;
end

%
if t> 30 && t<=40
        state_ref = [1,0,0];
        K = p.K_4;        
end

%
if t > 40 && t <=50
    state_ref = [1,0.3*sin(1*(t-40)),0];
    K = p.K_4;
    %[K,~,~] = my_lqr(t,z,p,state_ref,Q,R);

end
%

if t >50 && t <=55 && theta_F <= deg2rad(1) 
    state_ref = p.ref_phi;
    K = p.K_phi;
    %K = p.K_4;
end

if t >50 && t <=55 && theta_F > deg2rad(1)
     state_ref = [1,0.3*sin(1*(t-40)),0];
     K = p.K_4;
end

%
if t > 55
    state_ref = [0.1,0,0];
    K=p.K_4;
end
%{
if t >58 && t <=65
    state_ref = p.ref_theta_F;
    K= p.K_theta_F;
end

if t> 65 && t<=70
    state_ref=p.ref_theta_R;
    K = p.K_theta_R;
end

if t>70 && t<= 75
    state_ref=p.ref_theta_F
    K = p.K_theta_F
end

if t > 75

    state_ref=p.ref_theta_R;
    K=p.K_theta_R;

end

%}







%{
state_ref = p.ref_theta_F;
K = p.K_theta_F;
%}

%}
Vr       = state_ref(1);
theta_Fr = state_ref(2);
theta_Rr = state_ref(3);
%}


error = [   -phi,    Vr-V,  -phidot,  theta_Fr-theta_F, theta_Rr-theta_R]';



%state_lin    = [   phi,    V,  phidot,    theta_F,    theta_R];
%u            = [Tf, Tr, theta_Fdot, theta_Rdot]';
%
%lqr




%K = my_lqr(t,z,p)


U = K*error;
%{
if norm(U(2)) > deg2rad(20)
    U(2) = sign(U(2))*deg2rad(20);
end

if norm(U(3)) > deg2rad(20)
    U(3) = sign(U(3))*deg2rad(20);
end
%}
Vdot = U(1);
Vfdot = (Vdot*(cos(phi)^2 + tan(theta_F)^2)^(1/2))/(cos(phi)^2 + tan(theta_R)^2)^(1/2);

theta_Fdot = U(2);%0.5*cos(t);%-Kd*phidot;%cos(t);
theta_Rdot = U(3);%0.5*sin(t);









%{\
if t >=0 && t <=1
    %theta_Fdot = bang_bang_smoothing(0,1,t,theta_Fdot);
end


if t >= 10 && t <= 11

    theta_Fdot = bang_bang_smoothing(10,11,t,theta_Fdot);
    theta_Rdot = bang_bang_smoothing(10,11,t,theta_Rdot);
end

if t>= 20 && t<=24
    theta_Rdot = bang_bang_smoothing(20,21,t,theta_Rdot);
end


%}



%{
if theta_F ~= deg2rad(90) || theta_F ~= deg2rad(-90) || norm(Tr) > 1e-3
    Tf = Tr*cos(theta_F)/cos(theta_R);
end
%}

if abs(theta_F) <= deg2rad(92) && abs(theta_F) >= deg2rad(88) && abs(abs(theta_R)-abs(theta_F)) >= deg2rad(2) 
    %Tr = 0;
end

if abs(theta_R) <= deg2rad(92) && abs(theta_R) >= deg2rad(88) && abs(abs(theta_R)-abs(theta_F)) >= deg2rad(2)
    %Tf = 0;
end


%{
if norm(theta_F - theta_R) <=deg2rad(2)
    Tf = U(4);
end
%}




end