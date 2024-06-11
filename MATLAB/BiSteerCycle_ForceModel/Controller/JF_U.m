function JF_U = JF_U(I22,I33,V,df,dr,h,m,phi,psi,theta_F,theta_R)
%JF_U
%    JF_U = JF_U(I22,I33,V,DF,DR,H,M,PHI,PSI,theta_F,theta_R)

%    This function was generated by the Symbolic Math Toolbox version 23.2.
%    22-May-2024 12:31:19

%jacobian of F vecor with control input U
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
t15 = t2.^2;
t16 = t2.^3;
t18 = t2.^5;
t20 = t4.^2;
t21 = t5.^2;
t22 = t5.^3;
t23 = t5.^5;
t24 = t6.^2;
t25 = t10.^2;
t26 = t10.^3;
t27 = t11.^2;
t28 = t11.^3;
t30 = t11.^5;
t31 = t11.*-1.0;
t33 = df.*t3;
t34 = dr.*t3;
t35 = df.*t7;
t36 = dr.*t7;
t37 = t2.*t3;
t38 = t2.*t7;
t39 = t3.*t11;
t40 = t7.*t11;
t41 = t10.*t11;
t42 = 1.0./t2;
t46 = h.*t3.*t6;
t47 = 1.0./t12;
t49 = h.*t6.*t7;
t17 = t15.^2;
t19 = t15.^3;
t29 = t27.^2;
t43 = 1.0./t20;
t44 = 1.0./t22;
t45 = 1.0./t23;
t48 = t47.^2;
t50 = t25+1.0;
t51 = t27+1.0;
t52 = I22.*t24;
t53 = I33.*t24;
t54 = -t40;
t55 = -t21;
t56 = t10+t31;
t57 = -t46;
t58 = -t49;
t59 = t21.^(5.0./2.0);
t61 = t15.*t21;
t62 = t15+t25;
t63 = t15+t27;
t65 = t15+t41;
t66 = t35+t46;
t67 = t34+t49;
t68 = t38+t39;
t60 = -t53;
t64 = 1.0./t56;
t69 = sqrt(t62);
t70 = t63.^(3.0./2.0);
t71 = t33+t58;
t72 = t36+t57;
t73 = t37+t54;
t75 = 1.0./sqrt(t63);
t79 = t55+t61+1.0;
t74 = 1.0./t69;
t76 = 1.0./t70;
t77 = t75.^5;
t78 = I33+t52+t60;
t80 = 1.0./t79.^(5.0./2.0);
t81 = df.*dr.*t19.*t22.*t69.*2.0;
t82 = df.*dr.*t17.*t22.*t70.*2.0;
t83 = V.*m.*t9.*t13.*t17.*t69;
t84 = V.*m.*t9.*t14.*t17.*t69;
t85 = V.*df.*dr.*m.*t9.*t17.*t69.*2.0;
t86 = t13.*t19.*t22.*t69;
t87 = t13.*t17.*t22.*t70;
t88 = t14.*t19.*t22.*t69;
t89 = t14.*t17.*t22.*t70;
t90 = df.*dr.*t10.*t22.*t30.*t69.*2.0;
t91 = V.*df.*dr.*m.*t5.*t10.*t17.*t69.*-2.0;
t93 = t10.*t13.*t22.*t30.*t69;
t94 = t10.*t14.*t22.*t30.*t69;
t95 = V.*m.*t5.*t10.*t13.*t17.*t69.*-1.0;
t97 = V.*m.*t5.*t10.*t14.*t17.*t69.*-1.0;
t99 = V.*df.*h.*m.*t6.*t18.*t22.*t69;
t100 = V.*dr.*h.*m.*t6.*t18.*t22.*t69;
t101 = V.*df.*dr.*m.*t10.*t17.*t22.*t69;
t102 = t13.*t15.*t22.*t25.*t70;
t103 = t13.*t15.*t22.*t29.*t69;
t104 = t13.*t15.*t22.*t27.*t70;
t105 = t14.*t15.*t22.*t25.*t70;
t106 = t14.*t15.*t22.*t29.*t69;
t107 = t14.*t15.*t22.*t27.*t70;
t108 = t13.*t22.*t25.*t27.*t70;
t109 = t14.*t22.*t25.*t27.*t70;
t110 = df.*dr.*t15.*t22.*t25.*t70.*2.0;
t111 = df.*dr.*t15.*t22.*t29.*t69.*2.0;
t112 = df.*dr.*t17.*t22.*t27.*t69.*4.0;
t113 = df.*dr.*t15.*t22.*t27.*t70.*2.0;
t114 = df.*dr.*t22.*t25.*t27.*t70.*2.0;
t115 = V.*m.*t10.*t14.*t17.*t22.*t69;
t116 = V.*m.*t9.*t13.*t15.*t27.*t69;
t117 = V.*m.*t9.*t14.*t15.*t27.*t69;
t118 = t13.*t17.*t22.*t41.*t69;
t119 = t14.*t17.*t22.*t41.*t69;
t123 = V.*df.*dr.*m.*t9.*t15.*t27.*t69.*2.0;
t124 = V.*df.*dr.*m.*t10.*t22.*t29.*t69.*1.0;
t125 = df.*dr.*t17.*t22.*t41.*t69.*2.0;
t126 = t13.*t17.*t22.*t27.*t69.*2.0;
t127 = t14.*t17.*t22.*t27.*t69.*2.0;
t129 = V.*m.*t10.*t14.*t22.*t29.*t69.*1.0;
t130 = V.*df.*dr.*m.*t22.*t25.*t28.*t69;
t131 = V.*df.*dr.*m.*t22.*t25.*t30.*t69;
t132 = V.*df.*dr.*m.*t17.*t22.*t26.*t69.*1.0;
t133 = V.*df.*dr.*m.*t22.*t26.*t29.*t69.*1.0;
t134 = df.*dr.*t10.*t15.*t22.*t28.*t69.*4.0;
t135 = V.*df.*h.*m.*t2.*t6.*t22.*t29.*t69.*1.0;
t136 = V.*dr.*h.*m.*t2.*t6.*t22.*t29.*t69.*1.0;
t137 = V.*df.*dr.*m.*t5.*t10.*t15.*t27.*t69.*-2.0;
t139 = V.*m.*t14.*t22.*t25.*t28.*t69;
t140 = V.*m.*t14.*t22.*t25.*t30.*t69;
t141 = V.*m.*t14.*t17.*t22.*t26.*t69.*1.0;
t142 = V.*m.*t14.*t22.*t26.*t29.*t69.*1.0;
t143 = t10.*t13.*t15.*t22.*t28.*t69.*2.0;
t144 = t10.*t14.*t15.*t22.*t28.*t69.*2.0;
t145 = V.*df.*h.*m.*t2.*t6.*t10.*t22.*t28.*t69;
t146 = V.*df.*h.*m.*t6.*t16.*t22.*t41.*t69;
t147 = V.*df.*h.*m.*t2.*t6.*t10.*t22.*t30.*t69;
t148 = V.*dr.*h.*m.*t2.*t6.*t10.*t22.*t28.*t69;
t149 = V.*dr.*h.*m.*t6.*t16.*t22.*t41.*t69;
t150 = V.*dr.*h.*m.*t2.*t6.*t10.*t22.*t30.*t69;
t151 = V.*m.*t5.*t10.*t13.*t15.*t27.*t69.*-1.0;
t153 = V.*m.*t5.*t10.*t14.*t15.*t27.*t69.*-1.0;
t155 = V.*df.*h.*m.*t6.*t16.*t22.*t27.*t69;
t156 = V.*df.*h.*m.*t6.*t16.*t22.*t29.*t69;
t158 = V.*dr.*h.*m.*t6.*t16.*t22.*t27.*t69;
t159 = V.*dr.*h.*m.*t6.*t16.*t22.*t29.*t69;
t161 = V.*df.*dr.*m.*t10.*t15.*t22.*t27.*t69;
t162 = V.*df.*dr.*m.*t11.*t15.*t22.*t25.*t69;
t163 = V.*df.*dr.*m.*t10.*t15.*t22.*t29.*t69;
t166 = V.*m.*t10.*t14.*t15.*t22.*t27.*t69;
t167 = V.*m.*t11.*t14.*t15.*t22.*t25.*t69;
t175 = V.*df.*h.*m.*t6.*t10.*t16.*t22.*t28.*t69;
t176 = V.*dr.*h.*m.*t6.*t10.*t16.*t22.*t28.*t69;
t179 = V.*df.*dr.*m.*t15.*t22.*t26.*t27.*t69.*2.0;
t182 = V.*m.*t14.*t15.*t22.*t26.*t27.*t69.*2.0;
t120 = t99.*1.0;
t121 = t100.*1.0;
t122 = t101.*1.0;
t128 = t115.*1.0;
t157 = t27.*t99;
t160 = t27.*t100;
t164 = t27.*t101;
t165 = t161.*2.0;
t168 = V.*m.*t10.*t106;
t169 = t27.*t115;
t171 = t155.*2.0;
t173 = t158.*2.0;
t174 = t15.*t130;
t177 = t166.*2.0;
t178 = t15.*t139;
t180 = t25.*t135;
t181 = t25.*t136;
t185 = t82+t87+t89+t102+t104+t105+t107+t108+t109+t110+t113+t114;
t186 = t81+t86+t88+t90+t93+t94+t103+t106+t111+t112+t118+t119+t125+t126+t127+t134+t143+t144;
t170 = t25.*t120;
t172 = t25.*t121;
t183 = t25.*t171;
t184 = t25.*t173;
t188 = t83+t84+t85+t91+t95+t97+t99+t100+t101+t115+t116+t117+t123+t130+t131+t137+t139+t140+t145+t146+t147+t148+t149+t150+t151+t153+t155+t156+t157+t158+t159+t160+t161+t162+t163+t164+t166+t167+t168+t169+t174+t175+t176+t178;
t187 = t120+t121+t122+t124+t128+t129+t132+t133+t135+t136+t141+t142+t165+t170+t171+t172+t173+t177+t179+t180+t181+t182+t183+t184;
mt1 = [0.0,t7.*t42.*t44.*t47.*t64.*t68.*t74.*t77.*t185.*-1.0-t3.*t42.*t44.*t47.*t64.*t73.*t74.*t77.*t185.*1.0,0.0,0.0,0.0,0.0,t3.*t12.*t68.*t75-t7.*t12.*t73.*t75-t7.*t42.*t44.*t47.*t64.*t68.*t74.*t77.*t186.*1.0-t3.*t42.*t44.*t47.*t64.*t73.*t74.*t77.*t186.*1.0,0.0,0.0,0.0,0.0,V.*t47.*t50.*t75.*t78-V.*m.*t47.*t50.*t66.*t72.*t75-V.*m.*t47.*t50.*t67.*t71.*t75+t7.*t42.*t44.*t47.*t64.*t68.*t74.*t77.*t187.*1.0+t3.*t42.*t44.*t47.*t64.*t73.*t74.*t77.*t187.*1.0];
mt2 = [-t43.*t45.*t48.*t59.*t80.*(V.*h.*m.*t2.*t5.*t14-V.*h.*m.*t2.*t14.*t22.*2.0+V.*h.*m.*t2.*t14.*t23+V.*h.*m.*t14.*t16.*t22.*2.0-V.*h.*m.*t14.*t16.*t23.*2.0+V.*h.*m.*t14.*t18.*t23+V.*df.*dr.*h.*m.*t2.*t5-V.*df.*dr.*h.*m.*t2.*t22.*2.0+V.*df.*dr.*h.*m.*t2.*t23+V.*df.*dr.*h.*m.*t16.*t22.*2.0-V.*df.*dr.*h.*m.*t16.*t23.*2.0+V.*df.*dr.*h.*m.*t18.*t23),1.0,0.0,0.0,-m.*t66.*(V.*t2.*t44.*t76.*(t3.*t9+t5.*t38)-V.*t47.*t51.*t65.*t72.*t76)+m.*t71.*(V.*t2.*t44.*t76.*(t7.*t9-t5.*t37)+V.*t47.*t51.*t65.*t67.*t76)-V.*t47.*t51.*t65.*t76.*t78-t7.*t42.*t44.*t47.*t64.*t68.*t74.*t77.*t188.*1.0-t3.*t42.*t44.*t47.*t64.*t73.*t74.*t77.*t188.*1.0];
mt3 = [-t43.*t45.*t48.*t59.*t80.*(V.*h.*m.*t5.*t13.*t16.*t20-V.*h.*m.*t13.*t16.*t20.*t22+V.*h.*m.*t13.*t18.*t20.*t22+V.*df.*dr.*h.*m.*t5.*t16.*t20-V.*df.*dr.*h.*m.*t16.*t20.*t22+V.*df.*dr.*h.*m.*t18.*t20.*t22-V.*h.*m.*t2.*t4.*t8.*t9.*t14-V.*df.*dr.*h.*m.*t2.*t4.*t8.*t9+V.*h.*m.*t2.*t4.*t8.*t9.*t14.*t21+V.*h.*m.*t4.*t8.*t9.*t14.*t16.*t55+V.*df.*dr.*h.*m.*t2.*t4.*t8.*t9.*t21+V.*df.*dr.*h.*m.*t4.*t8.*t9.*t16.*t55),0.0,1.0];
JF_U = reshape([mt1,mt2,mt3],5,4);
end
