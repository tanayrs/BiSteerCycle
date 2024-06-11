function [Tf, Tr, theta_F, theta_R, theta_Fdot, theta_Rdot] = test_controller_bisteer3D(t,z,p)

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
%{
if t >= 0 && t<=5

    state_ref = p.ref_theta_F;
    K = p.K_theta_F;

end

%
if t > 5 && t <= 10

        state_ref = p.ref_theta_R;
        K = p.K_theta_R;
end

if t> 10 && t <=15

        state_ref = p.ref_3;
        K = p.K_3;

end


if t> 15 && t <=22
        state_ref = p.ref_4;
        K = p.K_4;
        
end


if t> 22 && t <=40
    state_ref = [0.8,sin(t-22),0];
    Q = diag([1e4, 1e2, 1e4, 1e1, 1e1]);
    R = diag([1e0, 1e0, 1e0, 1e3]);
    [K,~,~] = my_lqr(t,z,p,state_ref,Q,R);

end

if t >40 && t <=45
    state_ref = p.ref_phi;
    K = p.K_phi;
end

if t > 45 && t <=58
    state_ref = p.ref_V;
    K=p.K_V;
end
%
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
%{
Vr       = state_ref(1);
theta_Fr = state_ref(2);
theta_Rr = state_ref(3);
%}


%error = [   -phi,    Vr-V,  -phidot,  theta_Fr-theta_F, theta_Rr-theta_R]';



%state_lin    = [   phi,    V,  phidot,    theta_F,    theta_R];
%u            = [Tf, Tr, theta_Fdot, theta_Rdot]';
%
%lqr




%K = my_lqr(t,z,p)


%U = K*error;

Tf = 1;
Tr = 1;%-(Kp*phi+Kd*phidot);
%Tf  = Tr*(cos(theta_R)/cos(theta_F));

disp('test')

theta_Fdot = 0;%0.5*cos(t);%-Kd*phidot;%cos(t);
theta_Rdot = 0;%0.5*sin(t);


end