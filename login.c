#include <stdio.h>

int main(void){
	printf("%s%c%c\n","Content-Type:text/html;charset=iso-8859-1",13,10);
	printf("<html>\n<head>\n");
	printf("\t<title>Logging In...</title>\n<link href='../a4/common.css' rel='stylesheet' type='text/css'>\n\n<body>\n");
	printf("\t<div id='content'>\n \
		<span id='heading'>The <span id='teamname'>Quad-Core</span><br />Programmers</span><br /><br /> \
		This is not implemented yet!<br /><a href='http://cs.mcgill.ca/~vserva1/welcome.html'>Go Home</a>\n<br/> \
		or go straight to the <a href='http://cs.mcgill.ca/~vserva1/room1.html'>first room.</a> \
	</div>\n \
	<div id='left' class='wing'>&nbsp;</div>\n \
	<div id='right' class='wing'>&nbsp;</div>\
	<div id='border'></div>");
	printf("\n</body>\n</html>");
	return 0;
}