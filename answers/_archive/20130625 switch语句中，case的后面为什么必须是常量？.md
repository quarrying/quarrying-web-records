#! https://www.zhihu.com/question/21240276/answer/17655473

[comment]: <> (Answer URL: https://www.zhihu.com/question/21240276/answer/17655473)
[comment]: <> (Question Title: switch语句中，case的后面为什么必须是常量？)
[comment]: <> (Author Name: 采石工)
[comment]: <> (Create Time: 2013-06-25 12:19:38)

下面是我的笔记，希望有用！

> Any statement within the switch statement can be labeled with one or more case labels as follows: "case constant-expression :". where the constant-expression shall be a converted constant expression of the promoted type of the switch condition. No two of the case constants in the same switch shall have the same value after conversion to the promoted type of the switch condition. (C++ 标准)

讨论：为什么是case constant-expression:而不是case expression:？  

可以避免二义性，Consider switch (c) { case a: ...; break; case b: ...; break; }. What would you expect to happen if a==b and b==c? 另外 if the expression in label is not a constant, then it can't determine where each value goes at compile-time.

