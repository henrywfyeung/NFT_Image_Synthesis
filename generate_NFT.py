import cv2
import numpy as np
import glob

'''
@author Henry Wing Fung Yeung

@notice This file takes in images contained in a list of folder and return the generated NFTs
'''

### PARAMETERS ###

# the image width of the generated images
width = 1096
# the image height of the generated images
height = 1096

# the order that assets will overlay each other. From left to right => from background to foreground
order = ["BgColor", "Body", "Face"] 

# the folder of the input image assets (those given in the order list above)
input_folder = "Image_Source"
output_folder = "Image_Output"
output_csv_file = "attributes.csv"

# total variation aim, i.e. how much different combinations would you like to achieve?
# if there are 5 BgColor, 4 Bodies, 3 Clothes, then there are 60 combinations
variation_target = 20
# number of items to output. How many images to generate
items = 10
assert items <= variation_target, "There will be repeating images because the variation is too low."
##################

### GENERATION CODE ###
generation_list = []
for tl in range(len(order)):
  folder_name = order[tl]
  folders = glob.glob(input_folder + "/" + folder_name)
  for folder in folders:
    files = glob.glob(folder + "/*")
    assert len(files) > 0, "Empty folder detected. Please make sure all folders in the order list are populated with images"
    generation_list.append(files)

glist_len = len(generation_list)
glist_item_len = [ len(i) for i in generation_list]
print("Image generation by layer: ")
print(glist_item_len)
number_of_nfts = np.prod(glist_item_len)
assert variation_target < number_of_nfts, "The variation of images are lower than target. Please increase the variation by creating more assets"
print("Total Combinations: {}".format(number_of_nfts))

# assume equal prob, change the probability to a distribution if required
probabilities = []
for i in glist_item_len:
  probabilities.append([1/i] * i)

layers = len(order)
# generation_matrix is initialised to be twice the size of the required items to prevent duplication
generation_matrix = np.zeros((layers, items*2), dtype=np.uint8)
unique_generation_matrix = np.zeros((layers, items), dtype=np.uint8)

def column_from_prob(l):

  a = []
  for i in range(len(probabilities[l])):
    if i == len(probabilities[l]) - 1:
      a.extend([i] * (generation_matrix.shape[1] - len(a)))
    else:
      a.extend([i] * int(np.round(generation_matrix.shape[1] * probabilities[l][i])))
  return a

def init():
  for l in range(layers):
    generation_matrix[l,:] = column_from_prob(l)

def permute_column(m):
  for l in range(m.shape[0]):
    permutation = list(np.random.permutation(m.shape[1]))
    m[l,:] = m[l,permutation]
  return m

def permute_order(m):
    permutation = list(np.random.permutation(m.shape[1]))
    return m[:,permutation]

def check_duplication(m):
  unq, _ = np.unique(m, axis=1, return_counts=True)
  return unq

# Initalise and populate the matrix for generation
init()
# permutate the generation order of each layer
generation_matrix = permute_column(generation_matrix)
# ensure that the generation matrix is unique
unq = check_duplication(generation_matrix)
# select the unique images
unique_generation_matrix = unq[:,:items]
# pemute the order
unique_generation_matrix = permute_order(unique_generation_matrix)

# save to csv
np.savetxt(output_csv_file, unique_generation_matrix, delimiter=",")

count = 0
for i in range(unique_generation_matrix.shape[1]):
  img = np.zeros((height,width,4), dtype=np.uint8)
  
  item = [ generation_list[jid][j] for jid, j in enumerate(list(unique_generation_matrix[:,i])) ]
  
  for f in item:
    overlay = cv2.imread(f, cv2.IMREAD_UNCHANGED)
      
    # https://en.wikipedia.org/wiki/Alpha_compositing (alpha compositing)
    if overlay.shape[-1] > 3:
      alpha_foreground = overlay[:,:,3] / 255.0
      alpha_background = img[:,:,3] / 255.0

      for color in range(0, 3):
        img[:,:,color] = alpha_foreground * overlay[:,:,color] + \
          alpha_background * img[:,:,color] * (1 - alpha_foreground)
      
      # set adjusted alpha and denormalize back to 0-255
      img[:,:,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255
      
    else:
      img[:,:,0:3] += overlay
      img[:,:,3] = 255
  
  cv2.imwrite("./{}/image-{}.png".format(output_folder, count), img)
  print(count)
  count += 1
