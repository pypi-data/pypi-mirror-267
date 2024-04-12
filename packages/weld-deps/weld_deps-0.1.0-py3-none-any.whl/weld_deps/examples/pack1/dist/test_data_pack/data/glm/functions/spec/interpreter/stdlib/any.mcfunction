function glm:spec/helpers/check {describes: "Any on an empty array", expects: ["false"], receives: ["any([], -> () true)"]}
function glm:spec/helpers/check {describes: "Any successfully matching on an array", expects: ["true"], receives: ["any([1,2,3,4,5], -> (x) x % 2 == 0 && x >= 4)"]}
function glm:spec/helpers/check {describes: "Any unsuccessfully matching on an array", expects: ["false"], receives: ["any(['Hi','how','are','you'], -> (s) len(s) > 3)"]}
function glm:spec/helpers/check {describes: "Any successfully matching on an object", expects: ["true"], receives: ["any({a:1,b:2,c:3,d:4}, -> (k,v) v % 2 == 0 && k != 'b')"]}
function glm:spec/helpers/check {describes: "Any unsuccessfully matching on an object", expects: ["false"], receives: ["any({a:2,b:3}, -> (k,v) v % 2 == 0 && k == 'b')"]}
function glm:spec/helpers/check {describes: "Any successfully matching on a string", expects: ["true"], receives: ["any('Hi', -> (c) ascii(c) < 97)"]}
function glm:spec/helpers/check {describes: "Any unsuccessfully matching on a string", expects: ["false"], receives: ["any('fizzbuzz', -> (c) ascii(c) < 97)"]}
