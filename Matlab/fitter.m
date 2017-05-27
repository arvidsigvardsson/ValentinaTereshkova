%given a discrete set of points calculates a curve that represents the
%points using the least square method.
%param: X, Y
%X: a vector containing the x values
%Y: a vector containing the y values
%return: linearCoeffs, squaredCoeffs
%linearCoeffs: a fitter object containing the coefficients for the curve
%squaredCoeffs: a fitter object containing the coefficients for the curve
function [linearCoeffs, squaredCoeffs] = fitter(X,Y)
    linear = fit(X(:),Y(:),'poly1');
    squared = fit(X(:),Y(:), 'poly2');
    linearSum = 0;
    squaredSum = 0;
    for k=1:size(X, 2)
       linearSum = linearSum + abs(Y(k) - linear(X(k))); %calculate how much error the curve has
    end
    disp('linjärt fel: ');
    disp(linearSum);
    for k=1:size(X, 2)
       squaredSum = squaredSum + abs(Y(k) - squared(X(k))); %calculate how much error the curve has
    end
    disp('kvadratiskt fel: ');
    disp(squaredSum);
    
    plot(linear, X, Y);
    hold on
    plot(squared, X, Y);
    linear
    linearCoeffs = coeffvalues(linear);
    squared
    squaredCoeffs = coeffvalues(squared);
    legend('data', 'Linjär','data', 'Kvadratisk')
end