function fitter(X,Y)
    linear = fit(X(:),Y(:),'poly1');
    squared = fit(X(:),Y(:), 'poly2');
    summa = 0;
    for k=1:size(X, 2)
       summa = summa + abs(Y(k) - linear(X(k)));
    end
    disp('linjärt fel: ');
    disp(summa);
    summa = 0;
    for k=1:size(X, 2)
       summa = summa + abs(Y(k) - squared(X(k)));
    end
    disp('kvadratiskt fel: ');
    disp(summa);
    
    plot(linear, X, Y);
    hold on
    plot(squared, X, Y);
    linear
    squared
end