using System;

namespace GravityBalls
{
	public class WorldModel
	{
		public double BallX;
		public double BallY;
		public double BallRadius;
		public double WorldWidth;
		public double WorldHeight;
		public int Vector = 1;
		public int Speed = 200;
		public int SVector = 1;

		public void SimulateTimeframe(double dt)
		{
			BallY += Speed * dt * Vector;
			if (BallY >= WorldHeight - BallRadius)
				Vector = -1;
			if (BallY <= 0)
				Vector = 1;
			if (Speed >= 5000)
				SVector = -1;
			if (Speed <= 150) SVector = 1;
			Speed += 10 * SVector;

		}
	}
}