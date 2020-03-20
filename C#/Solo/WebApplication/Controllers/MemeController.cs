using Microsoft.AspNetCore.Mvc;
using WebApplication.Models;

namespace WebApplication.Controllers
{
	[Route("[controller]")]
	public class MemeController : Controller
	{
		[HttpGet]
		public IActionResult Get()
		{
			return Ok(new User());
		}
	}
}