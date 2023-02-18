from manim import *
from math import sin, cos, sqrt

from manim.utils.rate_functions import ease_out_sine
from numpy import square

class S1(Scene):
    def construct(self):
        text1 = Text("Everyone, it's a new year!").set_color_by_gradient(RED_B, YELLOW_B)
        self.play(Write(text1))
        self.play(text1.animate.shift(UP*3))
        
        time = ValueTracker(0)
        initTheta = PI/4
        l = 2
        g = 9.8
        w = np.sqrt(g/l)
        p = 2*PI/w

        originX = 0
        originY = 1
        startPoint = Dot([originX, originY, 0], radius=0.05, color=RED_B)
        originShft = originX * RIGHT + originY * UP

        theta = DecimalNumber().shift(10*UP)
        theta.add_updater(lambda m: m.set_value(initTheta*np.sin(w*time.get_value())))
        self.add(theta)

        def getLine(x, y):
            line = Line(start=ORIGIN + originShft, end=x*RIGHT+y*UP+originShft, color=RED_B)
            global verticalLine
            verticalLine = DashedLine(start=line.get_start(), end=line.get_start() + l*DOWN, color=YELLOW_B)

            return line

        def getAngle(theta):
            global angle
            global thetaLabel
            if theta == 0:
                angle = VectorizedPoint().move_to(10 * UP)
                thetaLabel = VectorizedPoint().move_to(10 * UP)
            else:
                if theta > 0:
                    angle = Angle(line, verticalLine, quadrant=(1, 1), other_angle=True, color=YELLOW_B, fill_opacity=0.5)
                else:
                    angle = Angle(line, verticalLine, quadrant=(1, 1), other_angle=False, color=YELLOW_B, fill_opacity=0.5)

            return angle

        def getEndBall(x, y):
            endBall = Dot(fill_color=RED_B, fill_opacity=1).move_to(x*RIGHT+y*UP+originShft).scale(l)
            return endBall

        line = always_redraw(lambda: getLine(l * np.sin(theta.get_value()), -l * np.cos(theta.get_value())))
        angle = always_redraw(lambda: getAngle(theta.get_value()))
        angleText = MathTex(r'\theta').scale(0.5).add_updater(lambda m: m.next_to(angle, DOWN))
        ball = always_redraw(lambda: getEndBall(l * np.sin(theta.get_value()), -l * np.cos(theta.get_value())))

        self.play(Create(VGroup(startPoint, line, verticalLine)))
        self.play(Create(VGroup(angle, angleText)))
        self.play(Create(ball))

        textDesc = Text("I think we should have a look at pendulums...").scale(0.7).shift(DOWN*3).set_color_by_gradient(BLUE_B, LIGHT_BROWN)

        self.play(time.animate.set_value(2.5*p), Write(textDesc), rate_func=linear, run_time = 5) 
        self.wait()

class S2(Scene):
    def construct(self):
        time = ValueTracker(0)
        initThetaS = PI/4
        initTheta = Variable(initThetaS, r'\theta')
        l = 5
        g = 9.8
        w = np.sqrt(g/l)
        p = 2*PI/w

        originX = -2.25
        originY = 3
        startPoint = Dot([originX, originY, 0], radius=0.1, color=BLUE_B)
        originShft = originX* RIGHT + originY * UP

        theta = DecimalNumber().shift(10*UP)
        theta.add_updater(lambda m: m.set_value(initTheta.tracker.get_value()*np.sin(w*time.get_value())))
        self.add(theta)

        def getLine(x, y):
            line = Line(start=ORIGIN + originShft, end=x*RIGHT+y*UP+originShft, color=BLUE_B)
            global verticalLine
            verticalLine = DashedLine(start=line.get_start(), end=line.get_start() + l*DOWN, color=WHITE)

            return line

        def getEndBall(x, y):
            endBall = Dot(fill_color=BLUE_B, fill_opacity=1).move_to(x*RIGHT+y*UP+originShft).scale(l)
            return endBall

        line = always_redraw(lambda: getLine(l * np.sin(theta.get_value()), -l * np.cos(theta.get_value())))
        ball = always_redraw(lambda: getEndBall(l * np.sin(theta.get_value()), -l * np.cos(theta.get_value())))

        self.add(VGroup(startPoint, line, verticalLine, ball))

        self.play(time.animate.set_value(2*p), rate_func=ease_out_sine, run_time=5)

        wDef = MathTex(r'w = \sqrt{\frac{g}{l}}').shift(UP*1, RIGHT*3)
        naturalFreqLabel = Text('"Natural Frequency"').scale(0.7).set_color_by_gradient(RED_B, YELLOW_B).align_to(wDef, LEFT).next_to(wDef, UP, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER+0.1).shift(1*RIGHT)
        wDef1 = MathTex(r'w = \sqrt{\frac{g}{l}}').shift(UP*1, RIGHT*3)
        thetaEquationMotion = MathTex(r'{{\theta}}(t)={{\theta}} \cos(wt)').set_color_by_tex("heta", BLUE).next_to(wDef, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER+0.2).align_to(wDef, LEFT)
        thetaRange = MathTex(r'-3 < {{\theta}}< 3').set_color_by_tex("heta", BLUE).next_to(thetaEquationMotion, DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER+0.5).align_to(thetaEquationMotion, LEFT)

        self.play(Write(wDef))
        self.add(wDef1)
        self.play(Write(naturalFreqLabel))
        self.wait()
        self.play(Transform(wDef, thetaEquationMotion))
        self.play(Create(thetaRange))
        self.wait()

        self.play(time.animate.set_value(4*p), rate_func=ease_out_sine, run_time=5)

        self.play(FadeOut(VGroup(wDef1, naturalFreqLabel, thetaEquationMotion, thetaRange, wDef)))

        normal = always_redraw(lambda: Arrow(start=[l * np.sin(theta.get_value())+originX, -l * np.cos(theta.get_value())+originY, 0], end=[l* np.sin(theta.get_value())+2*np.cos(theta.get_value())+originX, -l * np.cos(theta.get_value())+2*np.sin(theta.get_value())+originY, 0]) )
        normalLabel = always_redraw(lambda: MathTex(r'\mid \vec{v} \mid = mg \sin(\theta)').next_to(normal, DOWN, buff=0.7).scale(0.7).align_to(normal, ORIGIN))
        self.play(Create(VGroup(normal, normalLabel)))
        initTheta.label.set_color(BLUE)
        initTheta.shift(3*RIGHT).scale(1.2)

        self.play(Create(initTheta))
        self.wait()
        self.play(initTheta.tracker.animate.set_value(1))

        self.wait()
        self.play(time.animate.set_value(6*p), rate_func=ease_out_sine, run_time=5)
        self.play(FadeOut(normalLabel))

class S3(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-10, 10, 1], y_range=[-10, 10, 1], axis_config={"include_numbers": True}).scale(1)
        xLabel = plane.get_x_axis_label(r"\theta", edge=RIGHT, direction=RIGHT).scale(0.7)
        yLabel = plane.get_y_axis_label(r"\dot{\theta}", edge=UP, direction=UP).scale(0.7)
        func = lambda pos: ((-0.01*pos[1]) - np.sin(pos[0]))*UP + pos[1]*RIGHT
        vectorField = ArrowVectorField(func, x_range=[-10, 10, 0.5]).scale(1)

        self.play(Create(VGroup(plane, xLabel, yLabel)))
        self.play(*[GrowArrow(vec) for vec in vectorField], run_time=3)

        self.wait()
        phaseSpaceText = Text('"Phase Space"').set_color_by_gradient(RED_B, YELLOW_B).shift(UP*3).add_background_rectangle(BLACK, 0.5)
        self.play(Create(phaseSpaceText))

        opacityStreams = ValueTracker(0)
        streams = always_redraw(lambda: StreamLines(func, color=WHITE, virtual_time=1).set_opacity(opacityStreams.get_value()) )
        self.add(streams)
        streams.start_animation()
        self.play(opacityStreams.animate.set_value(0.3))
        self.wait(5)
        self.play(FadeOut(streams), FadeOut(phaseSpaceText))
        self.wait()

class S4(Scene):
    def construct(self):
        text = Text("Pendulums are very difficult to make.").scale(0.7).shift(UP*3).set_color_by_gradient(RED_B, YELLOW_B)

        time = ValueTracker(0)
        initTheta = PI/4
        l = 2
        g = 9.8
        w = np.sqrt(g/l)
        p = 2*PI/w

        originX = 0
        originY = 1
        startPoint = Dot([originX, originY, 0], radius=0.05, color=RED_B)
        originShft = originX * RIGHT + originY * UP

        theta = DecimalNumber().shift(10*UP)
        theta.add_updater(lambda m: m.set_value(initTheta*np.sin(w*time.get_value())))
        self.add(theta)

        def getLine(x, y):
            line = Line(start=ORIGIN + originShft, end=x*RIGHT+y*UP+originShft, color=RED_B)
            global verticalLine
            verticalLine = DashedLine(start=line.get_start(), end=line.get_start() + l*DOWN, color=YELLOW_B)

            return line

        def getAngle(theta):
            global angle
            global thetaLabel
            if theta == 0:
                angle = VectorizedPoint().move_to(10 * UP)
                thetaLabel = VectorizedPoint().move_to(10 * UP)
            else:
                if theta > 0:
                    angle = Angle(line, verticalLine, quadrant=(1, 1), other_angle=True, color=YELLOW_B, fill_opacity=0.5)
                else:
                    angle = Angle(line, verticalLine, quadrant=(1, 1), other_angle=False, color=YELLOW_B, fill_opacity=0.5)

            return angle

        def getEndBall(x, y):
            endBall = Dot(fill_color=RED_B, fill_opacity=1).move_to(x*RIGHT+y*UP+originShft).scale(l)
            return endBall

        line = always_redraw(lambda: getLine(l * np.sin(theta.get_value()), -l * np.cos(theta.get_value())))
        angle = always_redraw(lambda: getAngle(theta.get_value()))
        angleText = MathTex(r'\theta').scale(0.5).add_updater(lambda m: m.next_to(angle, DOWN))
        ball = always_redraw(lambda: getEndBall(l * np.sin(theta.get_value()), -l * np.cos(theta.get_value())))

        self.play(Write(text))
        self.play(Create(VGroup(startPoint, line, verticalLine)))
        self.play(Create(VGroup(angle, angleText)))
        self.play(Create(ball))

        self.play(time.animate.set_value(2*p), run_time=5, rate_func=linear)
        
        text2 = Text("Also the phase space took a long time to render...").scale(0.7).set_color_by_gradient(BLUE_B, LIGHT_BROWN).shift(DOWN*3)

        self.play(Write(text2))
