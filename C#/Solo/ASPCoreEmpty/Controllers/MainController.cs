using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.Net.Http.Headers;

namespace ASPCoreEmpty.Controllers
{
	[Route("")]
	public class MainController : Controller
	{
		[HttpGet]
		public IActionResult RegisterForm()
		{
			return View();
		}

		[HttpPost("register/{login}&{password}")]
		public IActionResult Register(string login, string password)
		{
			return Ok($"{login};{password}");
		}
	}
}