using System;

namespace VirtualMachine.Core.Debugger.Client
{
    public class DebuggerModel
    {
        public DebuggerClient Client
        {
            get => client ?? throw new InvalidOperationException("Debugger not connected");
            set => client = value;
        }

        private DebuggerClient client;
    }
}