function signal = bang_bang_smoothing(ti,tf,t,control_signal)


dt = tf-ti;

t= t-ti;

signal = ((3*(t^2)/(dt^2))-(2*(t^3)/(dt^3)))*control_signal;


if t+ti>tf
    signal = control_signal;
end

end