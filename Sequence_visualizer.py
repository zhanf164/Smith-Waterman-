# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 20:21:18 2019

@author: zach
"""
import pygame
import numpy as np 

pygame.init() # initialize an instance of pygame
screen = pygame.display.set_mode((1000, 900)) # set the display size of the screen
done = False # set a variable in order to know when to break out of the event loop.
topfont = pygame.font.SysFont('Courier New', 20) # initialize the font to use for the rest of the time
boxfont = pygame.font.SysFont('Courier New', 83)
insidefont = pygame.font.SysFont('Courier New', 40)
clock = pygame.time.Clock()



a = 'AGCTAGCGATCGACTAGCGCTAGCATATATATATCGCGCGCGACTCTAGCGATCGACTAGCTGACTGATGCGAC'
b = 'TAGCGCTAGCATA'
c= ' '
initial_length = len(b) # Going to end up needing this later. 

#Initialize the screen in order to hold the two sequences at the top of the screen
screen.fill((255, 255, 255))
pygame.display.update()
seqa = topfont.render(a, False, (0,0,0))
seqb = topfont.render(b, False, (0,0,0))
screen.blit(seqa, (50,0))
screen.blit(seqb, (50,13))
pygame.display.update()
pygame.display.flip()
   

def Smith_Waterman(seqA, seqB):
    gap_pen =  -4
    if len(seqA) > len(seqB):
         score_mat = np.zeros((int(len(seqB)+1), int(len(seqA)+1)), dtype=int)
         call_back = np.zeros((int(len(seqB)+1), int(len(seqA)+1)), dtype=str)
    else:
         score_mat = np.zeros((int(len(seqA)+1), int(len(seqB)+1)), dtype=int)
         call_back = np.zeros((int(len(seqA)+1), int(len(seqB)+1)), dtype=str)
    rows = score_mat.shape[0]
    cols = score_mat.shape[1]
    max_value = 0
    max_indexes = []
    for i in range(1, rows):
       for j in range(1, cols):
            mat_or_not = 0
            if seqA[i-1] == seqB[j-1]:
                mat_or_not = 5
                poss = ((score_mat[i-1,j-1]+mat_or_not),(score_mat[i-1,j]+gap_pen),(score_mat[i, j-1]+gap_pen), 0)
                score = max(poss)
                idx = poss.index(max(poss))
                score_mat[i,j] = score
                if score > max_value:
                    max_indexes = []
                    max_value = score
                    max_indexes.append((i,j))
                elif score == max_value:
                    max_indexes.append((i,j))
                if idx == 0:
                    call_back[i,j] = 'diag'
                elif idx == 1:
                    call_back[i,j] = 'up'
                else:
                    call_back[i, j] = 'left'
               
            else:
                mat_or_not = -3
                poss = ((score_mat[i-1,j-1]+mat_or_not),(score_mat[i-1,j]+gap_pen),(score_mat[i, j-1]+gap_pen), 0)
                score = max(poss)
                idx = poss.index(max(poss))
                score_mat[i,j] = score
                if score > max_value:
                    max_value = score
                    max_indexes = []
                    max_indexes.append((i,j))
                elif score == max_value:
                    max_indexes.append((i,j))
                if idx == 0:
                    call_back[i,j] = 'diag'
                elif idx == 1:
                    call_back[i,j] = 'up'
                else:
                    call_back[i, j] = 'left'
           
       
    return score_mat, call_back, max_indexes




def Create_boxes(initial_length):
    ''' Create the starting positions for the boxes to display on the screen'''
    box_list = []
    for i in range(initial_length+1):
        for j in range(initial_length+1):
           start_x = 100 + (50 * j)
           start_y = 120 + (50 * i)
           box_list.append((start_x, start_y))
    return box_list
       
box_list = Create_boxes(initial_length)
    
for i in range(len(box_list)):
    x = box_list[i][0]
    y = box_list[i][1]
    pygame.draw.rect(screen, (0, 0, 0), [x, y, 50,50],1)    

pygame.display.update()
pygame.display.flip()

 
def add_spaces(seqa, seqb):
    '''A quick funtion that will pad sequence b with a space in the front. This
    is so that when I end up displaying the sequences, when the user 
    pushes on the right arrow key, it will sequentially shift seqb one 
    nucleotide on seqa.'''
    
    pad = ' '
    if len(seqa) == len(seqb):
        pass
    else:
        return pad + seqb


current_spot_in_a = 0

    
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True 
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_RIGHT]:
        screen.fill((255, 255, 255))
        b = add_spaces(a, b)
        b_stripped = b.strip()
        current_spot_in_a += 1
        slice_a = a[current_spot_in_a:current_spot_in_a+initial_length]
        
        score_mat, call_back, max_indexes = Smith_Waterman(slice_a, b_stripped)
        score_mat_length = len(score_mat)
        for i in range(len(score_mat)):
            for j in range(len(score_mat)):
                start_x = 100 + (50 * j)
                start_y = 120 + (50 * i)
                value = score_mat[i][j]
                var = insidefont.render(str(value), False, (0,0,0))
                screen.blit(var, (start_x, start_y))

        seqa = topfont.render(a, False, (0,0,0))
        seqb = topfont.render(b, False, (0,0,0))
        b_stripped = boxfont.render(b_stripped, False, (0,0,0))
        b_stripped = pygame.transform.rotate(b_stripped, 270)
        box_a = boxfont.render(slice_a, False, (0, 0, 0))
        #
        
        for i in range(len(box_list)):
            x = box_list[i][0]
            y = box_list[i][1]
            pygame.draw.rect(screen, (0, 0, 0), [x, y, 50,50],1)
        screen.blit(b_stripped, (25, 170))
        screen.blit(box_a, (150, 50))
        screen.blit(seqa, (50,0))
        screen.blit(seqb, (50,13))
        pygame.display.update()
        pygame.display.flip()
        
    elif pressed[pygame.K_ESCAPE]:
        done = True
    clock.tick(18)
    
    