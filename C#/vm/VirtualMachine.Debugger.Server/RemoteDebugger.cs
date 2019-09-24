using VirtualMachine.Core.Debugger.Model;
using VirtualMachine.Core.Debugger.Server;
using VirtualMachine.Debugger.Server.Http;

namespace VirtualMachine.Debugger.Server
{
    public class RemoteDebugger : RemoteDebuggerBase
    {
        public RemoteDebugger(string host, ushort port, DebugMode mode) : base(new HttpServer(host, port), mode)
        {
        }
    }
}