import random
import sys
import time
import pygame

FT = 1000  # 刷新间隔（毫秒）
PopL = 500  # number of the peoples (init)


def preload():
    global s, i, r, bkg
    s = pygame.image.load("resource/S.png")
    i = pygame.image.load("resource/I.png")
    r = pygame.image.load("resource/R.png")
    bkg = pygame.image.load("resource/bkg.png")


class Person(object):
    # Fixed args
    IA = 20  # px;infect area
    IP = 1  # infect possibility
    ItRT = 10  # s;infect-to-recovered-time
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
            if COUNT - self.infected_time > self.ItRT and random.randint(0, 10000) in range(int(self.DR * 10000)):
                self.state = "R"
                self.icon = self.r
                bkg.blit(self.icon, self.pos)
            else:
                if COUNT - self.infected_time > self.ItRT:
                    self.die()

    def by_infect(self):
        self.state = "I"
        self.infected_time = COUNT
        self.icon = i

    def die(self):
        pos_new = list(self.pos)
        pos_new.append(self.pos[0] + 10)
        pos_new.append(self.pos[1] + 10)
        self.icon.fill((0, 0, 0))
        pygame.display.flip()
        print("{} is died".format(self))
        del self
        pygame.display.flip()

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


class main():
    def __init__(self):
        preload()  # preload resources

        global COUNT
        self.COUNT = 0
        # pygame
        pygame.init()
        size = (640, 640)
        global screen, bk
        screen = pygame.display.set_mode(size)

        # record prog-data
        self.start_time = int(round(time.time() * 1000))  # 毫秒数时间戳 round-四舍五入

        # make people
        self.city_list = []
        self.person_list = []
        init_infect_rt_by_per = 100
        sys.stderr.write("START:CONSTRUCTING\n")
        for ci in range(City.max_city):
            self.city_list.append(City(PopL, 0.05))
            for per in range(self.city_list[ci].max_pr):
                self.person_list.append(Person("I" if per % init_infect_rt_by_per == 0 else "S"))
                print("here is {}".format(self.person_list[per]))

        # Running
        sys.stderr.write("START:ITER\n")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.per_i = 0
            self.per_s = 0
            self.per_r = 0
            if (int(round(time.time() * 1000)) - self.start_time) >= FT:
                self.start_time += FT
                for per in self.person_list:
                    per.recovered()
                    if time.time() - per.birth_time > per.LT:
                        self.person_list.remove(per)
                    print(per)
                    if per.state == "I":
                        self.per_i += 1
                    elif per.state == "S":
                        self.per_s += 1
                    elif per.state == "R":
                        self.per_r += 1
                    # screen.fill((0, 0, 0))
                    pygame.display.flip()
                    per.move_randomly()

                sys.stderr.write(
                    "START:ITER {} ,{} INFECTED ,{} INFECTABLE ,{} RECOVERED\n".format(COUNT, self.per_i, self.per_s,
                                                                                       self.per_r))
                sys.stderr.flush()
                COUNT += 1

            for per in self.person_list:
                if per.state == "I":
                    for per_2 in self.person_list:
                        if (per.pos[0] - per.IA < per_2.pos[0] < per.pos[0] + per.IA) and (
                                per.pos[1] - per.IA < per_2.pos[1] < per.pos[1] + per.IA) and (
                                per.state == "I" and per_2.state == "S"):
                            if per.state == "I" and random.randint(0, 100) in range(per_2.IP):
                                per_2.by_infect()

            pygame.display.update()


