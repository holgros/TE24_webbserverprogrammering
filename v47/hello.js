// starta genom att ange kommandot "node hello.js" i mappen där filen ligger

let http = require("http");

http.createServer(function (req, res) {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end("<h1>Hello World!</h1>");
}).listen(8080);

console.log(
  "Webbserver lyssnar på port 8080. Öppna i webbläsaren på localhost:8080 eller [din ip-adress]:8080. Avsluta i kommandotolken med ctrl-C."
);
