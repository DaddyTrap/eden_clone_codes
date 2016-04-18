# eden_clone_codes
A python script to "clone" codes in eden (eden.sysu.edu.cn).

## 1.Why?
I use eden and I like this nice OJ website, though it has something annoying yet...So, that's why I write this script to help me clone the code files.
Our TAs usually tell us that we should compile and debug our code in local compiler and debugger, for which we have to copy the code to the local folder. But when we meet an assignment that has many files(maybe more than 10 files!), we have to copy them one by one.
Why not use ```clone``` like git's ```git clone```?

## 2.How to use it?
Just clone this repository, or only copy the .py file in it. Put the .py file to the folder you want to set your code.
Then run it!
In Windows, maybe you can double-click it and it runs itself.
In Linux, you may ```cd``` to your folder and ```python get_codes.py```.

Then, input your username, password and the assignment's id (please get it from the browser's url).

For example, if you want to clone **Digraph(DS)(15C++)**, whose url is **http://eden.sysu.edu.cn/m/ass/6183/**, then you should input "6183" (no quote).

Then you can input a folder name, and the program will clone the files there.

Now you can save your username and password in a file, so that you can skip the input next time.


## 3.TODO
It is very imperfect that maybe anyone can contribute to this lovely tool. So, feel **FREE** to make Pull Request. I will be very grateful and accept your hard work (if the code work well).

* Maybe we can implement the function "put the code in another path".

* To be honest.....I know my code is messy or even unreadable, I hope I will have time to add some comment and make it better. Also, if you can understand my code, you can add comments on it!

---

THX for reading this README....