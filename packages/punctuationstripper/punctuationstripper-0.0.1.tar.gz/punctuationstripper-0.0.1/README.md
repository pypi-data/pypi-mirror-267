# PunctuationStripper

PunctuationStripper is a Python package that can be used to strip punctuation from a file. It is easy to use and can be installed via pip: 

pip install punctuationstripper

Once installed, you can use the `punctuationstripper` command to strip punctuation from a file. The basic syntax is:

punctuationstripper -f [-n ] [-p ]

where:

* `<filename>` is the name of the file that you want to strip of punctuation.
* `<newfilename>` is the name of the new file that you want to save the stripped text to. If you do not specify a new filename, the program will save the stripped text to a new file named `<filename>_new.txt`.
* `<punct>` is a string of characters that you do not want to strip from the text. For example, if you want to keep all periods and commas in the text, you would specify `punct=".,"`.

For example, to strip all punctuation from the file `my_file.txt` and save the stripped text to a new file named `my_file_new.txt`, you would use the following command:

punctuationstripper -f my_file.txt -n my_file_new.txt


You can also use the `-p` option to specify a string of characters that you do not want to strip from the text. For example, to strip all punctuation from the file `my_file.txt` (and save it as `my_file_new.txt) except for periods and commas, you would use the following command:

punctuationstripper -f my_file.txt -p ".,"

PunctuationStripper is a powerful tool that can be used to clean up text data. It is easy to use and can be customized to meet your specific needs.
