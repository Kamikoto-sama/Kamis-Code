using System;
using VirtualMachine.Core;

namespace VirtualMachine.CPU.InstructionSet.Instructions
{
    public class If : InstructionBase
    {
        public If(OperandType second, OperandType third) : base(2, OperandType.Constant, second, third)
        { }

        protected override void ExecuteInternal(ICpu cpu, IMemory _, Operand op0, Operand op1, Operand op2)
        {
            var condition = (Condition) op0.Value.ToUInt();

            if (IsConditionTrue(condition, op1.Value, Word.Zero))
            {
                cpu.InstructionPointer = op2.Value;
            }
        }

        private static bool IsConditionTrue(Condition condition, Word a, Word b)
        {
            var cmp = a.CompareTo(b);

            if (condition.HasFlag(Condition.Less) && cmp < 0)
                return true;

            if (condition.HasFlag(Condition.Equals) && cmp == 0)
                return true;

            if (condition.HasFlag(Condition.Greater) && cmp > 0)
                return true;

            return false;
        }

        [Flags]
        public enum Condition : uint
        {
            Less = (1 << 2) | (0 << 1) | 0,
            Greater = (0 << 2) | (1 << 1) | 0,
            Equals = (0 << 2) | (0 << 1) | 1
        }
    }
}