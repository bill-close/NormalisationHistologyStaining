# NormalisationHistologyStaining
The Hematoxylin and Eosin (H&amp;E) stain is essential in histology, highlighting nuclei in blue for clear tissue evaluation. For automated analysis, it's vital to normalize these images due to color variations from sample preparation and imaging.


![computer_character_microscope](https://github.com/bill-close/NormalisationHistologyStaining/assets/90579801/e43f2876-0f78-4b72-9880-b9a5d2e9178a)

Publication reference:

[1] A method for normalizing histology slides for quantitative analysis, M Macenko, M Niethammer, JS Marron, D Borland, JT Woosley, G Xiaojun, C Schmitt, NE Thomas, IEEE ISBI, 2009. dx.doi.org/10.1109/ISBI.2009.5193250

Original references:
http://http//amida13.isi.uu.nl
Adoped from:
https://github.com/mitkovetta/staining-normalization
https://www.youtube.com/@DigitalSreeni


To execute:
python normalisestaining.py --imageFile imgs/example1.png --saveFile imgs/norm1
python normalisestaining.py --imageFile imgs/example2.png --saveFile imgs/norm2
