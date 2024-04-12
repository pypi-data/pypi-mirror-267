benchmark:
	rm -rf tmp_pdfs-*
	/usr/bin/time -f "%e %M" /usr/bin/python noteshrunk-multiprocessing.py -y -k -o output-multiprocessing.pdf tmp/notesA1.jpg tmp/notes*
	/usr/bin/time -f "%e %M" /usr/bin/python noteshrunk-multithreading.py  -y -k -o output-multithreading.pdf  tmp/notesA1.jpg tmp/notes*
