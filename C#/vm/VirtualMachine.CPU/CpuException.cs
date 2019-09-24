using System;
using VirtualMachine.Core;

namespace VirtualMachine.CPU
{
    public class CpuException : Exception
    {
        public readonly Word? Ip;
        public readonly Word? OpCode;

        internal CpuException(Word ip, Word opCode, string message) : base(message)
        {
            Ip = ip;
            OpCode = opCode;
        }

        public CpuException(string message) : base(message)
        {

        }
    }
}