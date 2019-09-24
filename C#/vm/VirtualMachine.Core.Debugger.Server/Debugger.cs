using System;
using System.Linq;
using VirtualMachine.CPU;
using VirtualMachine.Core.Debugger.Model;
using VirtualMachine.Core.Debugger.Server.BreakPoints;

namespace VirtualMachine.Core.Debugger.Server
{
	public class Debugger : ISupervisor
	{
		private readonly object pauseLock = new object();
		private volatile PausedDebugger pausedDebugger;

		public DebugMode DebugMode { get; set; }

		public readonly BreakPointCollection BreakPoints = new BreakPointCollection();

		public PausedDebugger TryGetPausedDebugger() => pausedDebugger;
		public PausedDebugger GetPausedDebugger() => TryGetPausedDebugger() ?? throw new InvalidOperationException("Not paused");

		Decision ISupervisor.OnStep(ICpu cpu, IMemory memory)
		{
			if (DebugMode == DebugMode.Stepping)
			{
				return OnPause(new PauseContext(memory, cpu, StopReason.Step, null, null));
			}
			else
			{
				var stopReason = BreakPoints.Find(cpu.InstructionPointer).FirstOrDefault(b => b.ShouldStop(memory));
				if (stopReason != default(IBreakPoint))
				{
					return OnPause(new PauseContext(memory, cpu, StopReason.Breakpoint, stopReason, null));
				}
			}

			return Decision.Continue;
		}

		Decision ISupervisor.OnInstructionDecodeError(ICpu cpu, IMemory memory, string message)
		{
			return OnPause(new PauseContext(memory, cpu, StopReason.InstructionDecodeError, null, message));
		}

		Decision ISupervisor.OnInstructionExecuteError(ICpu cpu, IMemory memory, string message)
		{
			return OnPause(new PauseContext(memory, cpu, StopReason.InstructionExecutionError, null, message));
		}

		private Decision OnPause(PauseContext context)
		{
			pausedDebugger = new PausedDebugger(context);

			pausedDebugger.Continued.GetAwaiter().GetResult();

			pausedDebugger = null;

			return Decision.Continue;
		}

		private class PauseContext : IPauseContext
		{
			public PauseContext(IMemory memory, ICpu cpu, StopReason stopReason, IBreakPoint stopBreakPoint, string stopMessage)
			{
				Memory = memory;
				Cpu = cpu;
				StopReason = stopReason;
				StopMessage = stopMessage;
				StopBreakPoint = stopBreakPoint;
			}

			public IMemory Memory { get; }
			public ICpu Cpu { get; }
			public StopReason StopReason { get; }
			public IBreakPoint StopBreakPoint { get; }
			public string StopMessage { get; }
		}
	}
}
