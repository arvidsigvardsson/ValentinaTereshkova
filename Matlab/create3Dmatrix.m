function create3Dmatrix(c1, c2, c3, c4, c5, c6)
    [X, Y] = meshgrid(0:5:400);
    
    R = c1*X.^2 + c2.*X + c3 + c4*Y.^2 + c5.*Y + c6;
    
    Z = R;
    
    %M = zeros(400, 400);
    %for k=1:400
    %    for n=1:400
    %        M(n,k) = x_axis(n) + y_axis(k);
    %    end
    %end
    surf(X, Y, Z)
end