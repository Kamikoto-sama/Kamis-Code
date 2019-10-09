using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization.Json;
using System.Threading;
using System.Threading.Tasks;
using Useful;

namespace Test
{
    class Program
    {
        public const BindingFlags Flags = BindingFlags.Instance 
                                          | BindingFlags.Static 
                                          | BindingFlags.NonPublic
                                          | BindingFlags.Public;

        enum E
        {
	        A, B, C
        }
        
        public static void Main(string[] args)
        {
	        var d = new Dictionary<A, int>();
	        d.Re
        }

        private static async void M()
        {
	        var worker = new BackgroundWorker();
	        worker.DoWork += (sender, args) =>
	        {
		        for (var i = 0; i < 3; i++)
		        {
			        Thread.Sleep(300);
			        worker.ReportProgress(i);
		        }
	        };
	        worker.WorkerReportsProgress = true;
	        worker.ProgressChanged += (sender, args) => Console.WriteLine(args.ProgressPercentage);
	        worker.RunWorkerAsync();
        }
    }

    public class A
    {
	    public override int GetHashCode()
	    {
		    return 1;
	    }

	    public override bool Equals(object obj)
	    {
		    return ReferenceEquals(obj, this);
	    }
    }
}