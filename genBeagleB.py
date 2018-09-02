# -*- coding: utf-8 -*-
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import time
import random

#constantes dos GPIO's
b0 = "P8_7"
b1 = "P8_8"
b2 = "P8_9"
b3 = "P8_10"
l0 = "P8_13"
l1 = "P8_14"
l2 = "P8_15"
l3 = "P8_16"

#Vetor com os leds
LEDS = [l0,l1,l2,l3]

game_sequence = []
player_sequence = []

GPIO.setup(b0, GPIO.IN)
GPIO.setup(b1, GPIO.IN)
GPIO.setup(b2, GPIO.IN)
GPIO.setup(b3, GPIO.IN)
GPIO.setup(l0, GPIO.OUT)
GPIO.setup(l1, GPIO.OUT)
GPIO.setup(l2, GPIO.OUT)
GPIO.setup(l3, GPIO.OUT)

GPIO.add_event_detect(b0, GPIO.FALLING)
GPIO.add_event_detect(b1, GPIO.FALLING)
GPIO.add_event_detect(b2, GPIO.FALLING)
GPIO.add_event_detect(b3, GPIO.FALLING)

current_round = 1
game_started = False

def pisca(led,tempo):
    GPIO.output(led, GPIO.HIGH)
    time.sleep(tempo)
    GPIO.output(led, GPIO.LOW)
    time.sleep(tempo)

def flag():
    pisca(l0,0.5)
    pisca(l1,0.5)
    pisca(l2,0.5)
    pisca(l3,0.5)

def generate_current_round():
    #Comecando com um led, a cada rodada aumenta um led no jogo gerado
    #for cont in range(0,current_round):
    current_led = random.randint(0,3)
    game_sequence.append(current_led)
    for count in range(0,current_round):
        pisca(LEDS[game_sequence[count]],0.5)
        #vai adicionando a sequencia dos leds na ordem     

def get_play():
    #numero de jogadas
    if(current_round > 1):
        del player_sequence[:]
    
    number_of_plays = 0
    play_time_begin = time.time() #Pega o numero de segundos desde epoch
    play_time_end = time.time()
    #Enquanto o tempo de resposta for menor que 3 segundos e numero de jogadas nao ultrapassar o limite da roda$
    while((play_time_end - play_time_begin) < current_round + 3): # cada jogada deve durar a

        if(GPIO.input(b0)):
            player_sequence.append(0)
            number_of_plays += 1
            print("B0")
            time.sleep(0.25)

        if(GPIO.input(b1)):
            player_sequence.append(1)
            number_of_plays += 1
            print("B1")
            time.sleep(0.25)

        if(GPIO.input(b2)):
            player_sequence.append(2)
            number_of_plays += 1
            print("B2")
            time.sleep(0.25)

        if(GPIO.input(b3)):
            player_sequence.append(3)
            number_of_plays += 1
            print("B3")
            time.sleep(0.25)

        play_time_end = time.time()
        if(number_of_plays == current_round):
            break
    if(number_of_plays < current_round): #encerra o jogo caso o jogador n aperte o num certo de botões
        while True:
            pisca(l0,0.1)
        
def validate_current_round():
    for i in range(0,current_round):
        if(player_sequence[i] != game_sequence[i]):
            return(False)
    return(True)

#Loop do jogo
while True:
    #Pressione qualquer botao para iniciar o jogo
    while(GPIO.input(b0) or GPIO.input(b1) or GPIO.input(b2) or GPIO.input(b3)):
        #Inicia o jogo
        flag()
        #flag game_started
        game_started = True
        #Loop do jogo
        while game_started:
            #O Computador gera uma rodada
            generate_current_round()    
            
            #Detecta a jogada do jogador
            get_play()

            #Pra debugar se tá tudo ok quando acertar e errar a sequencia gerada
            print(game_sequence)
            print(player_sequence)

            if(not(validate_current_round())):
                while True:
                    pisca(l0,0.1)

            flag()
            current_round += 1
