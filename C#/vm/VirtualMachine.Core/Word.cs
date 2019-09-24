using System;

namespace VirtualMachine.Core
{
    public struct Word : IEquatable<Word>, IComparable<Word>
    {
        public const int Size = 4;

        public static readonly Word Zero = new Word(0);

        public Word(byte ll, byte lh, byte hl, byte hh)
        {
            this.ll = ll;
            this.lh = lh;
            this.hl = hl;
            this.hh = hh;
        }

        public Word(int value) : this(BitConverter.GetBytes(value).ReverseIf(!BitConverter.IsLittleEndian))
        { }

        public Word(uint value) : this(BitConverter.GetBytes(value).ReverseIf(!BitConverter.IsLittleEndian))
        { }

        public Word(byte[] bytes)
        {
            if (bytes.Length != Size)
                throw new ArgumentException($"Word size should be {Size}", nameof(bytes));
            ll = bytes[0];
            lh = bytes[1];
            hl = bytes[2];
            hh = bytes[3];
        }

        public uint ToUInt()
        {
            unchecked
            {
                uint value = hh;
                value = (value << 8) + hl;
                value = (value << 8) + lh;
                return (value << 8) + ll;
            }
        }

        public int ToInt()
        {
            unchecked
            {
                return (int) ToUInt();
            }
        }

        public byte First => ll;
        public byte Second => lh;
        public byte Third => hl;
        public byte Fourth => hh;

        public byte LowLow => First;
        public byte LowHigh => Second;
        public byte HighLow => Third;
        public byte HighHigh => Fourth;

        public ushort Low => (ushort)((lh << 8) + ll);
        public ushort High => (ushort)((hh << 8) + hl);

        public static Word operator+(Word a, Word b)
        {
            unchecked
            {
                return new Word(a.ToUInt() + b.ToUInt());
            }
        }

        public static Word operator-(Word a, Word b)
        {
            unchecked
            {
                return new Word(a.ToUInt() - b.ToUInt());
            }
        }

        public static bool operator ==(Word a, Word b) => a.Equals(b);
        public static bool operator !=(Word a, Word b) => !(a == b);

        public int CompareTo(Word other) => ToInt().CompareTo(other.ToInt());

        public bool Equals(Word other) => other.ll == ll && other.lh == lh && other.hl == hl && other.hh == hh;
        public override bool Equals(object obj) => obj is Word w && Equals(w);
        public override int GetHashCode() => ToInt();

        public override string ToString() => $"{First:X2} {Second:X2} {Third:X2} {Fourth:X2}";

        private readonly byte ll;
        private readonly byte lh;
        private readonly byte hl;
        private readonly byte hh;
    }
}
