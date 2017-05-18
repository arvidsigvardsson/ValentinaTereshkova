function totalError(XX_coeffs, XY_coeffs, YY_coeffs, YX_coeffs)

    [X, Y] = meshgrid(0:5:400);

    %R = sqrt((c1*X.^2 + c2.*X + c3 + c4*Y.^2 + c5.*Y + c6).^2 + (c7*X.^2 + c8.*X + c9 + c10*Y.^2 + c11.*Y + c12).^2);
    %icke Arvids viktning
    R = sqrt((XX_coeffs(1)*X.^2 + XX_coeffs(2).*X + XX_coeffs(3) + XY_coeffs(1)*Y.^2 + XY_coeffs(2).*Y + XY_coeffs(3)).^2 + (YX_coeffs(1)*X.^2 + YX_coeffs(2).*X + YX_coeffs(3) + YY_coeffs(1)*Y.^2 + YY_coeffs(2).*Y + YY_coeffs(3)).^2);
    %Arvids viktning
    A = ((XX_coeffs(1)*X.^2 + XX_coeffs(2).*X + XX_coeffs(3) + XY_coeffs(1)*Y.^2 + XY_coeffs(2).*Y + XY_coeffs(3)).*X + (YX_coeffs(1)*X.^2 + YX_coeffs(2).*X + YX_coeffs(3) + YY_coeffs(1)*Y.^2 + YY_coeffs(2).*Y + YY_coeffs(3)).*Y)./(X + Y);
    %Z = R;
    Z = A;
    surf(X,Y,Z)
    rotate3d on;
end