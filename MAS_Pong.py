from mttkinter import mtTkinter as tk
import turtle
import random
import time
from spade.agent import Agent
from spade.behaviour import  CyclicBehaviour, PeriodicBehaviour

# region window setup
wn = turtle.Screen()
wn.title("MAS Pong by @mkrajcer")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(1)
# endregion

# region global vars
score_a = 0
score_b = 0
rn1 = 100
rn2 = 100
period = 5
goal = 1
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
ball.dx = 1
ball.dy = -1
# endregion

# region paddle a
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)
# endregion

# region paddle b
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)
# endregion

# region movement functions
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)


def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)
# endregion

# region check functions
def endGame():
    ball.setx(0)
    ball.sety(0)
    pen.clear()


def checkWinner():
    if score_a == goal:
        endGame()
        pen.write("Agent A: {}  Agent B: {}, WINNER: Agent A".format(score_a, score_b), align="center",
                  font=("Courier", 24, "normal"))

    elif score_b == goal:
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

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        writeResult()

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        writeResult()

def writeResult():
    if score_a != 10 and score_b != 10:
        pen.clear()
        pen.write("Agent A: {}  Agent B: {}".format(score_a, score_b), align="center",
                  font=("Courier", 24, "normal"))


def checkPaddleBallCollision():
    if (340 < ball.xcor() < 350) and (paddle_b.ycor() + 40 > ball.ycor() > paddle_b.ycor() - 40):
        ball.setx(340)
        ball.dx *= -1

    if (-340 > ball.xcor() > -350) and (paddle_a.ycor() + 40 > ball.ycor() > paddle_a.ycor() - 40):
        ball.setx(-340)
        ball.dx *= -1
# endregion

# # region AgentJoker
class AgentJoker(Agent):
    class PlayBehavior(PeriodicBehaviour):
        async def run(self):
            global rn1 
            global rn2
            rn1 = random.randint(20, 100)
            rn2 = random.randint(20, 100)
            print("AgentOne's aproximation is: ", rn1)
            print("AgentTwo's aproximation is: ", rn2)
            

    async def setup(self):
        b = self.PlayBehavior(period=period)
        self.add_behaviour(b)
# endregion

# # region AgentPlayerOne
class AgentPlayerOne(Agent):
    class PlayBehavior(CyclicBehaviour):
        async def run(self):
            global rn1
            if ball.xcor() < 0:
                if paddle_a.ycor() < ball.ycor() and abs(paddle_a.ycor() - ball.ycor()) > int(rn1):
                    paddle_a_up()

                elif paddle_a.ycor() > ball.ycor() and abs(paddle_a.ycor() - ball.ycor()) > int(rn1):
                    paddle_a_down()

    async def setup(self):
        b = self.PlayBehavior()
        self.add_behaviour(b)
# endregion

# # region AgentPlayerTwo
class AgentPlayerTwo(Agent):
    class PlayBehavior(CyclicBehaviour):
        async def run(self):
            global rn2
            if ball.xcor() > 0:
                if paddle_b.ycor() < ball.ycor() and abs(paddle_b.ycor() - ball.ycor()) > int(rn2):
                    paddle_b_up()

                elif paddle_b.ycor() > ball.ycor() and abs(paddle_b.ycor() - ball.ycor()) > int(rn2):
                    paddle_b_down()

    async def setup(self):
        b = self.PlayBehavior()
        self.add_behaviour(b)
# # endregion


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

    async def setup(self):
        b = self.EnvironmentBehavior()
        self.add_behaviour(b)
        print("Pokrenuto")
# endregion

if __name__ == "__main__":
    env = AgentEnvironment("mateo_krajcer@rec.foi.hr", "pw1234")
    env.start()
    joker = AgentJoker("posiljatelj@rec.foi.hr", "tajna")
    joker.start()
    agentOne = AgentPlayerOne("primatelj@rec.foi.hr", "tajna")
    agentOne.start()
    agentTwo = AgentPlayerTwo("agent@rec.foi.hr", "tajna")
    agentTwo.start()
    print("Wait until user interrupts with ctrl+C")
    try:
        while True:
            wn.update()
    except KeyboardInterrupt:
        print("Stopping...")
    joker.stop()
    agentOne.stop()
    agentTwo.stop()
    env.stop()

