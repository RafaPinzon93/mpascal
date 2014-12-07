fun fact(n:int):int
    p:int;
  begin
     if n == 1 then return 1
     else return n * fact(n-1)
  end

fun mai()
   x:int;
   r:int;
   begin
      print("Entre un numero\n");
      read(x);
      r := fact(x);
      write(r)
   end

