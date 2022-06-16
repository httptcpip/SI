import random
import sys
import time
import pygame

COUNT = 0
FT = 1000  # 刷新间隔（毫秒）
PopL = 500  # number of the peoples (init)
screen: pygame.Surface
per_i = 0
per_s = 0
per_r = 0
person_list = []
city_list = []
s = pygame.image.load("resource/S.png")
i = pygame.image.load("resource/I.png")
r = pygame.image.load("resource/R.png")
bkg = pygame.image.load("resource/bkg.png")
bk = bkg
have_input_g = True


class Person(object):
    # Fixed args
    IA = 40  # px;infect area
    IP = 0.25  # infect possibility
    ItRT = 14  # s;infect-to-recovered-time
    LT = 100  # iter;live time
    DR = 0.0118  # death rate

    def __init__(self, state="S"):
        self.age = random.randint(1, 100)
        self.state = state
        self.s = s
        self.i = i
        self.r = r
        self.birth_time = time.time()
        self.infected_time = COUNT if self.state == "I" else None
        self.icon = s if state == "S" else i if state == "I" else "R"
        self.pos = [random.randint(0, 64) * 10, random.randint(0, 64) * 10]
        self.moveable_object = screen.blit(self.icon, self.pos)
        pygame.display.update()

    def move_randomly(self):
        pos_movement = random.sample(list(range(10, 21, 10)) + list(range(-20, -9, 10)), 2)
        screen.blit(bkg, self.pos)
        self.pos[0] += pos_movement[0]
        self.pos[1] += pos_movement[1]
        self.icon = s if self.state == "S" else self.i if self.state == "I" else self.r
        if 640 > self.pos[0] > 0 or 640 > self.pos[1] > 0:
            screen.blit(self.icon, self.pos)
        else:
            screen.blit(self.icon, (320, 320))
        pygame.display.update()

    def recovered(self):
        if self.infected_time is not None:
            if not (COUNT - self.infected_time > self.ItRT and random.randint(0, 10000) in range(int(self.DR * 10000))):
                self.state = "R"
                self.icon = self.r
                bkg.blit(self.icon, self.pos)

    def by_infect(self):
        self.state = "I"
        self.infected_time = COUNT
        self.icon = i

    def __str__(self):
        return "Person {} with state {} stand at {} brith in {}".format(id(self), self.state, self.pos, self.birth_time)


class Market:
    def __init__(self, city):
        self.city = city


class City:
    max_city = 1  # Max city number

    def __init__(self, max_per, tarvel_rt):
        self.max_pr = max_per
        self.tar_rt = tarvel_rt


def Main(have_input=True):
    # preload()  # preload resources

    global COUNT, screen, per_s, per_r, per_i, COUNT, FT, PopL, person_list, city_list, s, i, r, bk, have_input_g

    # pygame
    pygame.init()
    size = (640, 640)
    have_input_g = have_input

    screen = pygame.display.set_mode(size)

    # record prog-data
    start_time = int(round(time.time() * 1000))  # 毫秒数时间戳 round-四舍五入

    # make people
    city_list = []
    init_infect_rt_by_per = 100
    sys.stderr.write("START:CONSTRUCTING\n")
    for ci in range(City.max_city):
        city_list.append(City(PopL, 0.05))
        for per in range(city_list[ci].max_pr):
            person_list.append(Person("I" if per % init_infect_rt_by_per == 0 else "S"))
            print("here is {}".format(person_list[per]) if have_input else "", end="\n" if have_input else "")

    # Running
    sys.stderr.write("START:ITER\n")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        per_i = 0
        per_s = 0
        per_r = 0
        if (int(round(time.time() * 1000)) - start_time) >= FT:
            start_time += FT
            for per in person_list:
                per.recovered()
                if time.time() - per.birth_time > per.LT:
                    person_list.remove(per)
                print(per if have_input else "", end="\n" if have_input else "")
                if per.state == "I":
                    per_i += 1
                elif per.state == "S":
                    per_s += 1
                elif per.state == "R":
                    per_r += 1
                # screen.fill((0, 0, 0))
                pygame.display.flip()
                per.move_randomly()

            sys.stderr.write(
                "START:ITER {} ,{} INFECTED ,{} INFECTABLE ,{} RECOVERED\n".format(COUNT, per_i, per_s,
                                                                                   per_r))
            sys.stderr.flush()
            COUNT += 1

        for per in person_list:
            if per.state == "I":
                for per_2 in person_list:
                    if (per.pos[0] - per.IA < per_2.pos[0] < per.pos[0] + per.IA) and (
                            per.pos[1] - per.IA < per_2.pos[1] < per.pos[1] + per.IA) and (
                            per.state == "I" and per_2.state == "S"):
                        if per.state == "I" and random.randint(0, 100) in range(int(per_2.IP * 100)):
                            per_2.by_infect()

        pygame.display.update()
