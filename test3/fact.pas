
fun fact(n:int):
  a : int;
  b : int
  begin
    a := 1;
   if n == 1
    then
    a := 1
  end

fun main():
   x:int;
   r:int
   begin
      print("Entre un numero\n");
      read(x);
      r := fact(x);
      write(r)
   end

