let http = require("http");
var fs = require("fs");

http.createServer(function (req, res) {
    res.writeHead(200, { "Content-Type": "text/html" });
    fs.readFile("index.html", function (err, data) {
        data = data.toString();
        res.end(data);
    });
}).listen(8080);

console.log(
  "Webbserver lyssnar på port 8080. Öppna i webbläsaren på localhost:8080 eller [din ip-adress]:8080. Avsluta i kommandotolken med ctrl-C."
);