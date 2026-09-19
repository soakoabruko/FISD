PS C:\Install\MyWorks\kpfu\FISD> cd cw2
PS C:\Install\MyWorks\kpfu\FISD\cw2> python server.py
PS C:\Install\MyWorks\kpfu\FISD\cw2>



PS C:\Install\MyWorks\kpfu\FISD> cd cw2
PS C:\Install\MyWorks\kpfu\FISD\cw2> python client.py
List of commands:
JOIN <username> - registration
TEXT <message> - broadcast
LIST - list of online users
QUIT - exit

JOIN user1
[SERVER] Welcome, user1!
[SERVER] user2 logged in.
[SERVER] user3 logged in.
TEXT hello         
[user1] hello
[user2] hello
[SERVER] user2 logged out.
[SERVER] user3 logged out.
QUIT
PS C:\Install\MyWorks\kpfu\FISD\cw2>



PS C:\Install\MyWorks\kpfu\FISD> cd cw2
PS C:\Install\MyWorks\kpfu\FISD\cw2> python client.py
List of commands:
JOIN <username> - registration
TEXT <message> - broadcast
LIST - list of online users
QUIT - exit

JOIN user2
[SERVER] Welcome, user2!
[SERVER] user3 logged in.
[user1] hello
TEXT hello
[user2] hello
LIST
[SERVER] Online users:
user1
user2
user3
QUIT
PS C:\Install\MyWorks\kpfu\FISD\cw2>



PS C:\Install\MyWorks\kpfu\FISD> cd cw2
PS C:\Install\MyWorks\kpfu\FISD\cw2> python client.py
List of commands:
JOIN <username> - registration
TEXT <message> - broadcast
LIST - list of online users
QUIT - exit

JOIN user3
[SERVER] Welcome, user3!
[user1] hello
[user2] hello
[SERVER] user2 logged out.
PS C:\Install\MyWorks\kpfu\FISD\cw2>