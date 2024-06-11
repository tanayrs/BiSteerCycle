function A = A(I11,I22,I33,df,dr,h,m,phi,psi,theta_F,theta_R)
%A
%    A = A(I11,I22,I33,DF,DR,H,M,PHI,PSI,theta_F,theta_R)

%    This function was generated by the Symbolic Math Toolbox version 23.2.
%    21-May-2024 08:03:53

%Mass matrix A
t2 = cos(phi);
t3 = cos(psi);
t4 = cos(theta_F);
t5 = cos(theta_R);
t6 = sin(phi);
t7 = sin(psi);
t8 = sin(theta_F);
t9 = sin(theta_R);
t10 = tan(theta_F);
t11 = tan(theta_R);
t12 = df+dr;
t13 = df.^2;
t14 = dr.^2;
t15 = h.^2;
t16 = t2.^2;
t17 = t2.^3;
t18 = t2.^5;
t19 = t4.^2;
t20 = t5.^2;
t21 = t5.^3;
t23 = t5.^5;
t24 = t6.^2;
t25 = t10.^2;
t26 = t11.^2;
t27 = df.*t3;
t28 = dr.*t3;
t29 = df.*t7;
t30 = dr.*t7;
t31 = t2.*t3;
t32 = t2.*t7;
t33 = t3.*t10;
t34 = t3.*t11;
t35 = t7.*t10;
t36 = t7.*t11;
t39 = -t11;
t40 = h.*t3.*t6;
t41 = 1.0./t12;
t43 = h.*t6.*t7;
t22 = t20.^2;
t37 = 1.0./t19;
t38 = 1.0./t23;
t42 = t41.^2;
t44 = -t35;
t45 = -t36;
t46 = -t20;
t47 = -t40;
t48 = -t43;
t49 = t10+t39;
t50 = t20.^(5.0./2.0);
t51 = 1.0./t20.^(3.0./2.0);
t52 = t16.*t20;
t53 = t16+t25;
t54 = t16+t26;
t55 = t29+t40;
t56 = t28+t43;
t57 = t32+t33;
t58 = t32+t34;
t59 = t27+t48;
t60 = t30+t47;
t61 = t31+t44;
t62 = t31+t45;
t63 = 1.0./sqrt(t53);
t64 = 1.0./sqrt(t54);
t65 = t46+t52+1.0;
t66 = t65.^(3.0./2.0);
t67 = 1.0./t65.^(5.0./2.0);
t68 = t58.*t64;
t69 = t62.*t64;
t70 = t41.*t49.*t56.*t64;
t71 = t41.*t49.*t60.*t64;
t72 = -t71;
t73 = t68+t70;
t74 = t69+t72;
et1 = h.*m.*t2.*t9.*t13.*t19+df.*dr.*h.*m.*t2.*t9.*t19+h.*m.*t2.*t4.*t5.*t8.*t14-h.*m.*t2.*t4.*t8.*t14.*t21.*2.0+h.*m.*t2.*t4.*t8.*t14.*t23-h.*m.*t2.*t9.*t13.*t19.*t20.*2.0+h.*m.*t4.*t8.*t14.*t17.*t21.*2.0+h.*m.*t2.*t9.*t13.*t19.*t22-h.*m.*t4.*t8.*t14.*t17.*t23.*2.0+h.*m.*t4.*t8.*t14.*t18.*t23+h.*m.*t9.*t13.*t17.*t19.*t20.*2.0-h.*m.*t9.*t13.*t17.*t19.*t22.*2.0+h.*m.*t9.*t13.*t18.*t19.*t22+df.*dr.*h.*m.*t2.*t4.*t5.*t8-df.*dr.*h.*m.*t2.*t4.*t8.*t21.*2.0+df.*dr.*h.*m.*t2.*t4.*t8.*t23-df.*dr.*h.*m.*t2.*t9.*t19.*t20.*2.0+df.*dr.*h.*m.*t4.*t8.*t17.*t21.*2.0+df.*dr.*h.*m.*t2.*t9.*t19.*t22-df.*dr.*h.*m.*t4.*t8.*t17.*t23.*2.0+df.*dr.*h.*m.*t4.*t8.*t18.*t23;
et2 = df.*dr.*h.*m.*t9.*t17.*t19.*t20.*2.0-df.*dr.*h.*m.*t9.*t17.*t19.*t22.*2.0+df.*dr.*h.*m.*t9.*t18.*t19.*t22;
mt1 = [-m.*t3.*t74-m.*t7.*t73,-m.*t3.*t73+m.*t7.*t74,-m.*t55.*t74+m.*t59.*t73-t41.*t49.*t64.*(I33+I22.*t24-I33.*t24),t37.*t38.*t42.*t50.*t67.*(et1+et2),0.0,h.*m.*t3.*t31+h.*m.*t7.*t32,-h.*m.*t32.*t55-h.*m.*t31.*t59];
mt2 = [-t37.*t38.*t42.*t50.*t67.*(I11.*t13.*t19.*t21.*t51.*t66+I11.*t14.*t19.*t21.*t51.*t66-I11.*t13.*t19.*t23.*t51.*t66-I11.*t14.*t19.*t23.*t51.*t66+I11.*df.*dr.*t19.*t21.*t51.*t66.*2.0-I11.*df.*dr.*t19.*t23.*t51.*t66.*2.0+I11.*t13.*t16.*t19.*t23.*t51.*t66+I11.*t14.*t16.*t19.*t23.*t51.*t66+m.*t13.*t15.*t19.*t21.*t51.*t66+m.*t14.*t15.*t19.*t21.*t51.*t66-m.*t13.*t15.*t19.*t23.*t51.*t66-m.*t14.*t15.*t19.*t23.*t51.*t66+I11.*df.*dr.*t16.*t19.*t23.*t51.*t66.*2.0+df.*dr.*m.*t15.*t19.*t21.*t51.*t66.*2.0-df.*dr.*m.*t15.*t19.*t23.*t51.*t66.*2.0+m.*t13.*t15.*t16.*t19.*t23.*t51.*t66+m.*t14.*t15.*t16.*t19.*t23.*t51.*t66+df.*dr.*m.*t15.*t16.*t19.*t23.*t51.*t66.*2.0),-t3.*t57.*t63+t7.*t61.*t63,t3.*t61.*t63+t7.*t57.*t63,0.0,0.0];
mt3 = [-t3.*t68+t7.*t69,t3.*t69+t7.*t68,-t3.*t12.*t69-t7.*t12.*t68,0.0];
A = reshape([mt1,mt2,mt3],4,4);
end
