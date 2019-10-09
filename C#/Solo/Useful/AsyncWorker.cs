using System;
using System.Threading.Tasks;

namespace Useful
{
	public static class AsyncWorker
	{
		public static Task Do(Action action, bool start=true)
		{
			var task = new Task(action);
			if (start)
				task.Start();
			return task;
		}

		public static Task<T> Do<T>(Func<T> action, bool start=true)
		{
			var task = new Task<T>(action); 
			if (start)
				task.Start();
			return task;
		}
	}
}