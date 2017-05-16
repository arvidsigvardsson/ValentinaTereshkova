function totalError(c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12)

    [X, Y] = meshgrid(0:5:400);

    R = sqrt((c1*X.^2 + c2.*X + c3 + c4*Y.^2 + c5.*Y + c6).^2 + (c7*X.^2 + c8.*X + c9 + c10*Y.^2 + c11.*Y + c12).^2);

    Z = R;
    
    surf(X,Y,Z)
end