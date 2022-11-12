import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

# Tamanho da janela do jogo
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

# Definir variaveis do jogo
current_fighter = 1  # O lutador vai ser o primeiro a atacar
total_fighters = 3  # Total de lutadores
action_cooldown = 0  # Cooldown 
action_wait_time = 90 # Tempo de espera entre os turnos
attack = False
potion = False
potion_effect = 15 
clicked = False
game_over = 0

# Carregar as imagens do jogo
background_img = pygame.image.load("RPG/imagens/background/background.png").convert_alpha()

# Carregar as imagens do painel
panel_img = pygame.image.load('RPG/imagens/icons/panel.png').convert_alpha()

# Carregar as imagens dos butões
potion_img = pygame.image.load('RPG/imagens/icons/potion.png').convert_alpha()
restart_img = pygame.image.load('RPG/imagens/icons/restart.png').convert_alpha()

#Carregar as imagens de derrota e vitoria
victory_img = pygame.image.load('RPG/imagens/icons/victory.png')
defeat_img = pygame.image.load('RPG/imagens/icons/defeat.png')

# Carregar as imagens do painel
sword_img = pygame.image.load('RPG/imagens/icons/sword.png').convert_alpha()

# Definir as fontes
font = pygame.font.SysFont('Times New Roman', 26)

# Definir cores
red = (255, 0, 0)
green = (0, 255, 0)

# Carregar imagem de fundo
def draw_bg():
    screen.blit(background_img, (0, 0))


# Função para desenhar texto
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color) # criar a imagem pq em python tem q ser texto convertido em img
    screen.blit(img, (x, y)) # exibit na tela com as coords x y

# Carregar imagem do painel
def draw_panel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))

    # Mostrar as stats do 
    draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
    for count, i in enumerate(bandit_list):
        # Mostrar nome e vida
        draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 60)

# Classe dos lutadores
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potion):  # construtor
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potion = potion
        self.potion = potion
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: idle, 1: ataque, 2: machucar, 3:morto
        self.update_time = pygame.time.get_ticks()
        # carregar imagens de idle
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'RPG/img_beta/{self.name}/idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list) # uma lista de listas
        # carregar imagens de ataque
        temp_list = []
        for i in range(8):
                img = pygame.image.load(f'RPG/img_beta/{self.name}/attack/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                temp_list.append(img)
        self.animation_list.append(temp_list)
        # carregar imagens qnd o player leva dano
        temp_list = []
        for i in range(3):
                img = pygame.image.load(f'RPG/img_beta/{self.name}/hurt/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                temp_list.append(img)
        self.animation_list.append(temp_list)
        # carregar imagens de morte
        temp_list = []
        for i in range(10):
                img = pygame.image.load(f'RPG/img_beta/{self.name}/death/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                temp_list.append(img)
        self.animation_list.append(temp_list) 
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        # animação
        # atualizar as imagens
        self.image = self.animation_list[self.action][self.frame_index]
        # pegue o tempo atual, tire o tempo que foi atualizado recentemente e se a diferença entre os dois for maior que 100, entao atualize a imagem
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Se a animação acabar, resetar desde o zero (idle)
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1 # ultimo frame da animação
            else:
                self.idle()
    
    def idle(self):
         # Resetar animação para idle
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # Atribui dano no inimigo
        rand = random.randint(-5, 5) # entre -5 e 5 numero aleatorio o dano do jogador
        damage = self.strength + rand # dano do jogador 
        target.hp -= damage  # Dano final causado nos inimigos
        # Animação de levar dano
        target.hurt()
        # Checar se o target morreu
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        # Animação de ataque
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def hurt(self):
        # Animação para qnd levar o dano
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def death(self):
        # Animação da morte
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def reset(self):
        self.alive = True
        self.potion = self.start_potion
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
    

    def draw(self):
        screen.blit(self.image, self.rect)


# Classe do HP
class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self. hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        # Atualize a barra de hp
        self.hp = hp
        # Calcular o ratio do hp
        ratio = self.hp/self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


# Classe de Texto de Dano
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        # Mover o texto pra cima
        self.rect.y -= 1   # Positivo = vai pra baixo / Negativo = vai pra cima
        # Deletar o texto depois de alguns segundos
        self.counter += 1
        if self.counter > 30:
            self.kill()       


damage_text_group = pygame.sprite.Group()


knight = Fighter(200, 260, 'Knight', 30, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

# Criar butões
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

# Função pra sair do jogo
run = True
while run:

    clock.tick(fps)

    # desenhe a imagem de fundo
    draw_bg()

    # desenhe a imagem do painel
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    # desenhe o 
    knight.update()
    knight.draw()

    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    # desenhe o texto do dano
    damage_text_group.update()
    damage_text_group.draw(screen)

    # Controlar ações do jogador
    #Resetar as variaveis de ação
    attack = False
    potion = False
    target = None
    # Deixar o cursor do mouse visivel 
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos() # passar o mouse em cima do inimigo mostra o icone de espada 
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            # esconder o mouse
            pygame.mouse.set_visible(False)
            # mostrar o icone da espada no lugar do cursor
            screen.blit(sword_img, pos)
            if clicked == True and bandit.alive == True:
                attack = True
                target = bandit_list[count]
    if potion_button.draw():
        potion = True
    # Mostrar quantas poções restam
    draw_text(str(knight.potion), font, red, 150, screen_height - bottom_panel + 70)

    if game_over == 0:
        # Ação do jogador
        if knight.alive == True: # Se estiver vivo
            if current_fighter == 1: # Começa a atacar
                action_cooldown +=1 # Incrementa o tempo de ação até 90 do action_wait_time
                if action_cooldown >= action_wait_time: # Esta pronto para atacar
                    # Procurar a ação do jogador
                    # Ataque
                    if attack == True and target != None:
                        knight.attack(target) # ataca o bandido 1 
                        current_fighter += 1  # avança para o proximo lutador
                        action_cooldown = 0 # reseta o cooldown de espera
                    # Poção
                    if potion == True:
                        if knight.potion > 0:
                            # Checar se a poção vai curar mais do q a vida maxima
                            # Exemplo: se o jogador tem 30 hp, levar 5 de dano, ele vai ter 25 de hp
                            #  30  - 25 = 5 (nao eh maior que 15, entao skipa e vai pro else)
                            if knight.max_hp - knight.hp > potion_effect:
                                heal_amount = potion_effect 
                            # So curar o restante dos 5, sem ultrapassar o HP max dele. 
                            else: 
                                heal_amount = knight.max_hp - knight.hp
                            knight.hp += heal_amount
                            knight.potion -= 1
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over = -1

        # Ação do inimigo
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive == True:
                    action_cooldown += 1 
                    if action_cooldown >= action_wait_time:
                        # Checar se o bandido precisa curar antes de atacar
                        if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potion > 0:
                            # Checar se a poção vai curar mais do q a vida maxima
                            if bandit.max_hp - bandit.hp > potion_effect:
                                heal_amount = potion_effect 
                            else: 
                                heal_amount = bandit.max_hp - bandit.hp
                            bandit.hp += heal_amount
                            bandit.potion -= 1
                            damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
                        # Ataque
                        else:
                            bandit.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                else: # Se estiver morto
                    current_fighter += 1 # passa pro proximo lutador

        if current_fighter > total_fighters:
            current_fighter = 1

    #checar se os inimigos estao mortos
    alive_bandits = 0
    for bandit in bandit_list:
        if bandit.alive == True:
            alive_bandits += 1
    if alive_bandits == 0:
        game_over = 1 # todos mortos = vitoria

    # Checar se o jogo acabou
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()