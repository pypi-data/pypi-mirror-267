function glm:spec/helpers/check {describes: "Arr on an array", expects: ["[1,2,3]"], receives: ["arr([1,2,3], ->(x) x + 1)"]}
function glm:spec/helpers/check {describes: "Arr on an object", expects: ["[['a', 1], ['b', 2]]"], receives: ["arr({a: 1, b: 2})"]}
function glm:spec/helpers/check {describes: "Arr on a string", expects: ["['a','b','c']"], receives: ["arr('abc')"]}
