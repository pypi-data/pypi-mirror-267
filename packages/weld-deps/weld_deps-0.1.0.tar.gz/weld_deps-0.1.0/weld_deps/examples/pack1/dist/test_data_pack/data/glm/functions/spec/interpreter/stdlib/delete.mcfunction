function glm:spec/helpers/check {describes: "Deleting from an array", expects: ["[1,2,4]"], receives: ["delete([1,2,3,4], 2)"]}
function glm:spec/helpers/check {describes: "Unsuccessfully deleting from an array", expects: ["[1,2,3]"], receives: ["delete([1,2,3], 42)"]}
function glm:spec/helpers/check {describes: "Deleting from an object", expects: ["{a:1,c:3}"], receives: ["delete({a:1,b:2,c:3}, 'b')"]}
function glm:spec/helpers/check {describes: "Unsuccessfully deleting from an object", expects: ["{a:false,bar:'foo'}"], receives: ["delete({a:false,bar:'foo'},'l')"]}
function glm:spec/helpers/check {describes: "Deleting from a string", expects: ["'Hell nah'"], receives: ["delete('Hello nah', 4)"]}
function glm:spec/helpers/check {describes: "Unsuccessfully deleting from a string", expects: ["'hi'"], receives: ["delete('hi', 69)"]}

