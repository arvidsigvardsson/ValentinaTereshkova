function [linearCoeffs, squaredCoeffs] = fitter(X,Y)
    linear = fit(X(:),Y(:),'poly1');
    squared = fit(X(:),Y(:), 'poly2');
    l_summa = 0;
    s_summa = 0;
    for k=1:size(X, 2)
       l_summa = l_summa + abs(Y(k) - linear(X(k)));
    end
    disp('linjärt fel: ');
    disp(l_summa);
    for k=1:size(X, 2)
       s_summa = s_summa + abs(Y(k) - squared(X(k)));
    end
    disp('kvadratiskt fel: ');
    disp(s_summa);
    
    plot(linear, X, Y);
    hold on
    plot(squared, X, Y);
    linear
    linearCoeffs = coeffvalues(linear);
    squared
    squaredCoeffs = coeffvalues(squared);
    legend('data', 'Linjär','data', 'Kvadratisk')
end