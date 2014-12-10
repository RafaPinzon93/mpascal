fun main()
    x: int;
    y: int;
    g: int;
begin
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