using System;
using System.Linq;
using System.Threading;
using VirtualMachine.Core;

namespace VirtualMachine.CPU
{
    public class Cpu : ICpu
    {
        private static readonly Word InstructionPointerAddress = Word.Zero;

        public Cpu(IInstructionSet instructionSet, ISupervisor supervisor)
        {
            this.instructionSet = instructionSet;
            this.supervisor = supervisor;

            StepDelay = TimeSpan.FromMilliseconds(100);
        }

        public TimeSpan StepDelay { get; set; }

        public Word InstructionPointer
        {
            get => memory.ReadWord(InstructionPointerAddress);
            set => memory.WriteWord(InstructionPointerAddress, value);
        }

        public void Run(IMemory memory)
        {
            if (Interlocked.CompareExchange(ref this.memory, memory, null) != null)
                throw new CpuException("Cpu already run");

            while (true)
            {
                Step();
                Thread.Sleep(StepDelay);
            }
        }

        private void Step()
        {
            IInstruction instruction;
            Word[] operands;

            if (supervisor.OnStep(this, memory) == Decision.Terminate)
                throw new CpuException("Terminate by debugger");

            try
            {
                (instruction, operands) = DecodeInstruction();
            }
            catch (CpuException e) when (e.OpCode != null && e.Ip != null)
            {
                if (supervisor.OnInstructionDecodeError(this, memory, e.Message) == Decision.Terminate)
                    throw;
                return;
            }
            catch (Exception e)
            {
                if (supervisor.OnInstructionDecodeError(this, memory, e.Message) == Decision.Terminate)
                    throw new CpuException($"Instruction decode error: {e.Message}");
                return;
            }

            try
            {
                Execute(instruction, operands);
            }
            catch (Exception e)
            {
                if (supervisor.OnInstructionExecuteError(this, memory, e.Message) == Decision.Terminate)
                    throw new CpuException(InstructionPointer, instruction.OpCode, $"Instruction execution error: {e.Message}");
            }
        }

        private void Execute(IInstruction instruction, Word[] operands)
        {
            InstructionPointer = InstructionPointer + new Word((1 + operands.Length) * Word.Size);

            instruction.Execute(this, memory, operands);
        }

        private (IInstruction instruction, Word[] operands) DecodeInstruction()
        {
            var opCode = memory.ReadWord(InstructionPointer);
            var instruction = instructionSet.FindInstruction(opCode);
            if (instruction == null)
                throw new CpuException(InstructionPointer, opCode, $"Unknown instruction");

            var operands = Enumerable.Range(1, instruction.OperandsCount)
                .Select(i => i * Word.Size)
                .Select(offset => InstructionPointer + new Word(offset))
                .Select(memory.ReadWord)
                .ToArray();
            return (instruction, operands);
        }

        private readonly IInstructionSet instructionSet;
        private readonly ISupervisor supervisor;
        private IMemory memory;
    }
}
