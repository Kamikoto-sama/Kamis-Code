using System;
using System.Linq;
using System.Net.Http;
using Newtonsoft.Json.Linq;
using VirtualMachine.Core.Debugger.Model;
using VirtualMachine.Core.Debugger.Server.BreakPoints;

namespace VirtualMachine.Core.Debugger.Server
{
	public class RemoteDebuggerBase : Debugger
	{
		public RemoteDebuggerBase(IHttpServer server, DebugMode mode)
		{
			DebugMode = mode;

			server.AddHandler("GetDebugMode", HttpMethod.Get, (Func<JToken>) GetDebugMode);
			server.AddHandler("SetDebugMode", HttpMethod.Post, (Action<JToken>) SetDebugMode);

			server.AddHandler("AddBreakPoint", HttpMethod.Post, (Action<JToken>) AddBreakPoint);
			server.AddHandler("RemoveBreakPoint", HttpMethod.Post, (Action<JToken>) RemoveBreakPoint);
			server.AddHandler("GetBreakPoints", HttpMethod.Get, (Func<JToken>) GetBreakPoints);

			server.AddHandler("IsPaused", HttpMethod.Get, (Func<JToken>) IsPaused);
			server.AddHandler("Continue", HttpMethod.Post, (Action<JToken>) Continue);

			server.AddHandler("ReadIp", HttpMethod.Get, (Func<JToken>) ReadIp);
			server.AddHandler("WriteIp", HttpMethod.Post, (Action<JToken>) WriteIp);

			server.AddHandler("ReadWord", HttpMethod.Post, (Func<JToken, JToken>) ReadWord);
			server.AddHandler("WriteWord", HttpMethod.Post, (Action<JToken>) WriteWord);

			server.Start();
		}

		private void Continue(JToken obj) => GetPausedDebugger().Continue();

		private JToken GetDebugMode() => DebugMode.ToString();
		private void SetDebugMode(JToken mode) => DebugMode = mode.ToObject<DebugMode>();

		private void AddBreakPoint(JToken bp) => BreakPoints.Add(BreakPointsConverter.FromDto(bp.ToObject<BreakPointDto>()));

		private void RemoveBreakPoint(JToken bp) => BreakPoints.Remove(BreakPoints.Find(bp.ToObject<string>()));
		private JToken GetBreakPoints()
		{
			// ReSharper disable once CoVariantArrayConversion
			return new JArray(BreakPoints.BreakPoints.Select(BreakPointsConverter.ToDto).Select(JObject.FromObject).ToArray());
		}

		private JToken IsPaused() => TryGetPausedDebugger() != null;

		private JToken ReadIp() => new JValue(GetPausedDebugger().Context.Cpu.InstructionPointer.ToUInt());
		private void WriteIp(JToken ip) => GetPausedDebugger().Context.Cpu.InstructionPointer = new Word(ip.ToObject<uint>());

		private JToken ReadWord(JToken address) => GetPausedDebugger().Context.Memory.ReadWord(new Word(address.ToObject<uint>())).ToUInt();
		private void WriteWord(JToken pair)
		{
			var (address, value) = pair.ToObject<ValueTuple<uint, uint>>();
			GetPausedDebugger().Context.Memory.WriteWord(new Word(address), new Word(value));
		}

		private static readonly BreakPointsConverter BreakPointsConverter = new BreakPointsConverter();
	}
}