# NormalisationHistologyStaining
The Hematoxylin and Eosin (H&amp;E) stain is essential in histology, highlighting nuclei in blue for clear tissue evaluation. For automated analysis, it's vital to normalize these images due to color variations from sample preparation and imaging.



Publication reference:

[1] A method for normalizing histology slides for quantitative analysis, M Macenko, M Niethammer, JS Marron, D Borland, JT Woosley, G Xiaojun, C Schmitt, NE Thomas, IEEE ISBI, 2009. dx.doi.org/10.1109/ISBI.2009.5193250

Original references:
http://http//amida13.isi.uu.nl
Adoped from:
https://github.com/mitkovetta/staining-normalization
https://www.youtube.com/@DigitalSreeni


To execute:
python normalizeStaining.py --imageFile imgs/example1.png --saveFile imgs/norm1
python normalizeStaining.py --imageFile imgs/example2.png --saveFile imgs/norm2