function glm:spec/helpers/check {describes: "Every on an empty array", expects: ["true"], receives: ["every([], -> () false)"]}
function glm:spec/helpers/check {describes: "Every successfully matching on an array", expects: ["true"], receives: ["every([2,4,6], -> (x) x % 2 == 0)"]}
function glm:spec/helpers/check {describes: "Every unsuccessfully matching on an array", expects: ["false"], receives: ["every([2,4,6,7], -> (x) x % 2 == 0)"]}
function glm:spec/helpers/check {describes: "Every successfully matching on an object", expects: ["true"], receives: ["every({a:1,b:3,d:5}, -> (k,v) v % 2 != 0 && k != 'c')"]}
function glm:spec/helpers/check {describes: "Every unsuccessfully matching on an object", expects: ["false"], receives: ["every({foo:'bar',hi:-1}, -> (k,v) len(k) == 3)"]}
function glm:spec/helpers/check {describes: "Every successfully matching on a string", expects: ["true"], receives: ["every('HI :)', -> (c) ascii(c) < 97)"]}
function glm:spec/helpers/check {describes: "Every unsuccessfully matching on a string", expects: ["false"], receives: ["every('Hello !', -> (c) c != ' ')"]}
