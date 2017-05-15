function [C] = squaredcompensation(X, Y)
    A = [1 1 1 1 1 1 1 1 1; X(1) X(2) X(3) X(4) X(5) X(6) X(7) X(8) X(9); X(1)^2 X(2)^2 X(3)^2 X(4)^2 X(5)^2 X(6)^2 X(7)^2 X(8)^2 X(9)^2];
    A = A';
    AT = A';
    Y = Y';
    
    C = (AT * Y) \ (AT * A);
    C = C / 10^8;
end