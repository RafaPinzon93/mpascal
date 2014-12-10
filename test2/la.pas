fun main()
     x: int;
     y: int;
     g: int;
     a: int;
    begin
        if x < 2 then
            begin
                a := 2;
                b := 3
            end;
        read(x);
        read(y);
        g := y;
    while x > 0 do
        begin
            g := x;
            x := y - (y/x)*x;
            y := g
        end;
    write(g)
end