%Calculate the total error in the system and present it in the form of a 3D
%plot
%param: XX_coeffs, XY_coeffs, YY_coeffs, YX_coeffs
%XX_coeffs: the coefficients for the compensation curve
%XY_coeffs:-------------------||-----------------------
%YY_coeffs:-------------------||-----------------------
%YX_coeffs:-------------------||-----------------------
function totalError(XX_coeffs, XY_coeffs, YY_coeffs, YX_coeffs)

    [X, Y] = meshgrid(0:5:400);
    A = ((XX_coeffs(1)*X.^2 + XX_coeffs(2).*X + XX_coeffs(3) + XY_coeffs(1)*Y.^2 + XY_coeffs(2).*Y + XY_coeffs(3)).*X + (YX_coeffs(1)*X.^2 + YX_coeffs(2).*X + YX_coeffs(3) + YY_coeffs(1)*Y.^2 + YY_coeffs(2).*Y + YY_coeffs(3)).*Y)./(X + Y);
    Z = A;
    surf(X,Y,Z)
    rotate3d on;
end