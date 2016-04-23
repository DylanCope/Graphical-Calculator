import string
import math
from InteractiveTextBox import InteractiveTextBox

def programatize(eqn):
    eqn = eqn.replace("^", "**")
    eqn = eqn.replace("abs", "math.fabs")
    eqn = eqn.replace("factorial", "math.factorial")
    eqn = eqn.replace("log", "math.log")
    eqn = eqn.replace("ln", "math.log")
    eqn = eqn.replace("pow", "math.pow")
    eqn = eqn.replace("sqrt", "math.sqrt")

    eqn = eqn.replace("e", "math.e")
    eqn = eqn.replace("pi", "math.pi")

    eqn = eqn.replace("sin", "math.sin")
    eqn = eqn.replace("cos", "math.cos")
    eqn = eqn.replace("tan", "math.tan")
    eqn = eqn.replace("arc", "math.a")
    eqn = eqn.replace("ar", "math.a")

    return eqn

class Locus:

    def __init__(self, form, eqn, colour):
        ## Form can be parametric or cartesian.
        self.form = form
        self.characters = []
        self.eqn = eqn
        self.colour = colour
        self.update(eqn)

    def update(self, eqn):

        if self.form == "cartesian":
            # Converting the equation to python:
            self.eqn = programatize(eqn)
            self.display = InteractiveTextBox("y = ", eqn, self.colour)

        elif self.form == "parametric":

            (e1, e2) = eqn

            self.display = (InteractiveTextBox("x = ", e1, self.colour),
                            InteractiveTextBox("y = ", e2, self.colour))

            e1 = programatize(e1)
            e2 = programatize(e2)

            self.eqn = (e1, e2)


    def getForm(self):
        return self.form

    def getEqnString(self):
        return self.eqn

    def getDisplay(self):
        return self.display

    def setColour(self, colour):
        self.colour = colour

    def getColour(self):
        return self.colour

    def calculate(self, start, stop, step):
        self.points = []
        self.start = start
        self.stop = stop
        self.step = step
        errors = []
        variable = start
        while variable < stop:
            coord = ()
            if self.form == "parametric":
                t = variable
                x = 0
                y = 0
                try:
                    x = eval(self.eqn[0])
                except ValueError:
                    errors.append("ValueError in x = "+self.eqn[0])
                except:
                    errors.append("Unknown error in x = "+self.eqn[0])

                try:
                    y = eval(self.eqn[1])
                except ValueError:
                    errors.append("ValueError in y = "+self.eqn[0])
                except:
                    errors.append("Unknown error in y = "+self.eqn[0])

                coord = (x, y)

            elif self.form == "cartesian":
                x = variable
                y = 0
                try:
                    y = eval(self.eqn)
                except ValueError:
                    errors.append("ValueError in y = "+self.eqn)
                except:
                    errors.append("Unknown error in y = "+self.eqn)

                coord = (x, y)


            self.points.append(coord)

            variable += step


    def pixelize(self, scale, gridOrigin):

        ## Transforming the locus to the grid it's within.
        self.adjustedPoints = []
        for p in self.points:
            x = p[0]
            y = p[1]

            ## Scale represents how many pixels represent a unit.
            x *= scale
            y *= -scale

            x += gridOrigin[0]
            y += gridOrigin[1]

            self.adjustedPoints.append((x, y))

    def updateDisplay(self, screen, events):

        if self.form == "parametric":
            for d in self.display:
                d.update(events)
                d.render(screen)
        elif self.form == "cartesian":
            self.display.update(events)
            self.display.render(screen)
            if self.display.computeLocus():
                self.update(self.display.characters)
                self.calculate(self.start, self.stop, self.step)
                self.display.compute = False

    def getPointsOnScreen(self):
        return self.adjustedPoints
