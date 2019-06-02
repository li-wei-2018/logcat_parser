# LogCat parsing tool

Returns log lines which match or does not match particular words. It also
can display test duration time between 'TEST STARTED' and 'TEST FINISHED'
phrases found in log file.

## Usage
### Word matcher

To use this tool as a word matcher there are two options:  
(1) to return lines that include desired words: `-i / --include`  
(2) to return lines that does not include any of desired words: `-e / --exclude`

It is possible to have it separately or combined:

    python logcat_parser.py <path_to_logcat_file> -i word1,word2,word3
    python logcat_parser.py <path_to_logcat_file> -i word1 -e word2,word3

**NOTE:** Keep in mind, words are separated with commas, without blank chars.

### Test duration

To display the test time duration between 'TEST STARTED' and 'TEST FINISHED'
phrases found in log file, use `-s` parameter:

    python logcat_parser.py <path_to_logcat_file> -s