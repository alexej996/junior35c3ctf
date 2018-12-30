# pretty_linear

#### Obtaining the matrix
First we need to extract the matrix from the packets in **surveillance.pcap**.

We can open the **pcap** file in Wireshark and filter only packets with some data in them with by putting *data.data* in the filter field.
Exporting these packets to a new pcap file will make it easier for us, so we do that in Wireshark under *File->Export Specified Packets...* and write the name of our new file, let's call it "data".
Wireshark will automatically add the file extension to it.

Now let's read data from these packets with *tcpick* and put them in a text file:
`tcpick -r [filename] -yP >> data.txt`

This file will need some manual cleaning. You can use any commands you want to speed this up.
We just need to clean up first and last few lines that tcpick writes that isn't packet data.
We can use *sed* to remove the "ACCESS GRANTED" packets that we don't need.
`sed -i ':a;N;$!ba;s/ACCESS GRANTED\n923fa1835d8dbdcd9f9b0e6658b24fce54512fbba71d7a0012c37d2c9dd094a6278593d8d9f7a4aa9fecb66042\n//g' data.txt`

That should leave us with a *data.txt* file that will have challange numbers that are followed by sums.
If there are any empty lines in data.txt file they should be removed before we raname it to **matrix** so **solve.py** can read it and solve it.

#### Solving the matrix
These chalanges when multipled with the keys make a system of linear equations that can be solved with Cramer's rule.
We just need to make sure to stay in the congruence subgroup of the modulo *p*.

This will mainly impact how we divide determinants so that we don't get fractions.
This can be done by finding the *modular multiplicative inverse* of the determinant we are dividing with.
Modular multiplicative inverse can be found very fast with extended Euclidean algorithm.

Some python libraries do this for us, such as *inverse()* function in the *Crypto.Util.number* library.
The rest of calculations are quite simple, where the slowest are actually calculating the 40x40 determinants, although solve.py does this in couple of minutes on modern CPUs.

The key obtained by solving the system can be used then to decrypt the AES cyphertext by SHA256 hashing the keys list to use as a decryption key.
