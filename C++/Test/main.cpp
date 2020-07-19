#include <iostream>
using namespace std;

class Array{
public:
    int Length;
private:
    int *values;    
    
public:
    explicit Array(int size){
        Length = size;
        values = new int[size]{};
    }
    
    ~Array(){
        delete [] values;
    }
    
    int & operator [](int index){
        if (index < 0)
            index += Length;
        if (index < 0 || index >= Length)
            return *values;
        return values[index];
    }
    
    bool Contains(int value){
        for (int i = 0; i < Length; ++i)
            if (values[i] == value)
                return true;
        return false;
    }
};

class List{
    const int InitialSize = 4;
    Array values = Array(InitialSize);
public:
    int Count = 0;
    int Capacity = InitialSize;
    
    void Add(int value){
        if (Count < Capacity){
            values[Count++] = value;
            return;
        }
        
    }
};

int main() {
    return 0;
}
