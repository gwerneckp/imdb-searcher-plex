# IMDb Movie Title Formatter
This Python script allows you to search for a movie by name on IMDb and format its title along with IMDb ID, or directly provide an IMDb URL to format the title.

## Usage
Download the binary (imdb) from the Releases section of your repository.
Open a terminal and navigate to the directory containing the binary.
Search for a movie by name:

```bash
./imdb blair witch
```

The script will display the formatted movie titles along with IMDb IDs. If using the search option, additional cast information will be displayed.


```
The Blair Witch Project (1999) {imdb-tt0185937}          || Heather Donahue, Michael C. Williams 
Blair Witch (2016) {imdb-tt1540011}                      || James Allen McCune, Callie Hernandez 
Book of Shadows: Blair Witch 2 (2000) {imdb-tt0229260}   || Jeffrey Donovan, Stephen Barker Turner 
Curse of the Blair Witch (1999) {imdb-tt0202493}         || Peg O'Keef, Heather Donahue 
Shadow of the Blair Witch (2000) {imdb-tt0265736}        || Tony Abatemarco, Andre Brooks 
The Blair Witch Legacy (2018) {imdb-tt7740342}           || Samantha Marie Cook, Cody Epling 
The Blair Witch Mountain Project (2002) {imdb-tt0381920} || Hope Levy, Ike Eisenmann 
The Real Blair Witch (2003) {imdb-tt0472599}             ||
```

Format the title using an IMDb URL:
```bash
./imdb --url https://www.imdb.com/title/tt15671028/
```

```
No Hard Feelings (2023) {imdb-tt15671028}
```


## License
This project is licensed under the MIT License.

