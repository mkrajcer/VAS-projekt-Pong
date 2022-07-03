from mttkinter import mtTkinter as tk
import turtle
from spade.agent import Agent
from spade.behaviour import  CyclicBehaviour, PeriodicBehaviour

# region global
score_a = 0
score_b = 0
rally = 0
global ball_speed 
ball_speed = 0
x_direction = 1
y_direction = -1
end = False
bounce_x = 0
GOAL = 1
PERIOD_ONE = 0.1
PERIOD_TWO = 0.3
LIMIT_ONE = -150
LIMIT_TWO = 150
WIDTH = 800
HEIGHT = 600

# endregion

# region window setup
wn = turtle.Screen()
wn.title("MAS Pong by @mkrajcer")
wn.bgcolor("black")
wn.setup(width=WIDTH, height=HEIGHT)
wn.tracer(1)
# endregion

# region pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
# endregion

# region ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = x_direction
ball.dy = y_direction
# endregion

# region paddle a
paddle_a = turtle.Turtle()
paddle_a.speed(1)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)
# endregion

# region paddle b
paddle_b = turtle.Turtle()
paddle_b.speed(1)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)
# endregion

# region movement functions
def paddle_a_up():
    y = paddle_a.ycor()
    y += 10
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()
    y -= 10
    paddle_a.sety(y)


def paddle_b_up():
    y = paddle_b.ycor()
    y += 10
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()
    y -= 10
    paddle_b.sety(y)
# endregion

# region check functions
def endGame():
    ball.setx(0)
    ball.sety(0)
    pen.clear()


def checkWinner():
    global end
    if score_a == GOAL:
        if end == False:
            print("Ball speed: " + str(ball_speed) + ", Rally: " + str(rally))
            end = True
        endGame()
        pen.write("Agent A: {}  Agent B: {}, WINNER: Agent A".format(score_a, score_b), align="center",
                  font=("Courier", 24, "normal"))

    elif score_b == GOAL:
        if end == False:
            print("Ball speed: " + str(ball_speed) + ", Rally: " + str(rally))
            end = True
        endGame()
        pen.write("Agent A: {}  Agent B: {}, WINNER: Agent B".format(score_a, score_b), align="center",
                  font=("Courier", 24, "normal"))


def checkPaddleBorder():
    if paddle_a.ycor() > 250:
        paddle_a.sety(250)

    if paddle_a.ycor() < -250:
        paddle_a.sety(-250)

    if paddle_b.ycor() > 250:
        paddle_b.sety(250)

    if paddle_b.ycor() < -250:
        paddle_b.sety(-250)


def checkBallBorder():
    global score_a
    global score_b
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        bounce_x = ball.xcor()
        print("bounce at: " + str(bounce_x))

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        bounce_x = ball.xcor()
        print("bounce at: " + str(bounce_x))

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        ball.dy *= -1
        score_a += 1
        writeResult()
        ball.speed(1)

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        ball.dy *= -1
        score_b += 1
        writeResult()
        ball.speed(1)


def writeResult():
    if score_a != 10 and score_b != 10:
        pen.clear()
        pen.write("Agent A: {}  Agent B: {}".format(score_a, score_b), align="center",
                  font=("Courier", 24, "normal"))


def checkPaddleBallCollision():
    global rally
    if (340 < ball.xcor() < 350) and (paddle_b.ycor() + 40 > ball.ycor() > paddle_b.ycor() - 40):
        rally += 1
        ball.setx(340)
        ball.dx *= -1

    if (-340 > ball.xcor() > -350) and (paddle_a.ycor() + 40 > ball.ycor() > paddle_a.ycor() - 40):
        rally += 1
        ball.setx(-340)
        ball.dx *= -1

# endregion


# region AgentPlayerOne
class AgentPlayerOne(Agent):     
    
    # periodically checking balls coordinates
    class PlayBehavior1(PeriodicBehaviour):
        async def run(self):
            if ball.xcor() < 0 and ball.dx == -1:
                if paddle_a.ycor() < ball.ycor() and abs(paddle_a.ycor() - ball.ycor()) > 40:
                    paddle_a_up()

                elif paddle_a.ycor() > ball.ycor() and abs(paddle_a.ycor() - ball.ycor()) > 40:
                    paddle_a_down()
     
    class PlayBehavior2(CyclicBehaviour):
        
        async def run(self):
            global bounce_x
            self.ballx = ball.xcor()
            self.paddley = paddle_a.ycor()
            self.paddlex = paddle_a.xcor()

            if self.ballx == -50 and ball.dx == -1:
                self.ballx1 = ball.xcor()
                self.bally1 = ball.ycor()

            if self.ballx == LIMIT_ONE and ball.dx == -1:
                self.ballx2 = ball.xcor()
                self.bally2 = ball.ycor()

                if bounce_x > LIMIT_ONE and bounce_x < 0:
                    if ball.dy == 1:
                        self.a = (-290 - self.bally2) / (bounce_x - self.ballx2)
                        self.b = self.a * -self.ballx2 + self.bally2
                        self.final_y = self.paddlex * self.a + self.b

                    elif ball.dy == -1:
                        self.a = (290-self.bally2)/(bounce_x-self.ballx2)
                        self.b = self.a * -self.ballx2 + self.bally2
                        self.final_y = self.paddlex * self.a + self.b

                elif bounce_x < 0:
                    if ball.dy == 1:
                        self.a = (-290 - self.bally2) / (bounce_x - self.ballx2)
                        self.b = self.a * -self.ballx2 + self.bally2
                        self.final_y = self.paddlex * self.a + self.b

                    elif ball.dy == -1:
                        self.a = (290-self.bally2)/(bounce_x-self.ballx2)
                        self.b = self.a * -self.ballx2 + self.bally2
                        self.final_y = self.paddlex * self.a + self.b
                
                else:
                    self.a1 = (self.bally2 - self.bally1) / (self.ballx2 - self.ballx1)
                    self.b1 = self.a1 * -self.ballx1 + self.bally1

                    if ball.dy == 1:
                        self.bounce_x = (self.b1 - 290) / (-self.a1)
                        self.a2 = (290 - self.bally1) / (self.bounce_x - (self.bounce_x * 2))

                    elif ball.dy == -1:
                        self.bounce_x = (self.b1 + 290) / (-self.a1)
                        self.a2 = (-290 - self.bally1) / (self.bounce_x - (self.bounce_x * 2))

                    self.b2 = self.a2 * - (self.bounce_x * 2) + self.bally1
                    self.final_y = self.paddlex * self.a2 + self.b2 

            if self.ballx < LIMIT_ONE:

                if self.paddley > self.final_y:
                    paddle_a_down()

                elif self.paddley < self.final_y:
                    paddle_a_up()
     

    async def setup(self):
        b1 = self.PlayBehavior1(period=PERIOD_ONE)
        #self.add_behaviour(b1)
        b2 = self.PlayBehavior2()
        self.add_behaviour(b2)
# endregion

# region AgentPlayerTwo
class AgentPlayerTwo(Agent):
    
    # periodically checking balls coordinates
    class PlayBehavior1(PeriodicBehaviour):
        async def run(self):
            if ball.xcor() > 0 and ball.dx == 1:
                if paddle_b.ycor() < ball.ycor() and abs(paddle_b.ycor() - ball.ycor()) > 40:
                    paddle_b_up()

                elif paddle_b.ycor() > ball.ycor() and abs(paddle_b.ycor() - ball.ycor()) > 40:
                    paddle_b_down()
                    
    
    # position aproximation up until ball reaches x-coordinate limit            
    class PlayBehavior2(CyclicBehaviour):
        async def run(self):
            global bounce_x
            self.ballx = ball.xcor()
            self.paddley = paddle_b.ycor()
            self.paddlex = paddle_b.xcor()

            if self.ballx == 50 and ball.dx == 1:
                self.ballx1 = ball.xcor()
                self.bally1 = ball.ycor()

            if self.ballx == LIMIT_TWO and ball.dx == 1:
                self.ballx2 = ball.xcor()
                self.bally2 = ball.ycor()

                if bounce_x < LIMIT_TWO and bounce_x > 0:
                    if ball.dy == 1:
                        self.a = (-290 - self.bally2) / (bounce_x - self.ballx2)
                        self.b = self.a * -self.ballx2 + self.bally2
                        self.final_y = self.paddlex * self.a + self.b

                    elif ball.dy == -1:
                        self.a = (290-self.bally2)/(bounce_x-self.ballx2)
                        self.b = self.a * -self.ballx2 + self.bally2
                        self.final_y = self.paddlex * self.a + self.b

                elif bounce_x < 0:
                    if ball.dy == 1:
                        self.a = (-290 - self.bally2) / (bounce_x - self.ballx2)
                        self.b = self.a * -self.ballx2 + self.bally2
                        self.final_y = self.paddlex * self.a + self.b

                    elif ball.dy == -1:
                        self.a = (290-self.bally2)/(bounce_x-self.ballx2)
                        self.b = self.a * -self.ballx2 + self.bally2
                        self.final_y = self.paddlex * self.a + self.b
                
                else:
                    self.a1 = (self.bally2 - self.bally1) / (self.ballx2 - self.ballx1)
                    self.b1 = self.a1 * -self.ballx1 + self.bally1

                    if ball.dy == 1:
                        self.bounce_x = (self.b1 - 290) / (-self.a1)
                        self.a2 = (290 - self.bally1) / (self.bounce_x - (self.bounce_x * 2))

                    elif ball.dy == -1:
                        self.bounce_x = (self.b1 + 290) / (-self.a1)
                        self.a2 = (-290 - self.bally1) / (self.bounce_x - (self.bounce_x * 2))

                    self.b2 = self.a2 * - (self.bounce_x * 2) + self.bally1
                    self.final_y = self.paddlex * self.a2 + self.b2 


            if self.ballx > LIMIT_TWO:

                if self.paddley > self.final_y:
                    paddle_b_down()

                elif self.paddley < self.final_y:
                    paddle_b_up()

    async def setup(self):
        b1 = self.PlayBehavior1(period=PERIOD_TWO)
        #self.add_behaviour(b1)
        b2 = self.PlayBehavior2()
        self.add_behaviour(b2)
# endregion


# region AgentEnvironment
class AgentEnvironment(Agent):
    class EnvironmentBehavior(CyclicBehaviour):
        async def run(self):
            
            ball.setx(ball.xcor() + ball.dx)
            ball.sety(ball.ycor() + ball.dy)
            
            # region check winner
            checkWinner()
            # endregion

            # region paddle border checking
            checkPaddleBorder()
            # endregion

            # region border checking
            checkBallBorder()
            # endregion

            # region paddle-ball collisions
            checkPaddleBallCollision()
            # endregion

            if rally == 10:
                print("tie")
                endGame()


    class BallBehavior(PeriodicBehaviour):
            async def run(self):
                # increase ball speed
                global ball_speed
                ball_speed = ball.speed()
                if ball_speed < 10 and ball_speed != 0:
                    ball_speed += 1
                    ball.speed(ball_speed)
                if ball_speed == 10:
                    ball.speed(0)


    async def setup(self):
        b = self.EnvironmentBehavior()
        self.add_behaviour(b)
        b = self.BallBehavior(period=10)
        self.add_behaviour(b)
        print("Pokrenuto")
# endregion

if __name__ == "__main__":
    env = AgentEnvironment("mateo_krajcer@rec.foi.hr", "pw1234")
    env.start()
    agentOne = AgentPlayerOne("posiljatelj@rec.foi.hr", "tajna")
    agentOne.start()
    agentTwo = AgentPlayerTwo("primatelj@rec.foi.hr", "tajna")
    agentTwo.start()
    print("Wait until user interrupts with ctrl+C")
    try:
        while True:
            wn.update()
    except KeyboardInterrupt:
        print("Stopping...")
    agentOne.stop()
    agentTwo.stop()
    env.stop()
