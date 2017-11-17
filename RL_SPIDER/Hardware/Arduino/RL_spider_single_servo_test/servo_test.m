
arr=zeros(1,100);
Q := adt::Queue();

s = serial('COM1','BaudRate',115200);
fopen(s)

for i=0:100
    fprintf(s,'*IDN?')

    for j=0:10000
        idn = fscanf(s);
    end
    
    
end

fclose(s)