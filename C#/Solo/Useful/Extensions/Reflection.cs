namespace Useful.Extensions.Reflection
{
	public static class Reflection
	{
		public static bool HasProperty<T>(this T obj, string propertyName) => 
			obj.GetType().GetProperty(propertyName) != null;
	}
}