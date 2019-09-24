using System;

namespace VirtualMachine.Core
{
    public class Ram : IMemory
    {
        private readonly Word baseAddress;
        private readonly Word size;

        public Ram(uint baseAddress, uint size)
        {
            this.baseAddress = new Word(baseAddress);
            this.size = new Word(size);
            memory = new byte[size];
        }

        public Word ReadWord(Word address)
        {
	        lock (memory)
	        {
		        return new Word(Read(0), Read(1), Read(2), Read(3));
	        }

            byte Read(int byteNumber)
            {
                var index = GetOffset(address + new Word(byteNumber));
                if (index > int.MaxValue)
                    return (byte) memory.GetValue(index);
                return memory[(int) index];
            }
        }

        public void WriteWord(Word address, Word value)
        {
	        lock (memory)
	        {
		        Write(0, value.First);
		        Write(1, value.Second);
		        Write(2, value.Third);
		        Write(3, value.Fourth);
	        }

            void Write(int byteNumber, byte v)
            {
                var index = GetOffset(address + new Word(byteNumber));
                if (index > int.MaxValue)
                    memory.SetValue(v, index);
                else
                    memory[(int)index] = v;
            }
        }

        public bool CompareExchange(Word address, Word expectedValue, Word value, out Word oldValue)
        {
	        lock (memory)
	        {
		        oldValue = ReadWord(address);

		        if (oldValue != expectedValue)
			        return false;

				WriteWord(address, value);
				return true;
	        }
        }

        private long GetOffset(Word address)
        {
            var offset = address - baseAddress;
            if (offset.CompareTo(size) < 0)
                return offset.ToUInt();

            throw new IndexOutOfRangeException("Too high memory address");
        }

        private readonly byte[] memory;
    }
}