function B_linear = B_matrix(I11,I22,I33,V,df,dr,h,m,phi,theta_F,theta_R)
%B_matrix
%    B_linear = B_matrix(I11,I22,I33,V,DF,DR,H,M,PHI,theta_F,theta_R)

%    This function was generated by the Symbolic Math Toolbox version 23.2.
%    13-Apr-2024 22:28:26

t2 = cos(phi);
t3 = cos(theta_F);
t4 = cos(theta_R);
t5 = sin(phi);
t6 = sin(theta_F);
t7 = sin(theta_R);
t8 = df+dr;
t9 = df.^2;
t10 = df.^3;
t12 = dr.^2;
t13 = dr.^3;
t15 = h.^2;
t16 = h.^3;
t18 = m.^2;
t11 = t9.^2;
t14 = t12.^2;
t17 = t15.^2;
t19 = t2.^2;
t20 = t2.^3;
t21 = t3.^2;
t22 = t3.^3;
t24 = t3.^5;
t25 = t4.^2;
t26 = t4.^3;
t27 = 1.0./t8;
t40 = I11.*I22.*V.*df.*t3.*t4.*t7;
t41 = I11.*I22.*V.*dr.*t3.*t4.*t7;
t59 = I11.*V.*df.*m.*t3.*t4.*t7.*t12;
t60 = I11.*V.*df.*m.*t3.*t4.*t7.*t15;
t61 = I22.*V.*df.*m.*t3.*t4.*t7.*t15;
t62 = I11.*V.*dr.*m.*t3.*t4.*t7.*t15;
t63 = I22.*V.*dr.*m.*t3.*t4.*t7.*t15;
t142 = V.*df.*t3.*t4.*t7.*t12.*t15.*t18;
t23 = t21.^2;
t28 = t27.^2;
t29 = I11.*I22.*t22;
t31 = I11.*I22.*t3.*t25;
t32 = I11.*m.*t9.*t22;
t34 = I11.*m.*t15.*t22;
t36 = I22.*m.*t15.*t22;
t38 = t17.*t18.*t22;
t44 = I11.*I33.*t19.*t22;
t46 = I11.*I22.*t21.*t25;
t49 = I11.*m.*t3.*t12.*t25;
t50 = I11.*m.*t3.*t15.*t25;
t51 = I22.*m.*t3.*t15.*t25;
t52 = t3.*t17.*t18.*t25;
t54 = I11.*I33.*t3.*t19.*t25;
t68 = I33.*m.*t15.*t19.*t22;
t72 = I11.*m.*t12.*t21.*t25;
t73 = I11.*m.*t12.*t22.*t25;
t75 = I11.*m.*t15.*t21.*t25;
t76 = I22.*m.*t15.*t21.*t25;
t77 = I11.*I22.*t4.*t6.*t7.*t21.*2.0;
t79 = t9.*t15.*t18.*t22;
t82 = V.*df.*t3.*t4.*t7.*t17.*t18;
t83 = V.*dr.*t3.*t4.*t7.*t17.*t18;
t90 = t17.*t18.*t21.*t25;
t91 = t19.*t40;
t92 = I11.*I33.*V.*df.*t3.*t4.*t7.*t19;
t93 = t19.*t41;
t94 = I11.*I33.*V.*dr.*t3.*t4.*t7.*t19;
t96 = I11.*I33.*t19.*t21.*t25;
t101 = I33.*m.*t3.*t15.*t19.*t25;
t116 = I22.*V.*h.*m.*t2.*t4.*t9.*t21;
t117 = I22.*V.*h.*m.*t2.*t4.*t12.*t21;
t118 = I22.*V.*df.*dr.*h.*m.*t2.*t4.*t21.*2.0;
t123 = I11.*df.*dr.*m.*t4.*t6.*t7.*t21.*2.0;
t124 = I11.*df.*dr.*m.*t4.*t6.*t7.*t22.*2.0;
t125 = t3.*t12.*t15.*t18.*t25;
t134 = I11.*m.*t4.*t6.*t7.*t15.*t21.*2.0;
t136 = I22.*m.*t4.*t6.*t7.*t15.*t21.*2.0;
t140 = I11.*I33.*t4.*t6.*t7.*t19.*t21.*2.0;
t149 = t12.*t15.*t18.*t21.*t25;
t150 = t12.*t15.*t18.*t22.*t25;
t152 = t19.*t60;
t153 = t19.*t61;
t154 = I33.*V.*df.*m.*t3.*t4.*t7.*t15.*t19;
t155 = t19.*t62;
t156 = t19.*t63;
t157 = I33.*V.*dr.*m.*t3.*t4.*t7.*t15.*t19;
t164 = I33.*m.*t15.*t19.*t21.*t25;
t165 = I11.*df.*dr.*m.*t19.*t22.*t25.*2.0;
t167 = I11.*df.*h.*m.*t2.*t4.*t5.*t7.*t22.*2.0;
t169 = I11.*dr.*h.*m.*t2.*t4.*t5.*t7.*t22.*2.0;
t175 = t4.*t6.*t7.*t17.*t18.*t21.*2.0;
t177 = I22.*V.*h.*m.*t4.*t9.*t20.*t21;
t178 = I33.*V.*h.*m.*t4.*t9.*t20.*t21;
t179 = I22.*V.*h.*m.*t4.*t12.*t20.*t21;
t180 = I33.*V.*h.*m.*t4.*t12.*t20.*t21;
t181 = I22.*V.*df.*dr.*h.*m.*t4.*t20.*t21.*2.0;
t182 = I33.*V.*df.*dr.*h.*m.*t4.*t20.*t21.*2.0;
t201 = V.*t2.*t4.*t9.*t16.*t18.*t21;
t202 = V.*t2.*t4.*t12.*t16.*t18.*t21;
t203 = V.*df.*dr.*t2.*t4.*t16.*t18.*t21.*2.0;
t216 = df.*dr.*t4.*t6.*t7.*t15.*t18.*t21.*2.0;
t217 = df.*dr.*t4.*t6.*t7.*t15.*t18.*t22.*2.0;
t218 = I11.*df.*h.*m.*t2.*t5.*t6.*t21.*t25.*2.0;
t219 = I11.*df.*h.*m.*t2.*t5.*t6.*t22.*t25.*2.0;
t220 = I11.*dr.*h.*m.*t2.*t5.*t6.*t21.*t25.*2.0;
t221 = I11.*dr.*h.*m.*t2.*t5.*t6.*t22.*t25.*2.0;
t223 = df.*t2.*t4.*t5.*t7.*t16.*t18.*t22.*2.0;
t225 = dr.*t2.*t4.*t5.*t7.*t16.*t18.*t22.*2.0;
t227 = V.*t4.*t9.*t16.*t18.*t20.*t21;
t228 = V.*t4.*t12.*t16.*t18.*t20.*t21;
t229 = V.*df.*dr.*t4.*t16.*t18.*t20.*t21.*2.0;
t235 = I33.*m.*t4.*t6.*t7.*t15.*t19.*t21.*2.0;
t243 = t19.*t142;
t245 = df.*dr.*t15.*t18.*t19.*t22.*t25.*2.0;
t254 = df.*t2.*t5.*t6.*t16.*t18.*t21.*t25.*2.0;
t255 = df.*t2.*t5.*t6.*t16.*t18.*t22.*t25.*2.0;
t256 = dr.*t2.*t5.*t6.*t16.*t18.*t21.*t25.*2.0;
t257 = dr.*t2.*t5.*t6.*t16.*t18.*t22.*t25.*2.0;
t262 = df.*dr.*t4.*t6.*t7.*t15.*t18.*t19.*t21.*-2.0;
t263 = df.*dr.*t4.*t6.*t7.*t15.*t18.*t19.*t22.*-2.0;
t30 = I11.*I22.*t23;
t33 = I11.*m.*t9.*t23;
t35 = I11.*m.*t15.*t23;
t37 = I22.*m.*t15.*t23;
t39 = t17.*t18.*t23;
t42 = t19.*t29;
t45 = I11.*I33.*t19.*t23;
t47 = t25.*t29.*2.0;
t53 = t19.*t31;
t64 = t19.*t34;
t66 = t19.*t36;
t69 = I33.*m.*t15.*t19.*t23;
t70 = t25.*t32;
t74 = I11.*m.*t12.*t23.*t25;
t78 = t4.*t6.*t7.*t29.*2.0;
t80 = t9.*t15.*t18.*t23;
t84 = t25.*t34.*2.0;
t86 = t25.*t36.*2.0;
t88 = t19.*t38;
t95 = t19.*t46;
t97 = -t77;
t99 = t19.*t50;
t100 = t19.*t51;
t108 = -t73;
t114 = t25.*t38.*2.0;
t121 = t25.*t44.*2.0;
t126 = t19.*t52;
t135 = t4.*t6.*t7.*t34.*2.0;
t137 = t4.*t6.*t7.*t36.*2.0;
t138 = t19.*t77;
t141 = t4.*t6.*t7.*t44.*2.0;
t145 = t19.*t79;
t147 = t25.*t79;
t151 = t12.*t15.*t18.*t23.*t25;
t160 = t19.*t73;
t162 = t19.*t75;
t163 = t19.*t76;
t166 = I11.*df.*dr.*m.*t19.*t23.*t25.*2.0;
t168 = I11.*df.*h.*m.*t2.*t4.*t5.*t7.*t23.*2.0;
t170 = I11.*dr.*h.*m.*t2.*t4.*t5.*t7.*t23.*2.0;
t171 = -t134;
t173 = -t136;
t176 = t4.*t6.*t7.*t38.*2.0;
t183 = -t140;
t186 = t19.*t82;
t187 = t19.*t83;
t192 = t25.*t68.*2.0;
t194 = -t167;
t196 = -t169;
t198 = t19.*t90;
t199 = -t175;
t208 = -t150;
t222 = t19.*t125;
t224 = df.*t2.*t4.*t5.*t7.*t16.*t18.*t23.*2.0;
t226 = dr.*t2.*t4.*t5.*t7.*t16.*t18.*t23.*2.0;
t231 = t19.*t134;
t233 = t19.*t136;
t236 = t4.*t6.*t7.*t68.*2.0;
t237 = t19.*t175;
t239 = -t223;
t241 = -t225;
t244 = t19.*t149;
t246 = df.*dr.*t15.*t18.*t19.*t23.*t25.*2.0;
t247 = -t235;
t252 = t19.*t150.*2.0;
t258 = -t243;
t43 = t19.*t30;
t48 = t25.*t30.*2.0;
t55 = -t42;
t57 = -t47;
t65 = t19.*t35;
t67 = t19.*t37;
t71 = t25.*t33;
t81 = -t53;
t85 = t25.*t35.*2.0;
t87 = t25.*t37.*2.0;
t89 = t19.*t39;
t98 = -t78;
t102 = -t64;
t104 = -t66;
t106 = -t70;
t109 = -t74;
t110 = -t84;
t112 = -t86;
t115 = t25.*t39.*2.0;
t119 = t25.*t42.*2.0;
t122 = t25.*t45.*2.0;
t127 = -t88;
t129 = -t114;
t131 = -t95;
t132 = -t121;
t139 = t4.*t6.*t7.*t42.*2.0;
t143 = -t99;
t144 = -t100;
t146 = t19.*t80;
t148 = t25.*t80;
t158 = t19.*t70;
t161 = t19.*t74;
t172 = -t135;
t174 = -t137;
t184 = -t141;
t185 = -t126;
t188 = t25.*t64.*2.0;
t190 = t25.*t66.*2.0;
t193 = t25.*t69.*2.0;
t195 = -t168;
t197 = -t170;
t200 = -t176;
t204 = -t145;
t206 = -t147;
t209 = -t151;
t210 = -t162;
t211 = -t163;
t212 = -t192;
t214 = t25.*t88.*2.0;
t230 = -t198;
t232 = t4.*t6.*t7.*t64.*2.0;
t234 = t4.*t6.*t7.*t66.*2.0;
t238 = t4.*t6.*t7.*t88.*2.0;
t240 = -t224;
t242 = -t226;
t248 = -t236;
t249 = -t222;
t250 = t25.*t145.*2.0;
t253 = t19.*t151.*2.0;
t259 = -t244;
t56 = -t43;
t58 = -t48;
t103 = -t65;
t105 = -t67;
t107 = -t71;
t111 = -t85;
t113 = -t87;
t120 = t25.*t43.*2.0;
t128 = -t89;
t130 = -t115;
t133 = -t122;
t159 = t19.*t71;
t189 = t25.*t65.*2.0;
t191 = t25.*t67.*2.0;
t205 = -t146;
t207 = -t148;
t213 = -t193;
t215 = t25.*t89.*2.0;
t251 = t25.*t146.*2.0;
t264 = t29+t31+t32+t34+t36+t38+t44+t49+t50+t51+t52+t54+t55+t57+t68+t79+t81+t97+t101+t102+t104+t106+t108+t110+t112+t119+t123+t125+t127+t129+t132+t138+t143+t144+t158+t160+t165+t171+t173+t183+t185+t188+t190+t194+t196+t199+t204+t206+t208+t212+t214+t216+t218+t220+t231+t233+t237+t239+t241+t245+t247+t249+t250+t252+t254+t256+t262;
t265 = 1.0./t264;
t266 = t30+t33+t35+t37+t39+t45+t46+t56+t58+t69+t72+t75+t76+t80+t90+t96+t98+t103+t105+t107+t109+t111+t113+t120+t124+t128+t130+t131+t133+t139+t149+t159+t161+t164+t166+t172+t174+t184+t189+t191+t195+t197+t200+t205+t207+t209+t210+t211+t213+t215+t217+t219+t221+t230+t232+t234+t238+t240+t242+t246+t248+t251+t253+t255+t257+t259+t263;
t267 = 1.0./t266;
et1 = -t40-t41+t59-t60-t61-t62-t63-t82-t83+t91-t92+t93-t94+t142+t152+t153-t154+t155+t156-t157+t186+t187+t258+V.*h.*t2.*t5.*t49+I11.*I22.*V.*df.*t6.*t25+I11.*I22.*V.*dr.*t6.*t25+I11.*V.*m.*t6.*t13.*t25+V.*df.*t6.*t17.*t18.*t25+V.*dr.*t6.*t17.*t18.*t25+V.*t6.*t13.*t15.*t18.*t25-I11.*I22.*V.*df.*t6.*t19.*t25+I11.*I33.*V.*df.*t6.*t19.*t25-I11.*I22.*V.*dr.*t6.*t19.*t25+I11.*I33.*V.*dr.*t6.*t19.*t25+I11.*V.*df.*m.*t6.*t12.*t25+I11.*V.*df.*m.*t6.*t15.*t25+I22.*V.*df.*m.*t6.*t15.*t25+I11.*V.*dr.*m.*t6.*t15.*t25+I22.*V.*dr.*m.*t6.*t15.*t25+V.*df.*t6.*t12.*t15.*t18.*t25;
et2 = -V.*df.*t6.*t17.*t18.*t19.*t25-V.*dr.*t6.*t17.*t18.*t19.*t25-V.*t6.*t13.*t15.*t18.*t19.*t25-I11.*V.*df.*m.*t6.*t15.*t19.*t25-I22.*V.*df.*m.*t6.*t15.*t19.*t25+I33.*V.*df.*m.*t6.*t15.*t19.*t25+I11.*V.*dr.*m.*t3.*t4.*t7.*t9-I11.*V.*dr.*m.*t6.*t15.*t19.*t25-I22.*V.*dr.*m.*t6.*t15.*t19.*t25+I33.*V.*dr.*m.*t6.*t15.*t19.*t25-V.*df.*t6.*t12.*t15.*t18.*t19.*t25+V.*dr.*t3.*t4.*t7.*t9.*t15.*t18+V.*t2.*t3.*t5.*t9.*t16.*t18.*t25+V.*t2.*t3.*t5.*t12.*t16.*t18.*t25+I11.*V.*h.*m.*t2.*t3.*t5.*t9.*t25+V.*df.*dr.*t2.*t3.*t5.*t16.*t18.*t25.*2.0-V.*dr.*t3.*t4.*t7.*t9.*t15.*t18.*t19+I11.*V.*df.*dr.*h.*m.*t2.*t3.*t5.*t25.*2.0;
et3 = t40+t41+t59+t60+t61+t62+t63+t82+t83-t91+t92-t93+t94+t142-t152-t153+t154-t155-t156+t157-t186-t187+t258+V.*df.*t6.*t46.*2.0-V.*df.*t6.*t72.*2.0+V.*df.*t6.*t75.*2.0+V.*df.*t6.*t76.*2.0+V.*df.*t6.*t90.*2.0-V.*df.*t6.*t95.*2.0+V.*df.*t6.*t96.*2.0-V.*df.*t6.*t149.*2.0-V.*df.*t6.*t162.*2.0-V.*df.*t6.*t163.*2.0+V.*df.*t6.*t164.*2.0-V.*df.*t6.*t198.*2.0+V.*df.*t6.*t244.*2.0+V.*dr.*t6.*t46.*2.0+V.*dr.*t6.*t75.*2.0+V.*dr.*t6.*t76.*2.0+V.*dr.*t6.*t90.*2.0-V.*dr.*t6.*t95.*2.0+V.*dr.*t6.*t96.*2.0-V.*dr.*t6.*t162.*2.0-V.*dr.*t6.*t163.*2.0+V.*dr.*t6.*t164.*2.0-V.*dr.*t6.*t198.*2.0;
et4 = t5.*t6.*t7.*t201.*2.0+t5.*t6.*t7.*t202.*2.0-V.*df.*t4.*t7.*t29.*2.0-V.*df.*t4.*t7.*t34.*2.0-V.*df.*t4.*t7.*t36.*2.0-V.*df.*t4.*t7.*t38.*2.0+V.*df.*t4.*t7.*t42.*2.0-V.*df.*t4.*t7.*t44.*2.0+V.*df.*t4.*t7.*t64.*2.0+V.*df.*t4.*t7.*t66.*2.0-V.*df.*t4.*t7.*t68.*2.0+V.*df.*t4.*t7.*t88.*2.0-V.*dr.*t4.*t7.*t29.*2.0-V.*dr.*t4.*t7.*t32-V.*dr.*t4.*t7.*t34.*2.0-V.*dr.*t4.*t7.*t36.*2.0-V.*dr.*t4.*t7.*t38.*2.0+V.*dr.*t4.*t7.*t42.*2.0-V.*dr.*t4.*t7.*t44.*2.0+V.*dr.*t4.*t7.*t64.*2.0+V.*dr.*t4.*t7.*t66.*2.0-V.*dr.*t4.*t7.*t68.*2.0-V.*dr.*t4.*t7.*t79+V.*dr.*t4.*t7.*t88.*2.0+V.*dr.*t4.*t7.*t145.*4.0-V.*h.*t2.*t5.*t32;
et5 = V.*h.*t2.*t5.*t70.*2.0+V.*h.*t2.*t5.*t73.*2.0-I11.*I22.*V.*df.*t6.*t21-I11.*I22.*V.*dr.*t6.*t21-V.*df.*t6.*t17.*t18.*t21+V.*dr.*t4.*t7.*t19.*t32.*3.0-V.*dr.*t6.*t17.*t18.*t21+I11.*I22.*V.*df.*t6.*t19.*t21-I11.*I33.*V.*df.*t6.*t19.*t21+I11.*I22.*V.*dr.*t6.*t19.*t21-I11.*I33.*V.*dr.*t6.*t19.*t21+I11.*V.*df.*m.*t6.*t12.*t21-I11.*V.*df.*m.*t6.*t15.*t21-I22.*V.*df.*m.*t6.*t15.*t21+I11.*V.*dr.*m.*t6.*t9.*t21-I11.*V.*dr.*m.*t6.*t15.*t21-I22.*V.*dr.*m.*t6.*t15.*t21+I11.*V.*m.*t3.*t4.*t7.*t13-I11.*V.*m.*t4.*t7.*t10.*t22-I11.*V.*m.*t4.*t7.*t13.*t22+V.*df.*t6.*t12.*t15.*t18.*t21+V.*df.*t6.*t17.*t18.*t19.*t21;
et6 = V.*dr.*t6.*t9.*t15.*t18.*t21+V.*dr.*t6.*t17.*t18.*t19.*t21+V.*t3.*t4.*t7.*t13.*t15.*t18-V.*t2.*t5.*t9.*t16.*t18.*t22-V.*t2.*t5.*t12.*t16.*t18.*t22-V.*t4.*t7.*t10.*t15.*t18.*t22-V.*t4.*t7.*t13.*t15.*t18.*t22-I11.*V.*df.*m.*t4.*t7.*t12.*t22+I11.*V.*df.*m.*t6.*t15.*t19.*t21+I22.*V.*df.*m.*t6.*t15.*t19.*t21-I33.*V.*df.*m.*t6.*t15.*t19.*t21-I11.*V.*dr.*m.*t6.*t9.*t21.*t25.*2.0+I11.*V.*dr.*m.*t6.*t15.*t19.*t21+I22.*V.*dr.*m.*t6.*t15.*t19.*t21-I33.*V.*dr.*m.*t6.*t15.*t19.*t21-I11.*V.*h.*m.*t2.*t5.*t12.*t22+I11.*V.*m.*t4.*t7.*t10.*t19.*t22+I11.*V.*m.*t4.*t7.*t13.*t19.*t22-V.*df.*dr.*t2.*t5.*t16.*t18.*t22.*2.0-V.*df.*t4.*t7.*t12.*t15.*t18.*t22;
et7 = -V.*df.*t6.*t12.*t15.*t18.*t19.*t21-V.*dr.*t6.*t9.*t15.*t18.*t19.*t21-V.*dr.*t6.*t9.*t15.*t18.*t21.*t25.*2.0-V.*t3.*t4.*t7.*t13.*t15.*t18.*t19+V.*t4.*t7.*t10.*t15.*t18.*t19.*t22.*2.0+V.*t2.*t5.*t9.*t16.*t18.*t22.*t25.*2.0+V.*t4.*t7.*t13.*t15.*t18.*t19.*t22.*2.0+V.*t2.*t5.*t12.*t16.*t18.*t22.*t25.*2.0+I11.*V.*df.*m.*t4.*t7.*t12.*t19.*t22.*3.0+V.*df.*dr.*t2.*t5.*t16.*t18.*t22.*t25.*4.0+V.*df.*t4.*t7.*t12.*t15.*t18.*t19.*t22.*4.0+V.*dr.*t6.*t9.*t15.*t18.*t19.*t21.*t25.*2.0-I11.*V.*df.*dr.*h.*m.*t2.*t5.*t22.*2.0+I11.*V.*df.*dr.*h.*m.*t2.*t5.*t22.*t25.*4.0+V.*df.*dr.*t2.*t4.*t5.*t6.*t7.*t16.*t18.*t21.*4.0+I11.*V.*h.*m.*t2.*t4.*t5.*t6.*t7.*t9.*t21.*2.0+I11.*V.*h.*m.*t2.*t4.*t5.*t6.*t7.*t12.*t21.*2.0;
et8 = I11.*V.*df.*dr.*h.*m.*t2.*t4.*t5.*t6.*t7.*t21.*4.0;
et9 = h.*m.*t2.*t4.*t7.*t11.*t22-h.*m.*t2.*t4.*t7.*t11.*t24+h.*m.*t4.*t7.*t11.*t20.*t24+h.*m.*t2.*t6.*t14.*t21.*t25-h.*m.*t2.*t6.*t14.*t23.*t25+h.*m.*t6.*t14.*t20.*t23.*t25+df.*h.*m.*t2.*t4.*t7.*t13.*t22-df.*h.*m.*t2.*t4.*t7.*t13.*t24+df.*h.*m.*t2.*t6.*t13.*t21.*t25.*3.0+df.*h.*m.*t4.*t7.*t13.*t20.*t24-df.*h.*m.*t2.*t6.*t13.*t23.*t25.*3.0+df.*h.*m.*t6.*t13.*t20.*t23.*t25.*3.0+dr.*h.*m.*t2.*t4.*t7.*t10.*t22.*3.0-dr.*h.*m.*t2.*t4.*t7.*t10.*t24.*3.0+dr.*h.*m.*t2.*t6.*t10.*t21.*t25+dr.*h.*m.*t4.*t7.*t10.*t20.*t24.*3.0-dr.*h.*m.*t2.*t6.*t10.*t23.*t25+dr.*h.*m.*t6.*t10.*t20.*t23.*t25+h.*m.*t2.*t4.*t7.*t9.*t12.*t22.*3.0-h.*m.*t2.*t4.*t7.*t9.*t12.*t24.*3.0;
et10 = h.*m.*t2.*t6.*t9.*t12.*t21.*t25.*3.0+h.*m.*t4.*t7.*t9.*t12.*t20.*t24.*3.0-h.*m.*t2.*t6.*t9.*t12.*t23.*t25.*3.0+h.*m.*t6.*t9.*t12.*t20.*t23.*t25.*3.0;
et11 = h.*m.*t2.*t7.*t11.*t23+df.*h.*m.*t2.*t7.*t13.*t23+dr.*h.*m.*t2.*t7.*t10.*t23.*3.0+h.*m.*t2.*t4.*t6.*t14.*t22+h.*m.*t2.*t7.*t9.*t12.*t23.*3.0-h.*m.*t2.*t7.*t11.*t23.*t25-h.*m.*t2.*t6.*t14.*t22.*t26+h.*m.*t7.*t11.*t20.*t23.*t25+h.*m.*t6.*t14.*t20.*t22.*t26+df.*h.*m.*t2.*t4.*t6.*t13.*t22.*3.0-df.*h.*m.*t2.*t6.*t13.*t22.*t26.*3.0-df.*h.*m.*t2.*t7.*t13.*t23.*t25+df.*h.*m.*t6.*t13.*t20.*t22.*t26.*3.0+df.*h.*m.*t7.*t13.*t20.*t23.*t25+dr.*h.*m.*t2.*t4.*t6.*t10.*t22-dr.*h.*m.*t2.*t6.*t10.*t22.*t26-dr.*h.*m.*t2.*t7.*t10.*t23.*t25.*3.0+dr.*h.*m.*t6.*t10.*t20.*t22.*t26+dr.*h.*m.*t7.*t10.*t20.*t23.*t25.*3.0+h.*m.*t2.*t4.*t6.*t9.*t12.*t22.*3.0-h.*m.*t2.*t6.*t9.*t12.*t22.*t26.*3.0;
et12 = h.*m.*t2.*t7.*t9.*t12.*t23.*t25.*-3.0+h.*m.*t6.*t9.*t12.*t20.*t22.*t26.*3.0+h.*m.*t7.*t9.*t12.*t20.*t23.*t25.*3.0;
et13 = t116+t117+t118-t177+t178-t179+t180-t181+t182+t201+t202+t203-t227-t228-t229-V.*df.*t5.*t7.*t244.*5.0+V.*h.*t14.*t18.*t20.*t21.*t26-V.*t2.*t9.*t16.*t18.*t21.*t26-V.*t2.*t12.*t16.*t18.*t21.*t26+V.*t9.*t16.*t18.*t20.*t21.*t26+V.*t12.*t16.*t18.*t20.*t21.*t26-I22.*V.*h.*m.*t2.*t9.*t21.*t26-I22.*V.*h.*m.*t2.*t12.*t21.*t26+I22.*V.*h.*m.*t9.*t20.*t21.*t26+I22.*V.*h.*m.*t12.*t20.*t21.*t26-I33.*V.*h.*m.*t9.*t20.*t21.*t26-I33.*V.*h.*m.*t12.*t20.*t21.*t26-V.*df.*dr.*t2.*t16.*t18.*t21.*t26.*2.0+V.*df.*dr.*t16.*t18.*t20.*t21.*t26.*2.0+V.*df.*h.*t13.*t18.*t20.*t21.*t26.*3.0+V.*dr.*h.*t10.*t18.*t20.*t21.*t26+V.*h.*t9.*t12.*t18.*t20.*t21.*t26.*3.0;
et14 = -V.*t2.*t3.*t6.*t7.*t9.*t16.*t18.*t25-V.*t2.*t3.*t6.*t7.*t12.*t16.*t18.*t25+V.*t3.*t6.*t7.*t9.*t16.*t18.*t20.*t25+V.*t3.*t5.*t6.*t13.*t15.*t18.*t19.*t26+V.*t3.*t6.*t7.*t12.*t16.*t18.*t20.*t25-V.*t5.*t7.*t10.*t15.*t18.*t19.*t21.*t25-V.*t5.*t7.*t13.*t15.*t18.*t19.*t21.*t25.*2.0-I22.*V.*df.*dr.*h.*m.*t2.*t21.*t26.*2.0+I22.*V.*df.*dr.*h.*m.*t20.*t21.*t26.*2.0-I33.*V.*df.*dr.*h.*m.*t20.*t21.*t26.*2.0-I22.*V.*h.*m.*t2.*t3.*t6.*t7.*t9.*t25-I22.*V.*h.*m.*t2.*t3.*t6.*t7.*t12.*t25+I22.*V.*h.*m.*t3.*t6.*t7.*t9.*t20.*t25+I22.*V.*h.*m.*t3.*t6.*t7.*t12.*t20.*t25-I33.*V.*h.*m.*t3.*t6.*t7.*t9.*t20.*t25-I33.*V.*h.*m.*t3.*t6.*t7.*t12.*t20.*t25-V.*df.*dr.*t2.*t3.*t6.*t7.*t16.*t18.*t25.*2.0;
et15 = V.*df.*dr.*t3.*t6.*t7.*t16.*t18.*t20.*t25.*2.0+V.*df.*t3.*t5.*t6.*t12.*t15.*t18.*t19.*t26.*2.0+V.*dr.*t3.*t5.*t6.*t9.*t15.*t18.*t19.*t26-V.*dr.*t5.*t7.*t9.*t15.*t18.*t19.*t21.*t25.*4.0-I22.*V.*df.*dr.*h.*m.*t2.*t3.*t6.*t7.*t25.*2.0+I22.*V.*df.*dr.*h.*m.*t3.*t6.*t7.*t20.*t25.*2.0-I33.*V.*df.*dr.*h.*m.*t3.*t6.*t7.*t20.*t25.*2.0;
et16 = t116+t117+t118-t177+t178-t179+t180-t181+t182+t201+t202+t203-t227-t228-t229-V.*dr.*t5.*t7.*t146.*2.0+V.*dr.*t4.*t5.*t6.*t145.*5.0+V.*h.*t4.*t11.*t18.*t20.*t23-V.*t2.*t4.*t9.*t16.*t18.*t23-V.*t2.*t4.*t12.*t16.*t18.*t23+V.*t4.*t9.*t16.*t18.*t20.*t23+V.*t4.*t12.*t16.*t18.*t20.*t23-I22.*V.*h.*m.*t2.*t4.*t9.*t23-I22.*V.*h.*m.*t2.*t4.*t12.*t23+I22.*V.*h.*m.*t4.*t9.*t20.*t23+I22.*V.*h.*m.*t4.*t12.*t20.*t23-I33.*V.*h.*m.*t4.*t9.*t20.*t23-I33.*V.*h.*m.*t4.*t12.*t20.*t23-V.*df.*dr.*t2.*t4.*t16.*t18.*t23.*2.0+V.*df.*dr.*t4.*t16.*t18.*t20.*t23.*2.0+V.*df.*h.*t4.*t13.*t18.*t20.*t23+V.*dr.*h.*t4.*t10.*t18.*t20.*t23.*3.0;
et17 = V.*h.*t4.*t9.*t12.*t18.*t20.*t23.*3.0-V.*t2.*t6.*t7.*t9.*t16.*t18.*t22-V.*t2.*t6.*t7.*t12.*t16.*t18.*t22-V.*t5.*t7.*t10.*t15.*t18.*t19.*t23+V.*t6.*t7.*t9.*t16.*t18.*t20.*t22+V.*t6.*t7.*t12.*t16.*t18.*t20.*t22-I22.*V.*h.*m.*t2.*t6.*t7.*t9.*t22-I22.*V.*h.*m.*t2.*t6.*t7.*t12.*t22+I22.*V.*h.*m.*t6.*t7.*t9.*t20.*t22+I22.*V.*h.*m.*t6.*t7.*t12.*t20.*t22-I33.*V.*h.*m.*t6.*t7.*t9.*t20.*t22-I33.*V.*h.*m.*t6.*t7.*t12.*t20.*t22-V.*df.*dr.*t2.*t6.*t7.*t16.*t18.*t22.*2.0+V.*df.*dr.*t6.*t7.*t16.*t18.*t20.*t22.*2.0-V.*df.*t5.*t7.*t12.*t15.*t18.*t19.*t23+V.*t4.*t5.*t6.*t10.*t15.*t18.*t19.*t22.*2.0+V.*t4.*t5.*t6.*t13.*t15.*t18.*t19.*t22-I22.*V.*df.*dr.*h.*m.*t2.*t4.*t23.*2.0;
et18 = I22.*V.*df.*dr.*h.*m.*t4.*t20.*t23.*2.0-I33.*V.*df.*dr.*h.*m.*t4.*t20.*t23.*2.0-I22.*V.*df.*dr.*h.*m.*t2.*t6.*t7.*t22.*2.0+I22.*V.*df.*dr.*h.*m.*t6.*t7.*t20.*t22.*2.0-I33.*V.*df.*dr.*h.*m.*t6.*t7.*t20.*t22.*2.0+V.*df.*t4.*t5.*t6.*t12.*t15.*t18.*t19.*t22.*4.0;
mt1 = [0.0,t27.*t265.*(I11.*t4.*t10.*t21-I11.*t4.*t10.*t23+I11.*t4.*t13.*t21-I11.*t4.*t13.*t23+I11.*df.*t4.*t12.*t21.*3.0-I11.*df.*t4.*t12.*t23.*3.0+I11.*dr.*t4.*t9.*t21.*3.0-I11.*dr.*t4.*t9.*t23.*3.0+I11.*t4.*t10.*t19.*t23+I11.*t4.*t13.*t19.*t23+m.*t4.*t10.*t15.*t21-m.*t4.*t10.*t15.*t23+m.*t4.*t13.*t15.*t21-m.*t4.*t13.*t15.*t23+df.*m.*t4.*t12.*t15.*t21.*3.0-df.*m.*t4.*t12.*t15.*t23.*3.0+dr.*m.*t4.*t9.*t15.*t21.*3.0-dr.*m.*t4.*t9.*t15.*t23.*3.0+m.*t4.*t10.*t15.*t19.*t23+m.*t4.*t13.*t15.*t19.*t23+I11.*df.*t4.*t12.*t19.*t23.*3.0+I11.*dr.*t4.*t9.*t19.*t23.*3.0+df.*m.*t4.*t12.*t15.*t19.*t23.*3.0+dr.*m.*t4.*t9.*t15.*t19.*t23.*3.0),t28.*t267.*(et9+et10),0.0,0.0,0.0];
mt2 = [t27.*t265.*(I11.*t10.*t22+I11.*t13.*t22-I11.*t10.*t22.*t25-I11.*t13.*t22.*t25+m.*t10.*t15.*t22+m.*t13.*t15.*t22+I11.*df.*t12.*t22.*3.0+I11.*dr.*t9.*t22.*3.0-I11.*df.*t12.*t22.*t25.*3.0-I11.*dr.*t9.*t22.*t25.*3.0+I11.*t10.*t19.*t22.*t25+I11.*t13.*t19.*t22.*t25+df.*m.*t12.*t15.*t22.*3.0+dr.*m.*t9.*t15.*t22.*3.0-m.*t10.*t15.*t22.*t25-m.*t13.*t15.*t22.*t25-df.*m.*t12.*t15.*t22.*t25.*3.0-dr.*m.*t9.*t15.*t22.*t25.*3.0+m.*t10.*t15.*t19.*t22.*t25+m.*t13.*t15.*t19.*t22.*t25+I11.*df.*t12.*t19.*t22.*t25.*3.0+I11.*dr.*t9.*t19.*t22.*t25.*3.0+df.*m.*t12.*t15.*t19.*t22.*t25.*3.0+dr.*m.*t9.*t15.*t19.*t22.*t25.*3.0),t28.*t267.*(et11+et12),0.0,0.0,0.0,-t27.*t265.*(et1+et2),t28.*t267.*(et13+et14+et15),1.0,0.0,0.0];
mt3 = [t27.*t265.*(et3+et4+et5+et6+et7+et8),t28.*t267.*(et16+et17+et18),0.0,1.0];
B_linear = reshape([mt1,mt2,mt3],5,4);
end
