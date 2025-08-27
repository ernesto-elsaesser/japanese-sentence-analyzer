<?php
$url = 'https://www.edrdg.org/cgi-bin/wwwjdic/wwwjdic?1ZUJ' . $_GET['q'];
echo file_get_contents($url);
?>