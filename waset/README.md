# waset-scraper

Downloads papers published to the popular predatory publisher waset.org :)
If you do not care about the meteadata stored in the json file you can download the papers much quicker like so
```
seq 1 1 10010100 | parallel -j100 wget -c --content-disposition https://waset.org/publications/{}
```
## Prerequisites
* python3
* bs4

## Usage
```
python3 waset-scraper.py
```

Sample output
```
memes@pepe:~/git/scrapers/waset$ python3 waset-scraper.py 
-- Grabbing page  0 Papers grabbed  0 --
-- Grabbing page  1 Papers grabbed  0 --
0 The Number of Rational Points on Elliptic Curves y2 = x3 + a3 on Finite Fields
1 Some Algebraic Properties of Universal and Regular Covering Spaces
2 Classification of the Bachet Elliptic Curves y2 = x3 + a3 in Fp, where p ≡ 1 (mod 6) is Prime
3 Gene Network Analysis of PPAR-γ: A Bioinformatics Approach Using STRING
4 The Dividend Payments for General Claim Size Distributions under Interest Rate
5 Affine Projection Algorithm with Variable Data-Reuse Factor
```

