# Low Cost TTS

    Module for computational low cost custom TTS.
    Working as alternative to ML cloning voice. 
    And avoid the problem of a computer without
    many RAM or CPU or GPU. It is useful for
    Cloning a basic human voice. 

## Warranty

    None

## Documentation

    $ ./install_complements.sh
    $ pip install -r requirements.txt 
    $ python main.py

    You need a vocabulary file in the main folder with the 1000 to 3000 most frequent words in the
    language target. The example in the folder is just for orientation.

## Folder structure

    ├── install_complements.sh\
    ├── main.py\
    ├── pronunciation_{lang}\
    ├── README.MD\
    ├── requirements.txt\
    └── vocabulary.txt\



## Testing
    
    OS:       Ubuntu Mate LTS 22.04 64 bits
    HW:       HP Laptop
    RAM:      15 GiB
    CPU:      AMD Ryzen 7 4700U with Radeon Graphics × 8 
    GRAPHICS: RENOIR (renoir, LLVM 15.0.6, DRM 3.47, 5.19.0-45-generic)
    VERSION:  Python 3.10.6