function [state_r,K] = ref(t,z,p,Vr,theta_Fr,theta_Rr,Q,R)

state_r = [V,theta_F,theta_R];

[K,~,~] = my_lqr(t,z,p,state_r,Q,R);


end