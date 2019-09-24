using System;

namespace VirtualMachine.Core.Debugger
{
	public class Result<T> : Result
	{
		public readonly T Value;

		public static Result<T> Success(T value) => new Result<T>(value, null);
		public new static Result<T> Fail(string error) => new Result<T>(default(T), error ?? throw new ArgumentNullException(nameof(error)));

		public Result(T value, string error) : base(error) => Value = value;
	}

	public class Result
	{
		public readonly string Error;

		public static Result Success() => new Result(null);
		public static Result Fail(string error) => new Result(error ?? throw new ArgumentNullException());

		public static Result<T> Success<T>(T value) => Result<T>.Success(value);
		public static Result<T> Fail<T>(string error) => Result<T>.Fail(error);

		protected Result(string error)
		{
			Error = error;
		}
	}
}