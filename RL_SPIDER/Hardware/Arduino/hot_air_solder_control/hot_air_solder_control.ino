
class Seg
{ public:
    Seg(int ia, int ib, int ic, int id, int ie, int iff, int ig, int idp, int ien);

    int pins[9];
    byte inp = 0, nums[10] = {0b11000000, 0b11111001, 0b10100100, 0b10110000, 0b10011001, 0b10010010, 0b10000010, 0b11111000, 0b10000000, 0b10011000};
    void display(int n);
    void enable();
    void disable();
    void decimalpoint(boolean state);
    void custom(byte inp);
    void render();
};
Seg::Seg(int ia, int ib, int ic, int id, int ie, int iff, int ig, int idp, int ien)
{
  pins[0] = ia;
  pins[1] = ib;
  pins[2] = ic;
  pins[3] = id;
  pins[4] = ie;
  pins[5] = iff;
  pins[6] = ig;
  pins[7] = idp;
  pins[8] = ien;

  for (int i = 0; i < 9; i++)
  {
    pinMode(pins[i], OUTPUT);
  }
};
void Seg::enable()
{ digitalWrite(pins[8], 1);
};
void Seg::disable()
{
  digitalWrite(pins[8], 0);
};
void Seg::decimalpoint(boolean state)
{ bitWrite(inp, 7, state);
};
void Seg::render()
{
  enable();
  for (int i = 0; i < 8; i++)
  {
    digitalWrite(pins[i], bitRead(inp, i));
  }
  disable();
};
void Seg::custom(byte inp)
{
  inp = inp;
};
void Seg::display(int n)
{
  inp = nums[n];
};

int a = 1, b = 3, c = 4, d = 5, e = 6, f = 7, g = 8, dp = 9;
/*
  Seg seg1(a, b, c, d, e, f, g, dp, 4);
  Seg seg2(a, b, c, d, e, f, g, dp, 5);
  Seg seg3(a, b, c, d, e, f, g, dp, 6);
  Seg seg4(a, b, c, d, e, f, g, dp, 7);*/

Seg segs[4] = {
  Seg(a, b, c, d, e, f, g, dp, 10),
  Seg(a, b, c, d, e, f, g, dp, 11),
  Seg(a, b, c, d, e, f, g, dp, 12),
  Seg(a, b, c, d, e, f, g, dp, 13)
};

volatile static boolean value = false;
volatile static long count = 0, pc = 0;
volatile static int seg_num = 0;
void disp(int val)
{
  for (int i = 0; i < 4; i++)
  {
    segs[i].display((val % (10 ^ i)));
  }
}
void counter()
{
  count++; l;
  seg_num++;
  seg_num = seg_num % 4;
  segs[seg_num].render();

}

void setup() {
  // put your setup code here, to run once:
  //Serial.begin(115200);
  pinMode(2, INPUT_PULLUP); 
  attachInterrupt(0, counter, RISING);
}
int v = 0;

void loop() {
  // put your main code here, to run repeatedly:
  disp(v);
  delay(100);
}
