# NFT_Image_Synthesis

This repo aims to generate synthetic images from folders of assets. The assets need to be in the same width and height and will need to follow a specific order of overlaying.

For using the code, please do the following:

1) Clone this repository \
   ` git clone https://github.com/henrywfyeung/NFT_Image_Synthesis.git`
2) Create your assets, i.e. background, body, face, etc
3) Put them in the corresponding folders inside **Image_Source**
4) Change the parameters inside generate_NFT.py. Parameters include:
    ```
    width:              the width of the generated images
    height:             the height of the generated images
    variation_target:   the expected number of unique images that your assets can generate
    items:              the number of generated images
    order:              the list of folder in order of left to right (background to foreground) in terms of overlaying
    ```
5) Install **opencv-python** and **numpy**
    
    ` pip install opencv-python ` \
    ` pip install numpy `
   
6) Goes to the directory that contains this repo \
   ` cd {path-to-repo}/NFT_Image_Synthesis `
7) run 
   
    `python genreate_NFT.py`

8) Check the folder **Image_Output** for generated images, and check the file **attributes.csv** for the corresponding attributes
