using System;
using VirtualMachine.Core;

namespace VirtualMachine.CPU.InstructionSet
{
    public abstract class InstructionBase : IInstruction
    {
        private const byte OpCodePrefix = 0xDE;
        private const byte OpCodeSuffix = 0xAD;

        public InstructionBase(byte opCode, OperandType first, OperandType second, OperandType third)
        {
            this.first = first;
            this.second = second;
            this.third = third;

            var operandType = (byte) (((ushort) first << 5) | ((ushort) second << 3) | (ushort) third);
            OpCode = new Word(OpCodePrefix, opCode, operandType, OpCodeSuffix);
            OperandsCount = 3;
        }

        public virtual string Name => $"{this.GetType().Name.ToLower()}-{ToChar(first)}{ToChar(second)}{ToChar(third)}";

        public Word OpCode { get; }
        public int OperandsCount { get; }
        public void Execute(ICpu cpu, IMemory memory, Word[] operands)
        {
            var op0 = new Operand(first, operands[0], memory);
            var op1 = new Operand(second, operands[1], memory);
            var op2 = new Operand(third, operands[2], memory);
            ExecuteInternal(cpu, memory, op0, op1, op2);
        }

        public override string ToString() => Name;

        protected abstract void ExecuteInternal(ICpu cpu, IMemory memory, Operand op0, Operand op1, Operand op2);

        private readonly OperandType first;
        private readonly OperandType second;
        private readonly OperandType third;

        private static char ToChar(OperandType t) => t == OperandType.AddressOfAddress ? 'p' : t.ToString().ToLower()[0];

        protected class Operand
        {
            public Operand(OperandType type, Word value, IMemory memory)
            {
                this.type = type;
                this.value = value;
                this.memory = memory;
            }

            public Word Value
            {
                get
                {
                    if (type == OperandType.Constant)
                        return value;
                    else if (type == OperandType.Address)
                        return memory.ReadWord(value);
                    else if (type == OperandType.AddressOfAddress)
                        return memory.ReadWord(memory.ReadWord(value));
                    else
                        throw new InvalidOperationException($"Access to ignored operand I={this.GetType().Name}");
                }
                set
                {
                    if (type == OperandType.Constant)
                        throw new InvalidOperationException($"Write access to const operand I={this.GetType().Namespace}");
                    else if (type == OperandType.Address)
                        memory.WriteWord(this.value, value);
                    else if (type == OperandType.AddressOfAddress)
                        memory.WriteWord(memory.ReadWord(this.value), value);
                    else
                        throw new InvalidOperationException($"Access to ignored operand I={this.GetType().Name}");
                }
            }

            private readonly OperandType type;
            private readonly Word value;
            private readonly IMemory memory;
        }
    }
}
