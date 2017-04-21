function mapping
width = 400;
height = 300;

% A = [143;555;1];
% B = [341;3416;1];
% C = [2486;3240;1];
% D = [2244;429;1];
% H = [2228;2937;1];

A = [536;824;1];
B = [384;3688;1];
C = [2560;3752;1];
D = [2608;944;1];
F = [1660;2112;1];

AD = A + 0.5*(D - A)
BC = B + 0.5*(C - B)
xscale = width / norm(BC - AD); 

AB = A + 0.5*(B - A);
CD = C + 0.5*(D - C);
yscale = height / norm(CD - AB); 

trans = [1 0 -(A(1, 1)) ; 0 1 -(A(2, 1)) ; 0 0 1]

xbase = [1;0;0];
alpha = -acos(dot(B - A, xbase) / (norm(B - A) * norm(xbase)))

rotate = [cos(alpha) -sin(alpha) 0 ; sin(alpha) cos(alpha) 0 ; 0 0 1];

scale = [xscale 0 0 ; 0 yscale 0 ; 0 0 1];

mapper = scale * rotate * trans;

mappedcoords = mapper * F
