
'use strict';

document.addEventListener('DOMContentLoaded', function ()
{
	const email = document.getElementById('text-conversion').firstChild;

	email.nodeValue = email.nodeValue
        .replaceAll(' ',  '')
        .replace('d',  'inb')
        .replace('on', 'ox.ka')
        .replace('t',  'leb')
        .replace('sc', '@')
        .replace('ra', 'gma')
        .replace('pe', 'il.c')
        .replace('me', 'om'); 
});

document.addEventListener('DOMContentLoaded', function ()
{
	const a = document.getElementById('link-conversion');

	a.setAttribute('href', a.getAttribute('href')
        .replaceAll(' ',  '')
        .replace('do', 'nb')
        .replace('nt', 'ox.ka')
        .replace('sc', 'leb@')
        .replace('ra', 'gma')
        .replace('pe', 'il.c')
        .replace('me', 'om')
        .replace('please',  'mailto:i')
	);
});
