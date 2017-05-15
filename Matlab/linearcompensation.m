function [C] = linearcompensation(X, Y)
    A = [1 1 1 1 1 1 1 1 1; X(1) X(2) X(3) X(4) X(5) X(6) X(7) X(8) X(9)];
    A = A';
    AT = A';
    
    Y = Y';
    C = (AT * Y) \ (AT*A);
    C = C / 10;
end