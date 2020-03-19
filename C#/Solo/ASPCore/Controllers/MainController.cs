using Microsoft.AspNetCore.Mvc;

namespace ASPCore.Controllers
{
	[ApiController]
	[Route("api/main")]
	public class MainController : Controller
	{
		[HttpGet]
		public IActionResult Get()
		{
			return Ok("HEllo :D");
		}
	}
}